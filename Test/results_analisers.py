from Test.models import Test, UsersAnswers, Results
from django.contrib.auth.models import User
from Test import reading_profession_data as rpd


def analise_results_test_1(user_id, current_test_id):
    return 0


def analise_results_test_2(user_id, current_test_id):
    lying_points = 0
    extra_intro_points = 0
    neuro_points = 0
    lying_yes = [6, 24, 36]
    lying_no = [12, 18, 30, 42, 48, 54]
    extra_intro_yes = [1, 3, 8, 10, 13, 17, 22, 25, 27, 39, 44, 46, 49, 53, 56]
    extra_intro_no = [5, 15, 20, 29, 32, 34, 37, 41, 51]
    neuroticism = [2, 4, 7, 9, 11, 14, 16, 19, 21, 23, 26, 28, 31, 33, 35, 38, 40, 43, 45, 47, 50, 52, 55, 57]
    answers = [answer.user_answer for answer in list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    print(answers)

    for i, value in enumerate(answers):
        true_index = i + 1
        if value != None:
            value = value.lower()
        else:
            pass
        if value == 'да' and true_index in extra_intro_yes: extra_intro_points += 1
        if value == 'нет' and true_index in extra_intro_no: extra_intro_points += 1
        if value == 'да' and true_index in lying_yes: lying_points += 1
        if value == 'нет' and true_index in lying_no: lying_points += 1
        if value == 'да' and true_index in neuroticism: neuro_points += 1
    points = {"extra_intro": extra_intro_points, "lying": lying_points, "neuroticism": neuro_points}

    return points


def analise_results_test_3(user_id, current_test_id):
    physical_agression_yes = [1, 25, 33, 48, 55, 62, 68]
    physical_agression_no = [9, 17, 41, 10]
    indirect_aggression_yes = [2, 18, 34, 42, 56, 63]
    indirect_aggression_no = [10, 26, 49, 9]
    irritation_yes = [3, 19, 27, 43, 50, 57, 64, 72]
    irritation_no = [11, 35, 69]
    negativism_yes = [4, 12, 20, 23, 36, 5]
    offense_yes = [5, 13, 21, 29, 37, 51, 58]
    offense_no = [44, 8]
    suspicion_yes = [6, 14, 22, 30, 38, 45, 52, 59]
    suspicion_no = [65, 70, 10]
    verbal_aggression_yes = [7, 15, 23, 31, 46, 53, 60, 71, 73]
    verbal_aggression_no = [39, 66, 74, 75, 18]
    remorse_conscience_yes = [8, 16, 24, 32, 40, 47, 54, 61, 67]
    physical_aggression_points = 0
    indirect_aggression_points = 0
    irritation_points = 0
    negativism_points = 0
    offense_points = 0
    suspicion_points = 0
    verbal_aggression_points = 0
    remorse_conscience_points = 0

    answers = [answer.user_answer for answer in list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]
    print(answers)

    for i, value in enumerate(answers):
        true_index = i + 1
        if value != None:
            value = value.lower()
        else:
            pass
        if value == 'да' and true_index in physical_agression_yes: physical_aggression_points += 1
        if value == 'нет' and true_index in physical_agression_no: physical_aggression_points += 1
        if value == 'да' and true_index in indirect_aggression_yes: indirect_aggression_points += 1
        if value == 'нет' and true_index in indirect_aggression_no: indirect_aggression_points += 1
        if value == 'да' and true_index in irritation_yes: irritation_points += 1
        if value == 'нет' and true_index in irritation_no: irritation_points += 1
        if value == 'да' and true_index in negativism_yes: negativism_points += 1
        if value == 'да' and true_index in offense_yes: offense_points += 1
        if value == 'нет' and true_index in offense_no: offense_points += 1
        if value == 'да' and true_index in suspicion_yes: suspicion_points += 1
        if value == 'нет' and true_index in suspicion_no: suspicion_points += 1
        if value == 'да' and true_index in verbal_aggression_yes: verbal_aggression_points += 1
        if value == 'нет' and true_index in verbal_aggression_no: verbal_aggression_points += 1
        if value == 'да' and true_index in remorse_conscience_yes: remorse_conscience_points += 1

    percents = {"physical_aggression": str(format('%.2f' % (physical_aggression_points / \
                                       sum(map(len, [physical_agression_no, physical_agression_yes])) * 100))) + "%",
                "indirect_aggression": str(format('%.2f' % (indirect_aggression_points / \
                                       sum(map(len, [indirect_aggression_yes, indirect_aggression_no])) * 100))) + "%",
                "irritation": str(format('%.2f' % (irritation_points / \
                                       sum(map(len, [irritation_yes, irritation_no])) * 100))) + "%",
                "negativism": str(format('%.2f' % (negativism_points / len(negativism_yes) * 100))) + "%",
                "offence": str(format('%.2f' % (offense_points / \
                                       sum(map(len, [offense_yes, offense_no])) * 100))) + "%",
                "suspicion": str(format('%.2f' % (suspicion_points / \
                                       sum(map(len, [suspicion_yes, suspicion_no])) * 100))) + "%",
                "verbal_aggression": str(format('%.2f' % (verbal_aggression_points / \
                                       sum(map(len, [verbal_aggression_yes, verbal_aggression_no]))* 100))) + "%",
                "remorse_conscience": str(format('%.2f' % (remorse_conscience_points / \
                                                           len(remorse_conscience_yes) * 100))) + "%"
                }

    return percents


def analise_results_test_4(user_id, current_test_id):
    P_D = [1, 6, 11, 16, 21, 26, 31, 36]
    A_C = [2, 7, 12, 17, 22, 27, 32, 37]
    C_L = [3, 8, 13, 18, 23, 28, 33, 38]
    H_O = [4, 9, 14, 19, 24, 29, 34, 39]
    K = [5, 10, 15, 20, 25, 30, 35, 40]
    P_D_points = 0
    A_C_points = 0
    C_L_points = 0
    H_O_points = 0
    K_points = 0

    answers = [answer.user_answer for answer in
               list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    for i, value in enumerate(answers):
        true_index = i + 1
        if value != None:
            value = value.lower()
        else:
            pass
        if value == 'да' and true_index in P_D: P_D_points += 1
        if value == 'да' and true_index in A_C: A_C_points += 1
        if value == 'да' and true_index in C_L: C_L_points += 1
        if value == 'да' and true_index in H_O: H_O_points += 1
        if value == 'да' and true_index in K: K_points += 1

    results = {"P_D": P_D_points,
               "A_C": A_C_points,
               "C_L": C_L_points,
               "H_O": H_O_points,
               "K": K_points}
    return results


def analise_results_test_5(user_id, current_test_id):
    profession_A = ['кинооператор', 'дизайнер компьютерных программ', 'дрессировщик', 'ландшафтный дизайнер',
                    'режиссер театра и кино', 'хореограф', 'музыкант', 'актер театра и кино', 'художественный редактор', 'литературный переводчик']
    profession_P = ['логистик', 'менеджер по продажам', 'фермер', 'заготовитель сельхозпродуктов', 'предприниматель',
                    'торговый агент', 'продюсер', 'арт-директор', 'антикризисный управляющий', 'брокер']
    profession_O = ['оператор связи', 'диспетчер', 'лаборант', 'микробиолог', 'администратор', 'страховой агент',
                    'редактор', 'музейный работник', 'корректор', 'бухгалтер']
    profession_I =  ['специалист по защите информации', 'инженер-конструктор', 'биолог-исследователь', 'селекционер', 'преподаватель',
                     'психолог', 'искусствовед', 'композитор', 'лингвист', 'программист']
    profession_C = ['физиотерапевт', 'продавец', 'эколог', 'санитарный врач', 'воспитатель', 'врач', 'журналист', 'экскурсовод',
                    'гид-переводчик', 'юрисконсульт']
    profession_R = ['автомеханик', 'водитель', 'ветеринар', 'агроном', 'массажист', 'официант', 'ювелир-гравер', 'дизайнер интерьера',
                    'верстальщик', 'наборщик текстов']
    points_A = 0
    points_P = 0
    points_O = 0
    points_I = 0
    points_C = 0
    points_R = 0

    answers = [answer.user_answer for answer in
               list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    for answer in answers:
        if answer != None:
            if answer.lower() in profession_A: points_A += 1
            if answer.lower() in profession_P: points_P += 1
            if answer.lower() in profession_O: points_O += 1
            if answer.lower() in profession_I: points_I += 1
            if answer.lower() in profession_C: points_C += 1
            if answer.lower() in profession_R: points_R += 1

    return {"A":points_A, "P":points_P, "O":points_O, "I":points_I, "C":points_C, "R":points_R}


def analise_results_test_6(user_id, current_test_id):
    right_answers = ['а', 'б', 'г', 'в', 'б', 'а', 'б', 'в',
                     'г', 'а', 'в', 'г', 'г', 'в',
                     'а', 'б', 'г', 'а', 'г', 'в', 'б', 'б',
                     'в', 'в', 'в', 'б', 'г', 'а', 'а', 'г',
                     'а',  'г', 'в', 'а', 'в', 'г', 'а', 'б',
                     'г', 'а', 'в', 'в']
    points = 0
    answers = [answer.user_answer for answer in
               list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    print(answers)

    for i, value in enumerate(answers):
        if 'а) ' in value or 'a)' in value:
            value = 'а'
        if 'б) ' in value or 'b)' in value:
            value = 'б'
        if 'в) ' in value or 'c)' in value:
            value = 'в'
        if 'г) ' in value or 'd)' in value:
            value = 'г'
        if 'д) ' in value:
            value = 'д'

        print(right_answers[i].lower(), value, right_answers[i].lower() == value)

        if value != None and value.lower() == right_answers[i].lower(): points += 1

    results = {"percentage": round(points / len(right_answers) * 100)}
    return results


def analise_results_test_7(user_id, current_test_id):
    right_answers = ['б', 'в', 'г', 'г', 'в', 'в', 'а', 'б', 'г', 'в', 'б',
                     'а', 'г', 'б', 'а', 'б', 'г', 'г', 'в', 'г', 'б']
    points = 0
    answers = [answer.user_answer for answer in
               list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    for i, value in enumerate(answers):
        if 'а' in value:
            value = 'а'
        if 'б' in value:
            value = 'б'
        if 'в' in value:
            value = 'в'
        if 'г' in value:
            value = 'г'

        print(right_answers[i].lower(), value, right_answers[i].lower() == value)

        if value != None and value.lower() == right_answers[i].lower(): points += 1

    results = {"percentage": round(points / len(right_answers) * 100)}
    return results


def analise_results_test_8(user_id, current_test_id):
    right_answers = ['а', 'в', 'в', 'а', 'а', 'в', 'б', 'г', 'в', 'б', 'а', 'в', 'г', 'б', 'а', 'г',#16
                     'г', 'г', 'в', 'б', 'г', 'а', 'г', 'в', 'б', 'б', 'в', 'г', 'а', #29
                     'в', 'а', 'г', 'а', 'г', 'б']

    points = 0
    answers = [answer.user_answer for answer in
               list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    for i, value in enumerate(answers):
        if 'а' in value:
            value = 'а'
        if 'б' in value:
            value = 'б'
        if 'в' in value:
            value = 'в'
        if 'г' in value:
            value = 'г'

        print(right_answers[i].lower(), value, right_answers[i].lower() == value)

        if value != None and value.lower() == right_answers[i].lower(): points += 1

    results = {"percentage": round(points / len(right_answers) * 100)}
    return results


def analise_results_test_9(user_id, current_test_id):
    right_answers = [['нет', 'нет', 'да', 'да'], ['да', 'да', 'нет', 'нет'], ['да', 'нет', 'да',
                     'нет'], ['нет', 'да', 'нет', 'нет'], ['да', 'да', 'да', 'да'], ['да', 'да',
                     'нет'], ['нет', 'да', 'нет', 'да'], ['нет', 'нет', 'да', 'нет'], ['нет', 'да',
                     'нет', 'нет'], ['да', 'нет', 'нет', 'да'], ['да', 'нет', 'нет', 'да'], ['да',
                     'нет', 'нет', 'да'], ['нет', 'да', 'нет', 'нет'], ['нет', 'нет', 'нет', 'да'],
                     ['нет', 'да', 'да', 'нет'], ['нет', 'нет', 'нет', 'да'], ['да', 'да', 'да',
                     'нет'], ['да', 'да', 'нет', 'нет'], ['нет', 'да', 'нет', 'нет']]
    right_answers_count = sum(len(answer) for answer in right_answers)

    points = 0
    answers = [answer.user_answer for answer in
               list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    print(answers)
    for i, answer in enumerate(answers):
        for k, value in enumerate(answer.split(',')):
            if value != None and value.lower() == right_answers[i][k].lower(): points += 1

    results = {"percentage": round(points / right_answers_count * 100)}
    return results


def analise_results_test_10(user_id, current_test_id):
    right_answers = ['в', 'б', 'в', 'б', 'б', 'в', 'а', 'а', 'а', 'г', 'в', 'в', 'б', 'а', 'в', 'б',
                     'а', 'а', 'а', 'б', 'в', 'а', 'а', 'б', 'в', 'г', 'в', 'б', 'а', 'б', 'г', 'б', 'в']
    points = 0
    answers = [answer.user_answer for answer in
               list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    print(right_answers)

    for i, value in enumerate(answers):
        if 'а) ' in value or 'a)' in value:
            value = 'а'
        if 'б) ' in value or 'b)' in value:
            value = 'б'
        if 'в) ' in value or 'c)' in value:
            value = 'в'
        if 'г) ' in value or 'd)' in value:
            value = 'г'
        if 'д) ' in value:
            value = 'д'

        print(value)

        if value != None and value.lower() == right_answers[i].lower(): points += 1

    results = {"percentage": round(points / len(right_answers) * 100)}
    return results


def analise_results_test_11(user_id, current_test_id):
    right_answers = ['29', '80', '104', '107', '57', '156', '120', '392', '183', '35', '29', '315', '52',
                     '871', '123', '79', '235', '91', '73', '5277', '1720', '99', '333', '121', '388',
                     '225', '124', '106', '192', '758', '90', '96', '79', '473', '588',
                     'в', 'в', 'а', 'б', 'а', 'в', 'б', 'а', 'б', 'а', 'б', 'в', 'а', 'б', 'в', 'а', 'в', 'а', 'а', 'б',
                     'а', 'а', 'в', 'б', 'б', 'б', 'а', 'а', 'б', 'в', 'б', 'а', 'в', 'б', 'б', 'а', 'в', 'в', 'в', 'в',
                     'а', 'в', 'б', 'а', 'б', 'в', 'а', 'б', 'а', 'б', 'б', 'в', 'а', 'а', 'а', 'б', 'а', 'в', 'а', 'в',
                     'а', 'в', 'а', 'в', 'б', 'б', 'б', 'в', 'в', 'б']

    points = 0
    answers = [answer.user_answer for answer in
               list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    print(answers)

    for i, value in enumerate(answers):
        if value is None:
            continue

        if 'а)' in value:
            value = 'а'
        if 'б)' in value:
            value = 'б'
        if 'в)' in value:
            value = 'в'

        if value != None and value.lower() == right_answers[i].lower(): points += 1

        print(i, value, points)

    results = {"percentage": round(points / len(right_answers) * 100)}
    return results


def analise_results_test_12(user_id, current_test_id):
    right_answers = [['в'], ['а'], ['г'], ['б', 'г'], ['в', 'г'], ['г'], ['б'], ['г'], ['а'],
                     ['б', 'г'], ['б'], ['г'], ['г'], ['г'], ['б'], ['в'], ['а'],
                     ['б'], ['б', 'г'], ['а', 'в'], ['б'], ['а', 'в'], ['г'], ['д'],
                     ['д'], ['а'], ['е'], ['а'], ['в'], ['в'], ['б']]
    points = 0
    answers = [answer.user_answer for answer in
               list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    for i, answer in enumerate(answers):
        if answer is None:
            continue
        print(answer)
        answer_split = answer.split('.,')
        for k, value in enumerate(answer_split):
            print(value)

            if 'а)' in value:
                answer_split[k] = value = 'а'
            elif 'б)' in value:
                answer_split[k] = value = 'б'
            elif 'в)' in value:
                answer_split[k] = value = 'в'
            elif 'г)' in value:
                answer_split[k] = value = 'г'
            elif 'д)' in value:
                answer_split[k] = value = 'д'
            elif 'е)' in value:
                answer_split[k] = value = 'е'
            elif 'ё)' in value:
                answer_split[k] = value = 'ё'
            elif 'ж)' in value:
                answer_split[k] = value = 'ж'
            elif 'з)' in value:
                answer_split[k] = value = 'з'
            else:
                pass

            try:
                right_answer = right_answers[i][k]
            except IndexError:
                pass


            if value != None and value == right_answer: points += 1

            if k != 0:
                if (answer_split[0] == right_answers[i][0] and answer_split[1] != right_answers[i][1]) or (answer_split[0] != right_answers[i][0] and answer_split[1] == right_answers[i][1]) or (answer_split[0] == right_answers[i][0] and answer_split[1] == right_answers[i][1]):
                    points -= 1
                print("//", answer_split[0], right_answers[i][0], answer_split[1], right_answers[i][1])

            print(i, k, value, right_answer, value == right_answer, points)
            print('')

    results = {"percentage": round(points / len(right_answers) * 100)}
    return results


def analise_results_test_13(user_id, current_test_id):
    nature = [4, 7, 11, 18, 25, 28]
    technique = [2, 9, 13, 16, 21, 26]
    sign = [5, 8, 14, 19, 22, 29]
    creation = [3, 10, 12, 17, 24, 30]
    person = [1, 6, 15, 20, 23, 27]
    double_points = [9, 10, 14, 15, 16, 17, 18, 19, 23, 25]
    nature_points = 0
    technique_points = 0
    sign_points = 0
    creation_points = 0
    person_points = 0

    answers = [answer.user_answer for answer in
               list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    print(answers)

    for i, value in enumerate(answers, start=1):
        if value is None:
            pass
        if i in double_points:
            point = 2
        else:
            point = 1

        if value == 'да' and i in nature: nature_points += point
        if value == 'да' and i in technique: technique_points += point
        if value == 'да' and i in sign: sign_points += point
        if value == 'да' and i in creation: creation_points += point
        if value == 'да' and i in person: person_points += point
        if value == 'нет' and i in nature: nature_points -= point
        if value == 'нет' and i in technique: technique_points -= point
        if value == 'нет' and i in sign: sign_points -= point
        if value == 'нет' and i in creation: creation_points -= point
        if value == 'нет' and i in person: person_points -= point

    results = {"nature": str(nature_points),
               "technique": str(technique_points),
               "signs": str(sign_points),
               "creation": str(creation_points),
               "person": str(person_points)}

    return results


def analise_results_test_14(user_id, current_test_id):
    right_answers = ['число', 'хор', 'камень', 'стол', 'кино', 'зонт', 'море', 'шмель', 'лампа', 'рысь']
    answers = [answer.user_answer for answer in
               list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    marks = []
    wrong_marks = []

    for value in answers:
        used_words = []
        mark = 0
        wrong_mark = 0
        words = value.split(",")
        for word in words:
            word = word.replace(" ", "")
            print(word)
            if word != '' and word.lower() in right_answers and word.lower() not in used_words:
                used_words.append(word)
                mark += 1
            if word != '' and word.lower() not in right_answers:
                wrong_mark += 1
        marks.append(mark)
        wrong_marks.append(wrong_mark)

    print(answers)
    print(marks, wrong_marks)

    results = {"marks": marks, "wrong_marks": wrong_marks}
    return results


def analise_results_test_15(user_id, current_test_id):
    answers_yes = [1, 2, 4, 5, 7, 10, 11, 12, 15, 20, 21, 23, 24, 26, 27, 32, 34, 37, 39, 41, 42, 43, 44, 46, 48]
    answers_no = [3, 6, 8, 9, 13, 14, 16, 17, 18, 19, 22, 25, 28, 29, 30, 31, 33, 35, 36, 38, 40, 45, 47, 49, 50]
    points = 0
    answers = [answer.user_answer for answer in
               list(UsersAnswers.objects.filter(user_id=user_id, test=current_test_id))]

    for i, value in enumerate(answers):
        true_index = i + 1
        if value == 'да' and true_index in answers_yes: points += 1
        if value == 'нет' and true_index in answers_no: points += 1
    results = {'points': points}
    return results


def analise_final_results(user_id, current_test_id):
    all_professions = rpd.collect_all_professions()
    user_answers = [answer.user_answer for answer in
                    list(Results.objects.filter(user_id=user_id, test=current_test_id))]

    return rpd.choose_appropriate_professions(user_answers, all_professions)