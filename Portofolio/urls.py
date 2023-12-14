from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from Portofolio import settings
from main import views

urlpatterns = [
                  path("admin/", admin.site.urls),  # Ссылка на админ паенль
                  path("", views.main, name="home"),  # Ссылка на страницу сведений
                  path("login/", views.loginPage, name="login"),  # Ссылка на страницу входа
                  path("logout/", views.doLogout, name="logout"),  # Ссылка на выход
                  path("raspisanie/", views.raspisanie, name="raspisanie"),  # Ссылка на страницу расписания
                  path("grade_current/", views.grade, name="grade_current"),  # Ссылка на страницу успеваемости
                  path("grade_current_subject/", views.grade_subject, name="grade_current_subject"),  # Ссылка на страницу успеваемости с раскрытым предметом
                  path("grade_current_subject_podrobnee/", views.grade_subject_podrobnee, name="grade_current_subject_podrobnee"),  # Ссылка на страницу успеваемости с раскрытым предметом и оценками
                  path("reiting/", views.reiting, name="reiting"),  # Ссылка на страницу рейтинг
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
