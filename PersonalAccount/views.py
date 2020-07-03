from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from Test.models import Test, UsersAnswers, Results, UserResultTestArchive
from Profile.models import Profile
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect


def reset_answers(request):
    user = auth.get_user(request)
    answers = UsersAnswers.objects.filter(user=user)
    for answer in answers:
        answer.delete()
    results = Results.objects.filter(user_id=user)
    for result in results:
        result.delete()
    user.profile.reset_tests()
    return redirect("all_tests")


def reset_answer(request, test_index):
    user = User.objects.get(username=auth.get_user(request).username)
    user.profile.reset_test(test_index)

    answers = UsersAnswers.objects.filter(user=user)
    for answer in answers:
        answer.delete()
    results = Results.objects.filter(user_id=user)
    for result in results:
        result.delete()

    return redirect("sinlge_test", test_index=test_index)


def activate_user(request, current_login="Login", activation_salt="yeap"):
    user = User.objects.get(username=current_login)
    salt = user.profile.activation_salt
    if salt == activation_salt:
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect("/")
    else:
        return render_to_response("AccountActivation.html")


def personal_account(request):
    user = User.objects.get(id=auth.get_user(request).id)
    profile = Profile.objects.get(user=user.id)
    return render_to_response('PersonalAccountExtension.html', {'user': user, 'profile': profile})


from Test.models import UserFinalResultArchive
from django.shortcuts import render


def personal_tests(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=auth.get_user(request).id)
        profile = Profile.objects.get(user=user.id)

        available_tests, passed_tests = profile.get_available_passed_tests()

        user_final_result_archive = UserFinalResultArchive.objects.filter(user=user).order_by('-whenWasCalculated')
        can_get_profs = False
        if user_final_result_archive.last():
            last_finished_test_date_prev = user_final_result_archive.first().lastFinishedTestDate
            last_finished_test_date_now = UserResultTestArchive.objects.all().last().whenWasFinished
            if last_finished_test_date_prev < last_finished_test_date_now:
                can_get_profs = True
        else:
            can_get_profs = True
    else:
        return render(request, 'HomeExtension.html', {'open_user_enter_popup': True})

    return render(request, 'PersonalTests.html', {'user': user,
                                                  'tests': Test.objects.all().order_by('test_lesson_number'),
                                                  'available_tests': available_tests,
                                                  'passed_tests': passed_tests,
                                                  'profs': user_final_result_archive,
                                                  'can_get_profs': can_get_profs
                                                  })


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

def profile_data(request):
    if request.user.is_authenticated:
        form_password = PasswordChangeForm(request.user)
        user = User.objects.get(id=auth.get_user(request).id)
        profile = Profile.objects.get(user=user.id)
        args = {
            'user': user,
            'profile': profile,
            'form_password': form_password
        }
    else:
        return render(request, 'HomeExtension.html', {'open_user_enter_popup': True})

    return render(request, 'ChangeData.html', args)


def change_profile_data(request):
    args = {}
    # args.update(csrf(request))

    if request.POST:
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        sex = request.POST.get("sex")
        date_of_birth = request.POST.get("date_of_birth")
        city_of_residence = request.POST.get("city_of_residence")
        country_of_residence = request.POST.get("country_of_residence")

        current_user = auth.get_user(request)
        current_profile = Profile.objects.get(user=current_user)
        current_profile.user.first_name = name
        current_profile.user.username = username
        current_profile.user.email = email
        current_profile.sex = sex
        current_profile.date_of_birth = date_of_birth
        current_profile.city_of_residence = city_of_residence
        current_profile.country_of_residence = country_of_residence
        current_profile.save_profile_n_user()
        auth.login(request, current_user)

        messages.success(request, '<span style="color:#28a745;margin: 0 0 1rem 0;">Основные данные успешно изменены!</span>', extra_tags='change_profile_data_messages')

        return redirect("personal_info")

    return render(request, 'ChangeData.html', args)


def delete_account(request):
    user = User.objects.get(id=auth.get_user(request).id)
    profile = Profile.objects.get(user=user.id)

    profile.delete_user()

    return redirect('home')
