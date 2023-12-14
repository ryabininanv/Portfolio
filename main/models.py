from django.contrib.auth.models import User
from django.db import models


# --------------------------------------Таблица-для-учителей--------------------------------------#
class Teacher(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Фамилия")
    last_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, verbose_name="Отчество")

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = '1. Преподаватели'

    def get_short(self):
        return f'{self.first_name} {self.last_name[0]}.{self.patronymic[0]}.'

    def __str__(self):
        return f"{self.get_short()}"


# --------------------------------------Таблица-для-групп--------------------------------------#
class Gorup(models.Model):
    name = models.CharField(max_length=20, verbose_name="Группа")
    special = models.CharField(max_length=100, verbose_name="Специальность", null=True)
    course = models.IntegerField(verbose_name="Курс")

    def get_semestrs(self, user):
        Semestr.objects.filter()

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = '2. Группы'

    def __str__(self):
        return f"{self.name}"


# ----------------------------------Таблица-для-студентов----------------------------------------#
class Data(models.Model):
    fio = models.CharField(max_length=100, verbose_name="Фамилия")
    name = models.CharField(max_length=100, verbose_name="Имя")
    vuz = models.CharField(max_length=100, verbose_name="Учебное заведение", null=True)
    patronymic = models.CharField(max_length=100, verbose_name="Отчество")
    faculty = models.CharField(max_length=100, verbose_name="Факультет")
    group = models.ForeignKey(Gorup, on_delete=models.CASCADE, related_name="group_data", null=True,
                              verbose_name="Группа")
    zachnumber = models.IntegerField(verbose_name="Номер зачетной книжки")
    year = models.IntegerField(verbose_name="Год поступления")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_data", null=True,
                                verbose_name="Пользователь")

    def get_short(self):
        return f'{self.fio} {self.name[0]}.{self.patronymic[0]}.'

    def get_count_subject(self):
        result = 0
        for subject in Subject.objects.filter(semestr=Semestr.objects.filter(group=self.group).first()):
            result += 1
        return result

    def get_sum(self):
        result = 0
        for mark in Mark_Note.objects.filter(student=self):
            result += mark.mark
        return round(result/self.get_count_subject(),1)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = '3. Студенты'

    def __str__(self):
        return f"{self.get_short()}"


# ----------------------------------Таблица-для-семестров----------------------------------------#
class Semestr(models.Model):
    year = models.CharField(max_length=20, verbose_name="Учебный год")
    semestr = models.IntegerField(verbose_name="Семестр")
    group = models.ForeignKey(Gorup, on_delete=models.CASCADE, related_name="semestr_group", null=True,
                              verbose_name="Группа")

    def get_subject(self):
        return Subject.objects.filter(semestr=self)

    class Meta:
        verbose_name = 'Семестр'
        verbose_name_plural = '4. Семестры'

    def __str__(self):
        return f"{self.semestr} семестр, {self.group.name}"


# ----------------------------------Таблица-для-предметов----------------------------------------#
class Subject(models.Model):
    type_list = (("Экзамен", "Экзамен",), ("Зачет", "Зачет"))
    status_list = (("Не закрыта", "Не закрыта",), ("Закрыта", "Закрыта"))
    name_subject = models.CharField(max_length=100, verbose_name="Название")
    type = models.CharField(max_length=50, choices=type_list, verbose_name="Тип атестации")
    numberved = models.CharField(max_length=20, null=True, verbose_name="Номер ведомости")
    vedstatus = models.CharField(max_length=50, choices=status_list, null=True, verbose_name="Статус ведомости")
    link = models.CharField(max_length=500, null=True, blank=True, verbose_name="Ссылка на предмет, в системе ДО")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="teacher_subject", null=True,
                                verbose_name="Преподаватель")
    semestr = models.ForeignKey(Semestr, on_delete=models.CASCADE, related_name="semestr_subject", null=True,
                                verbose_name="Семестр")

    def get_marks(self, student):
        return Mark_Note.objects.filter(subject=self, student=student)

    def get_current_ball(self, student):
        result = 0
        for mark in self.get_marks(student):
            result += mark.mark
        if result > 100:
            return 100
        return result

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = '5. Предметы'

    def __str__(self):
        return self.name_subject


# ----------------------------------Таблица-для-оценок-------------------------------------------#
class Mark_Note(models.Model):
    mark = models.IntegerField(null=True, blank=True, verbose_name="Оценка")
    note = models.CharField(max_length=100, verbose_name="За что")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subject_mark", null=True,
                                verbose_name="По какому предмету")
    student = models.ForeignKey(Data, on_delete=models.CASCADE, related_name="student_mark", null=True,
                                verbose_name="Кому")

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = '6. Оценки'


class RaspisanieWeek(models.Model):
    week_list = (("Четная", "Четная",), ("Нечетная", "Нечетная"))
    group = models.ForeignKey(Gorup, on_delete=models.CASCADE, related_name="raspisanieweek_group", null=True,
                              verbose_name="Группа")
    week = models.CharField(max_length=20, choices=week_list, verbose_name="Неделя")

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = '7. Расписания(недели)'

    def __str__(self):
        return f"{self.week} неделя, {self.group.name}"


class RaspisanieDay(models.Model):
    week = models.ForeignKey(RaspisanieWeek, on_delete=models.CASCADE, related_name="raspisanieday_group", null=True,
                             verbose_name="Неделя")
    week_list = (("Понедельник", "Понедельник",), ("Вторник", "Вторник"), ("Среда", "Среда"), ("Четверг", "Четверг"),
                 ("Пятница", "Пятница"), ("Суббота", "Суббота"))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="raspisanieday_subjects",
                                verbose_name="Предмет")
    day = models.CharField(max_length=20, choices=week_list, verbose_name="День")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="raspisanieday_teacher", null=True,
                                verbose_name="Преподаватель")
    time = models.TimeField(blank=True, null=True, verbose_name="Начало пары")

    cab = models.CharField(max_length=40, blank=True, null=True, verbose_name="Кабинет")
    type = models.CharField(max_length=60, null=True, verbose_name="Тип занятия")

    def get_time(self):
        return self.time.strftime("%H:%M")

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = '8. Расписания(Дни)'


class Reiting:
    def __init__(self):
        self.sum_bal = 0
        self.position = 1
        self.data = None
