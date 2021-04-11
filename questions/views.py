import json
from random import randint
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as _login
from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponse, get_object_or_404
from django.db import IntegrityError

from .models import Questions, Answer, Exam

NEGATIVE_MARK_FLAG = False
NUMBER_OF_QUESTIONS = 2


def log(request):
    return HttpResponse(request)

# Question.objects.create()
# Question()
# (form data) -> request.POST
# (json) -> request.POST (empty)
# class view

"""
example request :
{
    "title" :"is earth flat ?",
    "choice1" :"yes",
    "choice2" :"no",
    "choice3" :"",
    "choice4" :"",
    "correct_choice" : 2
}
"""

@csrf_exempt
def add_question(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            # Questions.objects.create(

            # )
            question_obj = Questions()
            question_obj.title = data['title']
            question_obj.choice1 = data['choice1']
            question_obj.choice2 = data['choice2']
            question_obj.correct_choice = data['correct_choice']
            try:
                question_obj.choice3 = data['choice3']
                question_obj.choice4 = data['choice4']
            except Exception as e:
                pass
        except:
            return JsonResponse({"message": "Bad Input"})
        try:
            question_obj.save()
        except IntegrityError as e:
            return JsonResponse({"messae":"Look The question title is unique .. :)"})
            
        return JsonResponse({"messae": "Question Added!"})

def remove_correct_choice(list_of_questions):
    res = []
    for question in list_of_questions:
        res.append({
            "title": question.title,
            "1": question.choice1,
            "2": question.choice2,
            "3": question.choice3,
            "4": question.choice4,
            "answer" : ""
        })
    return res


"""
Gets nothing and respondes with 
example :
{
    id : 3,
    questions : [
        {
            title : "is earth flat ? ",
            1: "yes",
            2: "no",
            3: "",
            4: ""
        },
        {
            title : "What year is it ? ",
            1: "1325",
            2: "1998",
            3: "2220",
            4: "2021"
        }
    ]
}
"""


@csrf_exempt
def start_exam(request):
    if request.method == "GET":
        users_questions = []

        question_list = Questions.objects.all()
        if len(question_list) > NUMBER_OF_QUESTIONS:
            for i in range(0, NUMBER_OF_QUESTIONS, 1):

                # Make Sure All Questions Are Unique
                while True:
                    random_index = randint(0, len(question_list) - 1)
                    if question_list[random_index] not in users_questions:
                        break

                users_questions.append(
                    question_list[random_index]
                )
            exam_obj = Exam.objects.create(user = request.user)
            for q_obj in users_questions:
                exam_obj.questions.add(q_obj)
            exam_obj.save()
            return JsonResponse({"id": exam_obj.id,
                                 "questions": remove_correct_choice(users_questions)})
        else:
            return JsonResponse({"message": "database is small :)"})


'''
example request data is :
{
    exam_id : 3,
    questions : [list_of_questions
        {
            title : "is earth flat ? ",
            1: "yes",
            2: "no",
            3: "",
            4: ""
            answer : 1
        },
        {
            title : "What year is it ? ",
            1: "1325",
            2: "1998",
            3: "2220",
            4: "2021"
            answer : 4
        }
    ]
}
'''


@csrf_exempt
def answer_exam(request):
    if request.method == "POST":
        result = 0
        data = json.loads(request.body)
        exam_obj = get_object_or_404(Exam, id=data["id"])
        if exam_obj.result != None:
            return JsonResponse({"error": f"Already Answered this exam on {exam_obj.answered_at} \n and your result was {exam_obj.result}"})
        for question in data['questions']:
            q_obj = get_object_or_404(Questions, title=question['title'])
            exam_obj.answers.add(
                Answer.objects.create(user = request.user,
                                      question = q_obj,
                                      answer= question['answer'])
            )
            if int(question['answer']) == q_obj.correct_choice:
                result += 1
            elif NEGATIVE_MARK_FLAG:
                result -= 0.33
        result /= NUMBER_OF_QUESTIONS 
        result *= 100
        exam_obj.result = result
        exam_obj.save()
        return JsonResponse({"result": result })
