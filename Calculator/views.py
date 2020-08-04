from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .BackEnd.Calculator.Calculator import evaluate


def index(request):

    template_name = "Calculator/index.html"
    return render(request, template_name)


def calculate(request, expression):
    
    expression = expression.replace('@', '/', -1)
    result = evaluate(expression)
    return JsonResponse({'result': result})
    
