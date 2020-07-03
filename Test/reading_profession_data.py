import re


def read_file():
    lines = []
    with open('./static/ResultsTexts/Lesson_5/professions_final.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if line != '\n':
                lines.append(line.strip().lower())
    return lines


def profession_list(lines):
    professions = []
    profession_pattern = '\d\. ([\w ]*)'
    for line in lines:
        profession = re.findall(profession_pattern, line)
        if len(profession) != 0:
            professions.append(profession[0].lower())
    return professions


def find_slice(lines, current_profession, next_profession):
    first_line = 0
    last_line = 0

    for index, line in enumerate(lines):
        if current_profession in line:
            first_line = index
            break

    for index, line in enumerate(lines):
        if next_profession in line and index > first_line:
            last_line = index
            break

    return lines[first_line + 1:last_line]


def collect_answers(test_slice):
    answers = []
    for line in test_slice:
        if line == 'не учитывается':
            line = "NTUD"

            continue  # for skills

        answers.append(line.lower())
    return answers

# for profs
# def answers_for_one_profession(line_slice, current_profession):
#     profession = {}
#     for test_number in range(1, 17):
#         current_test_index = 0
#         next_test_index = 0
#         if test_number != 11 and test_number != 12 and test_number != 16:
#             current_test = 'тест ' + str(test_number)
#             next_test = 'тест ' + str(test_number + 1)
#         if test_number == 11 or test_number == 12:
#             current_test = 'тест 11 и 12'
#             next_test = 'тест 13'
#         if test_number == 16:
#             current_test = 'тест 16'
#         key = "Test" + str(test_number)
#         for index, line in enumerate(line_slice):
#             if current_test in line:
#                 current_test_index = index
#             if next_test in line:
#                 next_test_index = index
#                 break
#         if test_number == 16:
#             next_test_index = current_test_index + 3
#         test_slice = line_slice[current_test_index + 1:next_test_index]
#
#         answers = collect_answers(test_slice)
#         profession.update({key: answers})
#     profession.update({'profession': current_profession})
#     return profession

# for skills
def answers_for_one_profession(line_slice, current_profession):
    profession = {}
    for test_number in range(1, 17):
        current_test_index = 0
        next_test_index = 0
        if test_number != 11 and test_number != 12 and test_number != 16:
            current_test = 'тест ' + str(test_number)
            next_test = 'тест ' + str(test_number + 1)
        if test_number == 11 or test_number == 12:
            current_test = 'тест 11 и 12'
            next_test = 'тест 13'
        if test_number == 16:
            current_test = 'тест 16'
        key = "Test" + str(test_number)
        for index, line in enumerate(line_slice):
            if current_test in line:
                current_test_index = index
            if next_test in line:
                next_test_index = index
                break
        if test_number == 16:
            next_test_index = current_test_index + 20#3
        test_slice = line_slice[current_test_index + 1:next_test_index]

        answers = collect_answers(test_slice)
        profession.update({current_profession: answers})
    # profession.update({'profession': current_profession})
    return profession

def collect_all_professions():
    lines = read_file()
    professions = profession_list(lines)
    all_professions = []
    for index in range(len(professions) - 1):
        line_slice = find_slice(lines, professions[index], professions[index + 1])
        _profession_answers = answers_for_one_profession(line_slice, professions[index])
        all_professions.append(_profession_answers)
    return all_professions


def profession_result(profession, num_of_tests):
    prof_answers = []
    for test_number in range(1, num_of_tests+1):
        key = "Test" + str(test_number)
        prof_answers.append(profession.get(key))
    prof_answers.append(profession.get('profession'))
    return prof_answers


def choose_appropriate_professions(result_list, prof_list):
    num_of_tests = len(result_list)
    appropriate_professions = []
    for prof in prof_list:
        appropriate_results = profession_result(prof, num_of_tests)
        points = 0

        appropriate_results_final = []
        for test_index, test_answer_list in enumerate(result_list):
            # print(test_answer_list.split(',')[0], len(test_answer_list.split(',')))

            test_answer_list = test_answer_list.split(',')
            for result_index, test_answer in enumerate(test_answer_list):
                # print(test_answer)
                # print()
                # print(test_index)
                try:  # in case 'profession': 'smth' and not results
                    if appropriate_results[test_index][0] == 'ntud':  # if result of a test doesn't matter
                        points += 1
                        break
                    else:
                        if test_answer.lower() in appropriate_results[test_index]:
                            points += 1
                            # appropriate_results_final.append(test_answer.lower())
                            # print(test_answer.lower(), test_index+1, appropriate_results[num_of_tests], points)
                            if test_index == 1:
                                temperament_result = test_answer_list[0]

                                try:
                                    temperament_result += ", " + str(test_answer_list[1])[0].capitalize() + str(test_answer_list[1])[1:]
                                except:
                                    pass

                                try:
                                    temperament_result += ", " + str(test_answer_list[2])[0].capitalize() + str(test_answer_list[2])[1:]
                                except:
                                    pass

                                try:
                                    temperament_result += ", " + str(test_answer_list[3])[0].capitalize() + str(test_answer_list[3])[1:]
                                except:
                                    pass

                                appropriate_results_final.append(temperament_result)
                            else:
                                appropriate_results_final.append(test_answer.lower())
                            break

                except:
                    break

        if points == num_of_tests:
            inner_list = []
            inner_list.append(appropriate_results[num_of_tests])
            inner_list.append(appropriate_results_final)
            appropriate_professions.append(inner_list)
            # print(points, num_of_tests)

    return appropriate_professions


def get_skills_list(skill_list, appropriate_professions):
    for skill in skill_list:
        print(skill)

    return 0
