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
        return render(request, 'padawan_form.html', {'planets': Planet.objects.all()})


def home(request):
    return render(request, 'home.html')


def test_view(request):
    if request.method == 'GET':
        test = Test.objects.all()
        test = test[random.randint(0, len(test) - 1)]
        padawan = Padawan.objects.get(email=request.GET.get('padawanEmail'))
        padawan.test = test
        padawan.save()
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
        if len(Padawan.objects.filter(master__name=name)) == 3:
            return render(request, 'deny.html')
        planet = Jedi.objects.get(name=name).planet
        padawans = Padawan.objects.filter(planet=planet)
        answers = PadawanAnswer.objects.all()
        return render(request, 'candidate_sel.html', {'name': name,
                                                      'padawans': padawans,
                                                      'answers': answers})
    else:
        mail = request.POST.get('email')
        padawan = Padawan.objects.get(email=mail)
        padawan.master = Jedi.objects.get(name=request.GET.get('name'))
        padawan.save()
        send_mail('Academy',
                  "You've been accepted to be padawan of %s" % (request.GET.get('name')),
                  'byskillcfpro@gmail.com',
                  [mail],
                  fail_silently=False)
        return render(request, 'sent.html')


def jedi_take(request):
    if request.method == 'GET':
        names = [jedi.name for jedi in Jedi.objects.all()]
        return render(request, 'jedi.html', {'names': names})
    else:
        base_url = reverse(jedi_candidate_sel)
        query_string = urlencode({'name': request.POST.get('name')})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)


def jedi_list_num(request):
    jedis = Jedi.objects.all()
    jedis = {jedi.name: 0 for jedi in jedis}
    for padawan in Padawan.objects.all():
        if padawan.master:
            jedis[padawan.master.name] += 1
    if int(request.GET.get('num')):
        jedis = {jedi: num for jedi, num in jedis.items() if num > 1}
    return render(request, 'jedis_list_num.html', {'jedis': jedis})
