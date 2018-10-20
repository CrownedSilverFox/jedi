from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.urls import reverse
from .models import Padawan
from .models import PadawanAnswer
from .models import Test
from .models import Planet
from .models import Jedi
from django.core.mail import send_mail
import random


def padawan_auth(request):
    if request.method == 'POST':
        Padawan.objects.create(name=request.POST.get('name'),
                               email=request.POST.get('email'),
                               planet=Planet.objects.get(name=request.POST.get('planet')))
        base_url = reverse(test_view)
        query_string = urlencode({'padawanEmail': request.POST.get('email')})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
    else:
        return render(request, 'padawan_form.html')


def home(request):
    return render(request, 'home.html')


def test_view(request):
    if request.method == 'GET':
        test = Test.objects.all()
        test = test[random.randint(0, len(test) - 1)]
        test_key = test.key
        test = list(test.questions.all())
        return render(request, 'test.html', {'test': test, 'test_key': test_key,
                                             'email': request.GET.get('padawanEmail')})
    else:
        padawan = Padawan.objects.get(email=request.POST.get('padawanEmail'))
        answers = []
        for i, _q in enumerate(Test.objects.get(key=request.POST.get('testKey')).questions.all()):
            answers.append(request.POST.get('quest_%s' % i))
        for i, answer in enumerate(answers):
            PadawanAnswer.objects.create(answer=answer, padawan=padawan,
                                         question=Test.objects.get(key=request.POST.get('testKey')).questions.all()[i])
        return render(request, 'success.html')


def jedi_candidate_sel(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        if len(Padawan.objects.filter(master__name=name)):
            return render(request, 'deny.html')
        planet = Jedi.objects.get(name=name).planet
        padawans = Padawan.objects.filter(planet=planet)
        answers = PadawanAnswer.objects.all()
        return render(request, 'candidate_sel.html', {'name': name,
                                                      'padawans': padawans,
                                                      'answers': answers})
    else:
        mail = request.POST.get('email')
        send_mail('Academy',
                  "You've been accepted to be padawan of",
                  'byskillcfpro@gmail.com',
                  mail)


def jedi_take(request):
    if request.method == 'GET':
        names = [jedi.name for jedi in Jedi.objects.all()]
        return render(request, 'jedi.html', {'names': names})
    else:
        base_url = reverse(jedi_candidate_sel)
        query_string = urlencode({'name': request.POST.get('name')})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)


