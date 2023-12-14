from django.contrib import admin
from django import forms
from django.forms import ModelForm
from main.models import *


# ------------------------------Свои-поля-для-ввода---------------------------#
class MyDateForm(forms.DateInput):
    input_type = 'date'

class MyTimeForm(forms.TimeInput):
    input_type = 'time'

class ChoiceShortName(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.get_short())


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class CutsomChoiceSubject(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name_subject)

class ChoiceWeek(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.week, obj.group.name)


class ChoiceSemestr(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "Семестр: %s" % (obj.semestr)


# ------------------------------Свои-формы-для-ввода---------------------------#
class SemestrAdminForm(forms.ModelForm):
    group = CustomModelChoiceField(queryset=Gorup.objects.all())
    group.label = "Группа"

    class Meta:
        model = Semestr
        fields = "__all__"


class StudentForm(forms.ModelForm):
    group = CustomModelChoiceField(queryset=Gorup.objects.all())
    group.label = "Группа"

    class Meta:
        model = Data
        fields = "__all__"

class RaspisanieWeekForm(forms.ModelForm):
    group = CustomModelChoiceField(queryset=Gorup.objects.all())
    group.label = "Группа"

    class Meta:
        model = RaspisanieWeek
        fields = "__all__"


class RaspisanieDayForm(forms.ModelForm):
    week = ChoiceWeek(queryset=RaspisanieWeek.objects.all())
    week.label = "Неделя"
    subject = CutsomChoiceSubject(queryset=Subject.objects.all())
    subject.label = "Предмет"
    teacher = ChoiceShortName(queryset=Teacher.objects.all())
    teacher.label = "Преподаватель"

    class Meta:
        #widgets = {'my_time_field': MyTimeForm()}
        model = RaspisanieDay
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(RaspisanieDayForm, self).__init__(*args, **kwargs)
        self.fields["time"].widget = MyTimeForm()

class MarkAdminForm(forms.ModelForm):
    subject = CutsomChoiceSubject(queryset=Subject.objects.all())
    subject.label = "По какому предмету"
    student = ChoiceShortName(queryset=Data.objects.all())
    student.label = "Кому"

    class Meta:
        model = Mark_Note
        fields = "__all__"


class MySybjectAdminForm(forms.ModelForm):
    teacher = ChoiceShortName(queryset=Teacher.objects.all())
    teacher.label = "Преподаватель"
    # student = ChoiceShortName(queryset=Data.objects.all())
    # student.label = "Студент"
    semestr = ChoiceSemestr(queryset=Semestr.objects.all())
    semestr.label = "Семестр"

    class Meta:
        model = Subject
        fields = "__all__"


# ------------------------------Модели-для-админ-панели---------------------------#
class SubjectAdmin(admin.ModelAdmin):
    form = MySybjectAdminForm
    title = ['id', 'name_subject', 'type', 'numberved', 'vedstatus', 'teacher', "semestr", "link"]
    search_fields = ['name_subject', 'type', 'numberved', 'vedstatus', 'teacher', "semestr"]
    list_filter = ['name_subject', 'type', 'numberved', 'vedstatus', 'teacher', "semestr"]
    list_display = ['id', 'name_subject', 'type', 'numberved', 'vedstatus', 'teacher', "semestr", "link"]
    list_editable = ['name_subject', 'type', 'numberved', 'vedstatus', 'teacher', "semestr"]


class MarkAdmin(admin.ModelAdmin):
    form = MarkAdminForm
    title = ['id', 'mark', 'note', 'subject', 'student']
    search_fields = ['note', 'subject']
    list_filter = [ 'note', 'subject']
    list_display = ['id', 'mark', 'subject', 'note']
    list_editable = ['mark', 'note']


class Student(admin.ModelAdmin):
    form = StudentForm
    title = ['id', 'fio', 'name', 'patronymic', 'faculty', 'group', 'zachnumber', 'year', 'student']
    search_fields = ['fio', 'name', 'patronymic', 'faculty', 'zachnumber', 'year']
    list_filter = ['fio', 'name', 'patronymic', 'faculty', 'group', 'zachnumber', 'year', 'student']
    list_display = ['id', 'fio', 'name', 'patronymic', 'faculty', 'zachnumber', 'year', 'student']
    list_editable = ['fio', 'name', 'patronymic', 'faculty', 'zachnumber', 'year', 'student']

class Teacher_Model(admin.ModelAdmin):
    title = ['id', 'first_name', 'last_name', 'patronymic']
    search_fields = ['first_name', 'last_name', 'patronymic']
    list_filter = ['first_name', 'last_name', 'patronymic']
    list_display = ['id', 'first_name', 'last_name', 'patronymic']
    list_editable = ['first_name', 'last_name', 'patronymic']


class Semestr_Model(admin.ModelAdmin):
    form = SemestrAdminForm
    title = ['id', 'year', 'semestr', 'group']
    search_fields = ['year', 'semestr']
    list_filter = ['year', 'semestr']
    list_display = ['id', 'year', 'semestr']
    list_editable = ['year', 'semestr']

class RaspisanieWeek_Model(admin.ModelAdmin):
    form = RaspisanieWeekForm
    title = ['id', 'group', 'week']
    search_fields = ['group', 'week']
    list_filter = ['group', 'week']
    list_display = ['id', 'week', 'group']
    list_editable = ['week', 'group']

class RaspisanieDay_Model(admin.ModelAdmin):
    form = RaspisanieDayForm
    title = ['id', 'week', 'day', 'time', "subject", "type", "teacher", "cab"]
    search_fields = ['week', 'day', 'time', "subject", "type", "teacher","cab"]
    list_filter = ['week', 'day', 'time', "subject", "type", "teacher","cab"]
    list_display = ['id', 'week', 'day', 'time', "subject", "type", "teacher","cab"]
    list_editable = ['week', 'day', "subject", "type", "teacher","cab"]


class GroupAdmin(admin.ModelAdmin):
    title = ['id', 'name', 'course', 'special']
    search_fields = ['name', 'course', 'special']
    list_filter = ['name', 'course', 'special']
    list_display = ['id', 'name', 'course', 'special']
    list_editable = ['name', 'course', 'special']


# ------------------------------Добавление-таблиц-в-админ-панель---------------------------#
admin.site.register(Subject, SubjectAdmin)
admin.site.register(RaspisanieDay, RaspisanieDay_Model)
admin.site.register(RaspisanieWeek, RaspisanieWeek_Model)
admin.site.register(Mark_Note, MarkAdmin)
admin.site.register(Data, Student)
admin.site.register(Gorup, GroupAdmin)
admin.site.register(Semestr, Semestr_Model)
admin.site.register(Teacher, Teacher_Model)
