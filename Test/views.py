# from datetime import datetime, timedelta, timezone
import pytz
from django.utils import timezone

from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render, redirect

from Pages.models import HelpFunctions
from Profile.models import Profile
from Test import results_analisers as analise
from Test.models import Test, UsersAnswers, Hint, Results, UserResultTestArchive


def all_tests(request):
    return render_to_response('PersonalAccountExtension.html', {'tests': Test.objects.all(),
                                                                'user': User.objects.get(
                                                                    username=auth.get_user(request).username)})


def single_test(request, test_index="1"):
    if request.user.is_authenticated:
        finished = 0
        help_func = HelpFunctions()
        current_user = User.objects.get(username=auth.get_user(request).username)
        profile = Profile.objects.get(user=current_user.id)
        finished_tests = profile.get_integer_finished_tests()
        if int(test_index) in finished_tests:
            finished = 1
        current_test = Test.objects.get(test_lesson_number=test_index)
        questions_with_answer = list(current_test.questionwithanswer_set.values())
        questions_with_variants = list(current_test.questionwithvariants_set.values())
        questions_type = [questions_with_answer, questions_with_variants]

        if request.POST:
            for question_type in questions_type:
                for question in range(len(question_type)):
                    current_question = question_type[question]
                    question_id = current_question.get("id")
                    question_is_radio = current_question.get("question_with_one_answer")
                    if question_is_radio:
                        answer = request.POST.get(str(question_id))
                    else:
                        answer = ",".join(request.POST.getlist(str(question_id)))
                    answer_model = UsersAnswers(user=User.objects.get(id=current_user.id),
                                                test=Test.objects.get(test_lesson_number=test_index),
                                                question_id=question_id,
                                                question_text=current_question.get("question_text"),
                                                user_answer=answer)
                    answer_model.save()

            return redirect("save_test_result", test_index=str(test_index))

        else:
            # *********** Вопросы с ответами ************
            for question in range(len(questions_with_answer)):  # проходимся по всем вопросам с ответами
                recognized_words = []  # список для слов, нуждающихся в уточнении
                hint_text = ""  # текст подсказки
                current_question = questions_with_answer[question]  # получаем текущий вопрос
                recognized_words += help_func.is_hint_need(current_question.get("question_text"))
                recognized_words = list(set(recognized_words))  # убираем повторные слова
                for word in recognized_words:  # проходимся по всем словам, нуждающимся в уточнении
                    current_hint = Hint.objects.get(defined_word=word)
                    hint_text += current_hint.defined_word + ": " + current_hint.hint + "***"  # формируем текст подсказки

                current_question.update({'hint': hint_text})  # дополняем словарь с параметрами вопроса подсказкой

            # *************  Вопросы с вариантами ответов ****************
            for question in range(len(questions_with_variants)):
                recognized_words = []
                hint_text = ""
                current_question = questions_with_variants[question]
                line_with_answers = current_question.get("question_variants")
                answers = [variant.strip() for variant in line_with_answers.split(';')]
                current_question.update({"question_variants": answers})
                recognized_words = list(set(recognized_words))

                hints = Hint.objects.all()
                defined_words = [hint.defined_word for hint in hints]

                hint_text = []
                for variant in current_question['question_variants']:
                    if variant.lower() in defined_words:
                        # print(variant.lower() + '/n ++')
                        current_hint = Hint.objects.get(defined_word=variant.lower())
                        if current_test.test_lesson_number != 15:
                            hint_text.append(current_hint.defined_word + ": " + current_hint.hint)
                        else:
                            hint_text.append(current_hint.hint)
                    else:
                        hint_text.append('')

                        # print("************\n", current_question, "\n************")
                current_question.update({'hint': hint_text})

                current_question['question_variants'] = zip(current_question['question_variants'], current_question['hint'])

    else:
        return render(request, 'HomeExtension.html', {'open_user_enter_popup': True})

    return render(request, 'SingleTestExtension.html', {'test': current_test,
                                                        'questions_with_answer': questions_with_answer,
                                                        'questions_with_variants': questions_with_variants,
                                                        'user': current_user,
                                                        'finished': finished,
                                                        'tests_with_imgs': [8, 9, 10]})


