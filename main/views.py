import operator
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from main import authorization
from main.admin import *

#------------------------------------Функция-отображения-страницы-сведений--------------------------------#
def main(request):
    if not request.user.is_authenticated:
        return redirect(loginPage)
    return render(request, "main.html", {"student": Data.objects.filter(student=request.user).first()})


#------------------------------------Функция-отображения-страницы-расписания--------------------------------#
def raspisanie(request):
    if not request.user.is_authenticated:
        return redirect(loginPage)

    cur_day = datetime.now().weekday()
    cur_week = "c" if datetime.now().isocalendar()[1]%2 == 0 else "n"
    data = Data.objects.filter(student=request.user).first()
    week = RaspisanieWeek.objects.filter(group=data.group)
    cweek = week.filter(week="Четная")
    nweek = week.filter(week="Нечетная")
    cdays = RaspisanieDay.objects.filter(week=cweek.first())
    ndays = RaspisanieDay.objects.filter(week=nweek.first())

    context = {
        "cur_week": cur_week,
        "curday": cur_day,
        "student": data,
        "cweek": cweek,
        "cmonday": cdays.filter(day="Понедельник"),
        "ctuesday": cdays.filter(day="Вторник"),
        "cwednesday": cdays.filter(day="Среда"),
        "cthursday": cdays.filter(day="Четверг"),
        "cfriday": cdays.filter(day="Пятница"),
        "csaturday": cdays.filter(day="Суббота"),
        "nweek": nweek,
        "nmonday": ndays.filter(day="Понедельник"),
        "ntuesday": ndays.filter(day="Вторник"),
        "nwednesday": ndays.filter(day="Среда"),
        "nthursday": ndays.filter(day="Четверг"),
        "nfriday": ndays.filter(day="Пятница"),
        "nsaturday": ndays.filter(day="Суббота"),
        "empty": cdays.filter(day="Пятница"),

    }
    print(context["cfriday"], context["empty"])
    return render(request, "raspisanie/raspisanie.html", context)

#------------------------------------Функция-отображения-страницы-рейтинга--------------------------------#
def reiting(request):
    if not request.user.is_authenticated:
        return redirect(loginPage)
    data = Data.objects.filter(student=request.user).first()
    reiting_list = []
    for student in Data.objects.all():
        r = Reiting()
        r.sum_bal = student.get_sum()
        r.data = student
        reiting_list.append(r)
    reiting_list.sort(key=operator.attrgetter('sum_bal'))
    reiting_list.reverse()
    mesto = 1
    for r in reiting_list:
        r.position = reiting_list.index(r)+1
        if r.data == data:
            mesto = r.position
    print(reiting_list)

    context = {
        "student": data,
        "dats": reiting_list,
        "mesto": mesto
    }
    return render(request, "reiting/reiting.html", context)

#------------------------------------Функция-отображения-страницы-успеваемости--------------------------------#
def grade(request):
    if not request.user.is_authenticated:
        return redirect(loginPage)
    data = Data.objects.filter(student=request.user).first()
    semestrs = Semestr.objects.filter(group=data.group)
    context = {
        "student": data,
        "semestrs": semestrs,
    }
    if semestrs.exists():
        context["semestr"]=semestrs.last()
        context["subjects"]=semestrs.last().get_subject()

    return render(request, "grade/grade.html", context)

#------------------------------------Функция-отображения-страницы-успеваемости-с-раскрытым-предметом------------#
def grade_subject(request):
    if not request.user.is_authenticated:
        return redirect(loginPage)
    data = Data.objects.filter(student=request.user).first()
    cursubject = Subject.objects.filter(id=request.GET['id']).first()
    semestr = Semestr.objects.filter(group=data.group).last()
    context = {
        "student": data,
        "semestr": semestr,
        "cursubjects": cursubject,
        "subjects": semestr.get_subject(),
        "cur_ball": cursubject.get_current_ball(data)
    }
    return render(request, "grade/grade_subject.html", context)

#------------------------------------Функция-отображения-страницы-успеваемости-с-раскрытым-предметом-и-оценками-----#
def grade_subject_podrobnee(request):
    if not request.user.is_authenticated:
        return redirect(loginPage)
    data = Data.objects.filter(student=request.user).first()
    cursubject = Subject.objects.filter(id=request.GET['id']).first()
    semestr = Semestr.objects.filter(group=data.group).last()
    context = {
        "student": data,
        "semestr": semestr,
        "cursubjects": cursubject,
        "subjects": semestr.get_subject(),
        "marks": cursubject.get_marks(data),
        "cur_ball": cursubject.get_current_ball(data)
    }
    return render(request, "grade/grade_subject_pordrobnee.html", context)

#------------------------------------Функция-отображения-страницы-авторизации--------------------------------#
def loginPage(request):
    form = authorization.LoginForm()
    if request.method == 'POST':
        form = authorization.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(main)
            else:
                form.add_error(None, 'Неверные данные!')
    return render(request, 'login.html', {'form': form})

#------------------------------------Функция-выхода-из-аккаунта--------------------------------#
def doLogout(request):
    logout(request)
    return redirect(loginPage)
