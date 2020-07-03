"""Profession URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Test import views as test_views
from LoginSys import views as auth_views
from Pages import views as pages_views
from PersonalAccount import views as account_views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from LoginSys import views as loginsys_views

from Profile import views as callback_views
from Pages import views as pages_views



urlpatterns = [
    path('admin/', admin.site.urls),  # Админка
    path('', pages_views.home_page, name="home"),  # Стартовая страница

    path('test/<test_index>/', test_views.single_test, name='sinlge_test'),  # Конкретный тест

    path('account/reset_answers/', account_views.reset_answers),  # Очистить ответы пользователя

    path('reset_test/<test_index>/', account_views.reset_answer, name='reset_test'),  # Allow to pass a test again

    path('auth/login/', auth_views.login),  # Страница авторизации
    path('auth/logout/', auth_views.logout),  # Выход из авторизации
    path('auth/registration/', auth_views.registration),  # Регистрация


    path('reset-password/', loginsys_views.MyPasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/',
    PasswordResetCompleteView.as_view(),name='password_reset_complete'),


    path('account/', account_views.personal_account),  # Вход в личный кабинет


    path('personal_tests/', account_views.personal_tests, name='all_tests'),


    path('change_password/', auth_views.change_password, name="change_password"),  # Изменение данных профиля
    path('change_profile_data/', account_views.change_profile_data, name="change_profile_data"),  # Изменение данных профиля
    path('personal_info/', account_views.profile_data, name="personal_info"),  # Изменение данных профиля
    path('delete_account/', account_views.delete_account, name="delete_account"),  # Изменение данных профиля



    path('contact/', pages_views.contact_us),  # Контактная форма
    path('test/<test_index>/result/', test_views.test_results_all, name="test_result"),  # all results of a test

    path('save_test_result/<test_index>/', test_views.save_test_result, name="save_test_result"),  # save result

    path('activate_user/<current_login>/<activation_salt>', account_views.activate_user),

    path('tz_detect/', include('tz_detect.urls')),

    path('get_final_result/', test_views.get_final_result, name="get_final_result"),
    path('final_result/', test_views.final_result_page, name="final_result"),

    path('record_callback/', callback_views.record_callback, name="callback"),
    path('confidentiality/', pages_views.confidentiality_page, name="confidentiality"),
    path('terms/', pages_views.terms_page, name="terms"),
    path('about/', pages_views.about_page, name="about"),
    path('my-vam-polezny-esli/', pages_views.about_page_2, name="about_2"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
