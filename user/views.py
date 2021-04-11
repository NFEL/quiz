import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login  as _login
from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponse
from django.db import IntegrityError

from questions.models import Questions,Answer



User = get_user_model()

@csrf_exempt
def signup(request):
    if request.method == 'POST' :
        data=json.loads(request.body)
        if len(data['password']) < 8 :
            return HttpResponse("Short Password")
        try:
            user_obj = User.objects.create_user(data['username'],data['email'],data['password'])
            # user_obj.save()
            return HttpResponse(user_obj)
        except IntegrityError as e:
            return HttpResponse("Bad Username (unique u know) ")
        

@csrf_exempt
def login(request):
    if request.method == 'POST':
        print(request.POST)
        data=json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if not user :
            return HttpResponse("Bad Cridential")
        else:
            _login(request, user)
            return HttpResponse('Success :)')
            
@csrf_exempt
def whoami(request):
    return HttpResponse([request.user])


@csrf_exempt
def answer_question(request):
    data = json.loads(request.body)
    for answer in data['answers']:
        question_obj = Questions.objects.get(title = answer['title'])
        Answer.objects.create(user=request.user,
                              question = question_obj,
                              answer = answer['answer'])







import json
from django.shortcuts import HttpResponse ,redirect

@csrf_exempt
def hello_world(request):
    if request.method == 'GET':
        return HttpResponse("Hello")
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data['username'])
        print(data['pass'])
        print(data['email'])
        return HttpResponse("POST baram frestad")
    


# HttpResponse -> "OK"

# JsonResponse -> {
#     "key" : "value"
# }
# render (<- template )-> webpage

# redirect