def save_test_result(request, test_index="1"):
    current_user = User.objects.get(username=auth.get_user(request).username)
    current_test = Test.objects.get(test_lesson_number=test_index)
    current_user.profile.add_finished_test(current_test.id)
    current_user.save()

    functions_for_analise = {1: analise.analise_results_test_1,
                             2: analise.analise_results_test_2,
                             3: analise.analise_results_test_3,
                             4: analise.analise_results_test_4,
                             5: analise.analise_results_test_5,
                             6: analise.analise_results_test_6,
                             7: analise.analise_results_test_7,
                             8: analise.analise_results_test_8,
                             9: analise.analise_results_test_9,
                             10: analise.analise_results_test_10,
                             11: analise.analise_results_test_11,
                             12: analise.analise_results_test_12,
                             13: analise.analise_results_test_13,
                             14: analise.analise_results_test_14,
                             15: analise.analise_results_test_15, }

    result = functions_for_analise.get(current_test.test_lesson_number)(current_user.id, current_test.id)

    if request.POST:

        results = UserResultTestArchive.objects.filter(user=auth.get_user(request), test=current_test.id).order_by(
            '-whenWasFinished')

        if results.first():
            days_till_reset_test_allowed = results.first().whenWasFinished + timezone.timedelta(
                seconds=30) - timezone.now()
            if days_till_reset_test_allowed > timezone.timedelta(seconds=0):
                days_till_reset_test_allowed = False
            else:
                days_till_reset_test_allowed = True

        if not results.first() or days_till_reset_test_allowed:
            results = request.POST.get('result')
            result_description = request.POST.get('result_description')
            print(result_description)
            when_was_finished = timezone.now()
            user_result_test_archive_model, user_result_test_archive_created = UserResultTestArchive.objects.get_or_create(
                user=auth.get_user(request),
                test=current_test,
                result=results,
                result_description=result_description,
                whenWasFinished=when_was_finished)

        # results_another = request.POST.get('result')
        # test_number = request.POST.get('test_number')
        # tests_dict = {"1": "first_test_result", "2": "second_test_result", "3": "third_test_result",
        #               "4": "fourth_test_result", "5": "fifth_test_result", "6": "six_test_result",
        #               "7": "seventh_test_result", "8": "eighth_test_result", "9": "ninth_test_result",
        #               "10": "tenth_test_result", "11": "eleventh_test_result", "12": "twelfth_test_result",
        #               "13": "thirteenth_test_result", "14": "fourteenth_test_result", "15": "fifteenth_test_result"}
        # result_model, created = Results.objects.get_or_create(user_id=auth.get_user(request), test_id=current_test)
        # model_code = "result_model." + tests_dict.get(str(test_number)) + "=\"" + results_another + "\""
        # exec(model_code)
        # result_model.save()

        return render(request, "TestResults.html",
                      {"test": current_test, "user": current_user, "result": result,
                       "lesson_number": current_test.test_lesson_number})

    return render(request, "TestResults.html",
                  {"test": current_test, "user": current_user, "result": result,
                   "lesson_number": current_test.test_lesson_number})


def test_results(request, current_login="MissLog", current_test_id="1"):
    current_user = User.objects.get(username=current_login)
    current_test = Test.objects.get(id=current_test_id)
    current_user.profile.add_finished_test(current_test.id)
    current_user.save()

    functions_for_analise = {1: analise.analise_results_test_1,
                             2: analise.analise_results_test_2,
                             3: analise.analise_results_test_3,
                             4: analise.analise_results_test_4,
                             5: analise.analise_results_test_5,
                             6: analise.analise_results_test_6,
                             7: analise.analise_results_test_7,
                             8: analise.analise_results_test_8,
                             9: analise.analise_results_test_9,
                             10: analise.analise_results_test_10,
                             11: analise.analise_results_test_11,
                             12: analise.analise_results_test_12,
                             13: analise.analise_results_test_13,
                             14: analise.analise_results_test_14,
                             15: analise.analise_results_test_15, }

    result = functions_for_analise.get(current_test.test_lesson_number)(current_user.id, current_test_id)

    if request.POST:
        results = request.POST.get('result')
        test_number = request.POST.get('test_number')
        tests_dict = {"1": "first_test_result", "2": "second_test_result", "3": "third_test_result",
                      "4": "fourth_test_result", "5": "fifth_test_result", "6": "six_test_result",
                      "7": "seventh_test_result", "8": "eighth_test_result", "9": "ninth_test_result",
                      "10": "tenth_test_result", "11": "eleventh_test_result", "12": "twelfth_test_result",
                      "13": "thirteenth_test_result", "14": "fourteenth_test_result", "15": "fifteenth_test_result"}

        result_model, created = Results.objects.get_or_create(user_id=auth.get_user(request), test_id=current_test)
        model_code = "result_model." + tests_dict.get(str(test_number)) + "=\"" + results + "\""
        exec(model_code)
        result_model.save()

        # result_description = request.POST.get('result_description')
        # print(result_description)
        # when_was_finished = datetime.now()
        # user_result_test_archive_model, user_result_test_archive_created = UserResultTestArchive.objects.get_or_create(
        #     user=auth.get_user(request),
        #     test=current_test,
        #     result=results,
        #     result_description=result_description,
        #     whenWasFinished=when_was_finished)

        return render_to_response("TestResults.html", {"test": current_test, "user": current_user, "result": result,
                                                       "lesson_number": current_test.test_lesson_number})
    else:
        return render_to_response("TestResults.html", {"test": current_test, "user": current_user, "result": result,
                                                       "lesson_number": current_test.test_lesson_number})


def final_result(request, current_login="MissLog", current_test_id="1"):
    current_user = User.objects.get(username=current_login)
    current_test = Test.objects.get(id=current_test_id)
    appropriate_professions = final_result(current_user.id, current_test.id)
    return render_to_response("FinalResults.html", {"professions": appropriate_professions})


def test_results_all(request, test_index="1"):
    current_user = User.objects.get(username=auth.get_user(request).username)
    current_test = Test.objects.get(test_lesson_number=test_index)

    results = UserResultTestArchive.objects.filter(user=auth.get_user(request), test=current_test).order_by(
        '-whenWasFinished')

    days_till_reset_test_allowed = "Reload page"

    if results:
        days_till_reset_test_allowed = results.first().whenWasFinished + timezone.timedelta(seconds=30) - timezone.now()

        if days_till_reset_test_allowed < timezone.timedelta(seconds=0):
            days_till_reset_test_allowed = None

    context = {
        "test": current_test,
        "test_id": test_index,
        "lesson_number": current_test.test_lesson_number,
        "days_till_reset_test_allowed": days_till_reset_test_allowed,
        "results": results
    }

    return render(request, "TestResultsAll.html", context)


from django.http import HttpResponse
from .models import Test
from .reading_profession_data import *
from .results_analisers import *
from .dummyproflist import *
from .dummyskilllist import *
from Test.models import UserFinalResultArchive
from django.utils import timezone


def get_final_result(request):
    result_list = []
    for test_number in list(Test.objects.all().order_by('test_lesson_number').values_list('test_lesson_number')):
        test_number = test_number[0]
        obj = UserResultTestArchive.objects.filter(user=auth.get_user(request),
                                                   test__test_lesson_number=test_number).last()
        result = getattr(obj, 'result')
        result_list.append(result)

    print(result_list)
    profs = choose_appropriate_professions(result_list, prof_list)
    print(profs)

    html_content = ''
    for skill in skill_list:
        key = list(skill.keys())[0]
        value_list = list(skill.values())[0]

        for prof_0 in profs:
            if key == prof_0[0]:
                html_content += '<div class="accordion">'
                html_content += '<div class="accordion__title">' + str(
                    prof_0[0].capitalize()) + '<i class="accordion__icon fas fa-caret-down"></i></div>'
                html_content += '<div class="accordion__content">'
                html_content += '<p class="mb-025">На основе пройденных тестов.</p>'
                html_content += '<ul>'
                for prof_1 in prof_0[1]:
                    html_content += "<li>" + str(prof_1.capitalize()) + "</li>"
                html_content += '</ul>'

                html_content += "<p class='mb-025'>Ниже перечисленные навыки мы не можем проверить тестами. Поэтому Вам нужно самостоятельно или с помощью родителей; близких друзей  понять, развиты эти навыки или нет.</p>"

                html_content += '<ul>'
                for skill in value_list:
                    html_content += "<li>" + str(skill[0].capitalize()) + str(skill[1:]) + "</li>"
                html_content += '</ul>'
                html_content += "</div>"
                html_content += "</div>"

    if len(profs) == 0:
        html_content += '<p class="final-result__no-profs-text">К сожалению, на данный момент Ваши способности слабо развиты. Поработайте над их улучшением и возвращайтесь заново подобрать профессию.</p>'

    UserFinalResultArchive.objects.create(
        user=auth.get_user(request),
        final_result_description=html_content,
        lastFinishedTestDate=getattr(UserResultTestArchive.objects.filter(user=auth.get_user(request)).last(), 'whenWasFinished'),
        whenWasCalculated=timezone.now()
    )

    return redirect('final_result')


def final_result_page(request):
    user = User.objects.get(username=auth.get_user(request).username)
    profile = Profile.objects.get(user=user)

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

    return render(request, 'FinalResults.html', {'user': user,
                                                  'available_tests': available_tests,
                                                  'passed_tests': passed_tests,
                                                  'profs': user_final_result_archive,
                                                  'can_get_profs': can_get_profs
                                                  })
