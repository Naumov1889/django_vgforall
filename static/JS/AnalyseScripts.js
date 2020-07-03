function getCookie(c_name) {
    if (document.cookie.length > 0) {
        let c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            let c_end = document.cookie.indexOf(";", c_start);
            if (c_end === -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}


function send_result(result, test_number, result_description = "None") {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', location.href, true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));

    if (xhr.readyState === 4) {
        if (xhr.status === 200) {
            console.log("Status 200");
        } else {
            console.log("Error");
        }
    }

    let body = new FormData();
    body.append('result', result.toLowerCase());
    body.append('result_description', result_description);
    body.append('test_number', test_number);
    xhr.send(body);
    console.log(body);

    setTimeout(function(){
        window.location.replace(document.querySelector("#redirect-url").innerText) }, 1500);

}


function readTextFile(filename) {
    let file = "/static/" + filename;
    let text = "";
    let rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function () {
        if (rawFile.readyState === 4) {
            if (rawFile.status === 200 || rawFile.status === 0) {
                text = rawFile.responseText;
            }
        }
    };
    rawFile.send(null);
    return text;
}


function results_test_1(args, test_number) {
    let final_content = readTextFile('ResultsTexts/Lesson_1/Lesson_1.txt');
    document.getElementById("result_field").innerHTML = final_content;

    send_result("test 1 is passed", test_number, final_content);
}


function results_test_2(args, test_number) {
    let extra_intro_1_9 = "<p>" + readTextFile("ResultsTexts/Lesson_2/Extra_Intro_1_9.txt") + "</p>";
    let extra_intro_10_14 = "<p>" + readTextFile("ResultsTexts/Lesson_2/Extra_Intro_10_14.txt") + "</p>";
    let extra_intro_15_24 = "<p>" + readTextFile("ResultsTexts/Lesson_2/Extra_Intro_15_24.txt") + "</p>";
    let neuroticism_1_9 = "<p>" + readTextFile("ResultsTexts/Lesson_2/Neuroticism_1_9.txt") + "</p>";
    let neuroticism_10_14 = "<p>" + readTextFile("ResultsTexts/Lesson_2/Neuroticism_10_14.txt") + "</p>";
    let neuroticism_15_24 = "<p>" + readTextFile("ResultsTexts/Lesson_2/Neuroticism_15_24.txt") + "</p>";
    let Choleric = "<p>" + readTextFile("ResultsTexts/Lesson_2/Choleric.txt") + "</p>";
    let Phlegmatic = "<p>" + readTextFile("ResultsTexts/Lesson_2/Phlegmatic.txt") + "</p>";
    let Sanguine = "<p>" + readTextFile("ResultsTexts/Lesson_2/Sanguine.txt") + "</p>";
    let Melancholic = "<p>" + readTextFile("ResultsTexts/Lesson_2/Melancholic.txt") + "</p>";
    let afterwords = "<p>" + readTextFile("ResultsTexts/Lesson_2/Afterwords.txt") + "</p>";
    let last_paragraph = "<p>" + readTextFile("ResultsTexts/Lesson_2/Last_paragraph.txt") + "</p>";
    let chart_description = "<p>" + readTextFile("ResultsTexts/Lesson_2/Chart_description.txt") + "</p>";
    let liar = "<p><strong>" + readTextFile("ResultsTexts/Lesson_2/liar.txt") + "</strong></p>";

    const extra_intro_points = args.extra_intro;
    const lying_points = args.lying;
    const neuro_points = args.neuroticism;
    let Temperaments = {1: "Холерик", 2: "Меланхолик", 3: "Флегматик", 4: "Сангвиник"};
    let type_start_phrase = "Твой преобладающий тип темперамента — ";
    let final_content = "";
    let test_result = "";
    let test_result_list = [];

    let data = [];
    let x_ticks = [];
    for (let i = 0; i <= 24; i++) {
        x_ticks.push(i);

        if (extra_intro_points==i) {
            data.push(neuro_points)
        } else {
            data.push(null)
        }
    }

    let chart_text_html = '<span class="chart-grid-horizontal"></span><span class="chart-text-label-y-top">Нестабильность</span><span class="chart-text-label-y-bottom">Стабильность</span><span class="chart-text-label-x-left">Интроверсия</span><span class="chart-text-label-x-right">Экстроверсия</span><span class="chart-text-corner-top-left">Меланхолик</span><span class="chart-text-corner-top-right">Холерик</span><span class="chart-text-corner-bottom-right">Сангвиник</span><span class="chart-text-corner-bottom-left">Флегматик</span>';

    random_number =Math.floor((Math.random() * 10000000) + 1);
    final_content = '<div class="ct-chart ct-chart-' + random_number + '">';
    final_content += chart_text_html +'</div>';
    final_content += '<script>new Chartist.Line(".ct-chart-' + random_number + '",{labels:[' + x_ticks + '],series:[[' + data + ']]},{showLine:false, height: "400px", width:"650px",high:24, low:0, chartPadding:{left: 70}, axisX:{low: 0,high:24}, axisY: {type: Chartist.FixedScaleAxis, ticks:['+x_ticks+'],low: 0,high:24,}});</script>';

    final_content += chart_description;

    // Определение по баллам
    let result_field = document.getElementById("result_field");
    if (lying_points == 9) final_content += liar;
    if (extra_intro_points < 9) {
        final_content += extra_intro_1_9;
        test_result_list.push('интроверт');
    }
    if (extra_intro_points >= 9 && extra_intro_points <= 11) {
        test_result_list.push('интроверт (не яркий)');
    }
    if ((extra_intro_points >= 10) && (extra_intro_points <= 14)) {
        final_content += extra_intro_10_14;
        test_result_list.push('амбиверт');
    }
    if (extra_intro_points > 15) {
        final_content += extra_intro_15_24;
        test_result_list.push('экстраверт');
    }
    if (extra_intro_points >= 13 && extra_intro_points <= 15) {
        test_result_list.push('экстраверт (не яркий)');
    }
    if (neuro_points <= 9) {
        final_content += neuroticism_1_9;
    }
    if ((neuro_points >= 10) && (neuro_points <= 14)) {
        final_content += neuroticism_10_14;
    }
    if (neuro_points >= 15) {
        final_content += neuroticism_15_24;
    }
    // Определение по кругу
    if ((extra_intro_points >= 12) && (neuro_points >= 12)) {
        final_content += "<p>" + type_start_phrase + '<strong>' + Temperaments["1"] + '</strong>' + "</p>" + Choleric;
        test_result_list.push(Temperaments["1"]);
    }
    if ((extra_intro_points >= 13 && extra_intro_points <= 15) && (neuro_points >= 13 && neuro_points <= 15)) {
        test_result_list.push('холерик (не яркий)');
    }
    if ((extra_intro_points <= 12) && (neuro_points >= 12)) {
        final_content += "<p>" + type_start_phrase + '<strong>' + Temperaments["2"] + '</strong>' + "</p>" + Melancholic;
        test_result_list.push(Temperaments["2"]);
    }
    if ((extra_intro_points >= 9 && extra_intro_points <= 11) && (neuro_points >= 13 && neuro_points <= 15)) {
        test_result_list.push('меланхолик (не яркий)');
    }
    if ((extra_intro_points <= 12) && (neuro_points <= 12)) {
        final_content += "<p>" + type_start_phrase + '<strong>' + Temperaments["3"] + '</strong>' + "</p>" + Phlegmatic;
        test_result_list.push(Temperaments["3"]);
    }
    if ((extra_intro_points >= 9 && extra_intro_points <= 11) && (neuro_points >= 9 && neuro_points <= 11)) {
        test_result_list.push('флегматик (не яркий)');
    }
    if ((extra_intro_points >= 12) && (neuro_points <= 12)) {
        final_content += "<p>" + type_start_phrase + '<strong>' + Temperaments["4"] + '</strong>' + "</p>" + Sanguine;
        test_result_list.push(Temperaments["4"]);
    }
    final_content += afterwords + last_paragraph;
    result_field.innerHTML = final_content;

    test_result = test_result_list.join();

    send_result(test_result, test_number, final_content);
}


function results_test_3(args, test_number) {
    let final_content = "";
    let physical_aggression = "<h5 class='mt-4'>Физическая агрессия - " + args.physical_aggression + "</h5>";
    let physical_aggression_text = "<p>" + readTextFile("ResultsTexts/Lesson_3/Physical_aggression_text.txt") + "</p>";
    let indirect_aggression = "<h5 class='mt-4'>Косвенная агрессия - " + args.indirect_aggression + "</h5>";
    let indirect_aggression_text = "<p>" + readTextFile("ResultsTexts/Lesson_3/Indirect_aggression_text.txt") + "</p>";
    let irritation = "<h5 class='mt-4'>Раздражение - " + args.irritation + "</h5>";
    let irritation_text = "<p>" + readTextFile("ResultsTexts/Lesson_3/Irritation_text.txt") + "</p>";
    let negativism = "<h5 class='mt-4'>Неготивизм - " + args.negativism + "</h5>";
    let negativism_text = "<p>" + readTextFile("ResultsTexts/Lesson_3/Negativism_text.txt") + "</p>";
    let offence = "<h5 class='mt-4'>Обидчивость - " + args.offence + "</h5>";
    let offence_text = "<p>" + readTextFile("ResultsTexts/Lesson_3/Offence_text.txt") + "</p>";
    let suspicion = "<h5 class='mt-4'>Подозрительность - " + args.suspicion + "</h5>";
    let suspicion_text = "<p>" + readTextFile("ResultsTexts/Lesson_3/Suspicion_text.txt") + "</p>";
    let verbal_aggression = "<h5 class='mt-4'>Вербальная агрессия - " + args.verbal_aggression + "</h5>";
    let verbal_aggression_text = "<p>" + readTextFile("ResultsTexts/Lesson_3/Verbal_aggression_text.txt") + "</p>";
    let remorse_conscience = "<h5 class='mt-4'>Угрызения совести / чувство вины  - " + args.remorse_conscience + "</h5>";
    let remorse_conscience_text = "<p>" + readTextFile("ResultsTexts/Lesson_3/Remorse_conscience_text.txt") + "</p>";

    final_content += physical_aggression + physical_aggression_text + indirect_aggression + indirect_aggression_text + irritation + irritation_text + negativism + negativism_text + offence + offence_text + suspicion + suspicion_text + verbal_aggression + verbal_aggression_text + remorse_conscience + remorse_conscience_text;


    let result_field = document.getElementById("result_field");
    result_field.innerHTML = final_content;
    let test_result = "";
    if ((parseInt(args.physical_aggression, 10) <= 45) && (parseInt(args.indirect_aggression, 10) <= 45) && (parseInt(args.irritation, 10) <= 45) && (parseInt(args.negativism, 10) <= 45) && (parseInt(args.offence, 10) <= 45) && (parseInt(args.suspicion, 10) <= 45) && (parseInt(args.verbal_aggression, 10) <= 45)) {
        test_result = "низкий уровень агрессии"
    } else {
        test_result = "высокий уровень агрессии"
    }
    send_result(test_result, test_number, final_content);
}


function results_test_4(args, test_number) {
    let final_content = "<p>Уровни развития определенных типов мышления:</p>";
    let test_result = '';
    let types_dict = {
        "P_D": "Предметно-действенное мышление",
        "A_C": "Абстрактно-символическое мышление",
        "C_L": "Словесно-логическое мышление",
        "H_O": "Наглядно-образное мышление",
        "K": "Креативность"
    };
    let calc_level = points => points < 3 ? "низкий" : points < 6 ? "средний" : "высокий";
    let P_D_level = calc_level(args.P_D);
    let A_C_level = calc_level(args.A_C);
    let C_L_level = calc_level(args.C_L);
    let H_O_level = calc_level(args.H_O);
    let K_level = calc_level(args.K);
    let P_D_text = "<li>Предметно–действенное мышление - <strong>" + P_D_level + "</strong></li>";
    let A_C_text = "<li>Абстрактно–символическое мышление - <strong>" + A_C_level + "</strong></li>";
    let C_L_text = "<li>Словесно–логическое мышление - <strong>" + C_L_level + "</strong></li>";
    let H_O_text = "<li>Наглядно–образное мышление -  <strong>" + H_O_level + "</strong></li>";
    let K_text = "<li>Креативность - <strong>" + K_level + "</strong></li>";
    let descriptions = "<br><p>" + readTextFile("ResultsTexts/Lesson_4/descriptions.txt") + "</p>";

    let _max = 0;
    let _type = "";
    for (let _key in args) {
        if (args[_key] > _max) {
            _max = args[_key];
            _type = _key;
        }
    }
    let test_result_list = [];
    for (let _key in args) {
        if (parseInt(args[_key]) == _max) {
            test_result_list.push(types_dict[_key]);
        }
    }
    test_result = test_result_list.join();

    final_content += "<ul>" + P_D_text + A_C_text + C_L_text + H_O_text + K_text + "</ul>" + descriptions;
    let result_field = document.getElementById("result_field");
    console.log(final_content);
    result_field.innerHTML = final_content;

    send_result(test_result, test_number, final_content);
}


function results_test_5(args, test_number) {
    let test_result = '';

    function strength(value) {
        if (value <= 3) return "слабо";
        if (value >= 7) return "сильно";
        if ((value >= 4) && (value <= 6)) return "средне"
    }

    let _types_dict = {
        "A": "артистичный тип",
        "P": "предпринимательский тип",
        "O": "офисный тип",
        "I": "интеллектуальный тип",
        "C": "социальный тип",
        "R": "реалистичный тип"
    };


    let real = "<li>" + "Реалистичный тип - " + args.R / 10 * 100 + "%" + ", выражен " + strength(args.R) + "</li>";
    let intellectual = "<li>" + "Интеллектуальный тип - " + args.I / 10 * 100 + "%" + ", выражен " + strength(args.I) + "</li>";
    let social = "<li>" + "Социальный тип - " + args.C / 10 * 100 + "%" + ", выражен " + strength(args.C) + "</li>";
    let office = "<li>" + "Офисный тип - " + args.O / 10 * 100 + "%" + ", выражен " + strength(args.O) + "</li>";
    let predpr = "<li>" + "Предпринимательский тип - " + args.P / 10 * 100 + "%" + ", выражен " + strength(args.P) + "</li>";
    let artistic =  "<li>" + "Артистичный тип - " + args.A / 10 * 100 + "%" + ", выражен " + strength(args.A) + "</li>";
    let text = readTextFile("ResultsTexts/Lesson_5/final_content.txt");
    let final_content = "<h5 class='mt-4'>Профессиональные типы личности:</h5>" + "<ul>" + real + intellectual + social + office + predpr + artistic + "</ul>" + text;
    let result_field = document.getElementById("result_field");
    result_field.innerHTML = final_content;

    let _max = 0;
    let _type = "";
    for (let _key in args) {
        if (args[_key] > _max) {
            _max = args[_key];
            _type = _key;
        }
    }
    let test_result_list = [];
    for (let _key in args) {
        if (parseInt(args[_key]) == _max) {
            test_result_list.push(_types_dict[_key]);
        }
    }
    test_result = test_result_list.join();

    send_result(test_result, test_number, final_content);
}


function results_test_6(args, test_number) {
    let final_content = "";
    let test_result;
    final_content += "<p>Ваш результат - " + args.percentage + "%.</p>";
    if (args.points >= 21) {
        test_result = "речевые (вербальные) способности";
    } else test_result = "no";

    // send_result(test_result, test_number);
    final_content += "<p>" + readTextFile("ResultsTexts/Lesson_6/Final_content.txt") + "</p>";
    let result_field = document.getElementById("result_field");
    result_field.innerHTML = final_content;

    send_result(test_result, test_number, final_content);
}


function results_test_7(args, test_number) {
    let final_content = "";
    let test_result;
    final_content += "<p>Ваш результат - " + args.percentage + "%.</p>";
    final_content += "<p>" + readTextFile("ResultsTexts/Lesson_7/Final_content.txt") + "</p>";
    let result_field = document.getElementById("result_field");
    result_field.innerHTML = final_content;
    if (args.percentage >= 50) {
        test_result = "способность к счету и логике";
    } else
        test_result = "no";
    send_result(test_result, test_number, final_content);
}


function results_test_8(args, test_number) {
    let text = "<p>" + readTextFile("ResultsTexts/Lesson_8/Final_content.txt") + "</p>";
    let final_content = "";
    let test_result;
    final_content += "<p>Образное мышление развито на " + args.percentage + "%.</p>";
    final_content += text;
    let result_field = document.getElementById("result_field");
    result_field.innerHTML = final_content;

    if (args.percentage >= 50) {
        test_result = "образное мышление";
    } else
        test_result = "no";
    send_result(test_result, test_number, final_content);
}

function results_test_9(args, test_number) {
    let text = "<p>" + readTextFile("ResultsTexts/Lesson_9/Final_content.txt") + "</p>";
    let final_content = "";
    let test_result;
    final_content += "<p>Пространственное восприятие развито на " + args.percentage + "%.</p>";
    final_content += text;
    let result_field = document.getElementById("result_field");
    result_field.innerHTML = final_content;
    if (args.percentage >= 50) {
        test_result = "пространственное восприятие";
    } else
        test_result = "no";
    send_result(test_result, test_number, final_content);
}


function results_test_10(args, test_number) {
    let text = "<p>" + readTextFile("ResultsTexts/Lesson_10/Final_content.txt") + "</p>";
    let final_content = "";
    let test_result;
    final_content += "<p>Технические способности развиты на " + args.percentage + "%.</p>";
    final_content += text;
    let result_field = document.getElementById("result_field");
    result_field.innerHTML = final_content;
    if (args.percentage >= 50) {
        test_result = "технические способности";
    } else
        test_result = "no";
    send_result(test_result, test_number, final_content);
}


function results_test_11(args, test_number) {
    let text = readTextFile("ResultsTexts/Lesson_12/Final_content.txt");
    let final_content = "";
    let test_result;
    final_content +=  "<p>Ваш результат - " + args.percentage + "%.</p>";
    final_content += text;
    let result_field = document.getElementById("result_field");
    result_field.innerHTML = final_content;
    if (args.percentage >= 50) {
        test_result = "внимательность";
    } else
        test_result = "no";
    send_result(test_result, test_number, final_content);
}

function results_test_12(args, test_number) {
    let text = readTextFile("ResultsTexts/Lesson_12/Final_content.txt");
    let final_content = "";
    let test_result;
    final_content += "<p>Аналитические способности развиты на " + args.percentage + "%.</p>";
    final_content += text;
    let result_field = document.getElementById("result_field");
    result_field.innerHTML = final_content;
    if (args.percentage >= 50) {
        test_result = "аналитические способности";
    } else
        test_result = "no";
    send_result(test_result, test_number, final_content);
}


function results_test_13(args, test_number) {
    let text = readTextFile("ResultsTexts/Lesson_13/Final_content.txt");
    let test_result = '';
    let final_content = "";
    let _types_dict = {
        "nature": "человек-природа",
        "technique": "человек-техника",
        "signs": "человек-знак",
        "creation": "человек-художественный образ",
        "person": "человек-человек"
    };
    let nature = "<li>Человек-природа: " + args.nature + "</li>";
    let technique = "<li>Человек-техника: " + args.technique + "</li>";
    let signs = "<li>Человек-знак: " + args.signs + "</li>";
    let creation = "<li>Человек-художественный образ: " + args.creation + "</li>";
    let person = "<li>Человек-человек: " + args.person + "</li>";

    final_content += "<ul>" + nature + technique + signs + creation + person + "</ul>";
    final_content += text;
    let result_field = document.getElementById("result_field");
    result_field.innerHTML = final_content;

    let _max = 0;
    let _type = "";
    for (let _key in args) {
        if (parseInt(args[_key]) > _max) {
            _max = parseInt(args[_key]);
            _type = _key;
        }
    }
    let test_result_list = [];
    for (let _key in args) {
        if (parseInt(args[_key]) == _max) {
            test_result_list.push(_types_dict[_key]);
        }
    }
    test_result = test_result_list.join();

    send_result(test_result, test_number, final_content);
}


function results_test_14(args, test_number) {
    let final_content = "";
    let labels_x = [];

    for (let i = 0; i < args.marks.length; i++) {
        labels_x[i] = i + 1;
    }

    let chart_text_html = '<span style="position: absolute;font-size: 12px;left: -86px;bottom: 142px;transform: rotate(-90deg);">Количество воспроизведенных слов</span><span style="position: absolute;font-size: 12px;left: 51px;bottom: 8px;">Номер пробы</span>';
    let random_number =Math.floor((Math.random() * 10000000) + 1);
    final_content += '<div style="padding-bottom: 10px;" class="ct-chart ct-chart-' + random_number + '">';
    final_content += chart_text_html +'</div>';
    final_content += '<script>new Chartist.Line(".ct-chart-' + random_number + '",{labels:[' + String(labels_x) + '],series:[[' + String(args.marks) + ']]},{axisY: {type: Chartist.FixedScaleAxis,ticks: [0,1,2,3,4,5,6,7,8,9,10],onlyInteger: true, high: 10, low: 0}, width: "650px", height: "240px",chartPadding:{right:40}});</script>';

    let case_1_text = "<p>Поздравляем! =) У вас хорошая память. Но помните, показатели всегда можно улучшить.</p>";
    let case_2_text = "<p>Вы рассеяны, забывчивы или утомлены.</p>";
    let case_3_text = "<p>Ваше внимание неустойчиво. Сосредоточьтесь на тесте.</p>";
    let case_4_text = "<p>Вы эмоционально вялы, и не заинтересованы, в том чтобы запомнить больше слов. Отдохните и позже снова вернитесь к прохождению теста.</p>";
    if (args.marks[0] >= 5) {
        if (args.marks[0] <= 8) {
            if ((args.marks[1]-2) >= args.marks[0] && args.marks[2] >= 9 && args.marks[3] == 10 && args.marks[4] == 10 /*&& args.marks[5] == 10*/) {
                final_content += case_1_text;
            }
        }
        if (args.marks[0] > 8 && args.marks[1] == 10 && args.marks[2] == 10 && args.marks[3] == 10 && args.marks[4] == 10 /*&& args.marks[5] == 10*/) {
            final_content += case_1_text;
        }
    }
    if (args.marks[1] >= 8 && args.marks[2] < 8 && args.marks[3] < 8 && args.marks[4] < 8/* && args.marks[5] < 8*/) {
        final_content += case_2_text;
    }
    if (args.marks.slice(0, 5).every( (val, i, arr) => ((val === arr[0]) && (val >= 1 && val <= 7)))) {
        final_content += case_4_text;
    }

    let zigzag = false;
    for (let i=1; i <= (args.marks.length - 3); i++) {
        let current = args.marks[i];
        let prev = args.marks[i-1];
        let next = args.marks[i+1];


        if (!((current >= prev && current <= next) || (current <= prev && current >= next))) {
            zigzag = true
        }
    }
    if (zigzag) {
        final_content += case_3_text;
    }

    let long_term_memory_text = "";
    let sixth_audition = args.marks[5];
    if (sixth_audition === 7) {
        long_term_memory_text = "<p>У вас нормальный уровень слуховой долговременной памяти.</p>";
    } else if (sixth_audition >= 8 && sixth_audition <= 10) {
        long_term_memory_text = "<p>У вас высокий уровень слуховой долговременной памяти.</p>";
    } else if (sixth_audition >= 5 && sixth_audition <= 6) {
        long_term_memory_text = "<p>У вас средний уровень слуховой долговременной памяти.</p>";
    } else if (sixth_audition >= 3 && sixth_audition <= 4) {
        long_term_memory_text = "<p>Ваш уровень слуховой долговременной памяти ниже среднего.</p>";
    } else if (sixth_audition >= 0 && sixth_audition <= 2) {
        long_term_memory_text = "<p>У вас низкий уровень слуховой долговременной памяти.</p>";
    }
    final_content += long_term_memory_text;

    let wrong_labels_x = [];
    let hasWrongWords = false;
    for (let i = 0; i < args.wrong_marks.length; i++) {
        wrong_labels_x[i] = i + 1;
        if (args.wrong_marks[i] > 0) {
            hasWrongWords = true
        }
    }
    if (hasWrongWords) {
        final_content += "<p>У вас замечены лишние слова. Будьте  внимательны при прослушивании слов.</p>";
        random_number = Math.floor((Math.random() * 10000000) + 1);

        let chart_text_html_2 = '<span class="text-center" style="width: 100%;position: absolute;top: 0;">Лишние слова</span><span style="position: absolute;font-size: 12px;left: -55px;bottom:101px;transform: rotate(-90deg);">Количество лишних слов</span><span style="position: absolute;font-size: 12px;left: 51px;bottom: 0;">Номер пробы</span>';
        let random_number_2 =Math.floor((Math.random() * 10000000) + 1);
        final_content += '<div style="padding-top: 25px;min-height: 180px;" class="ct-chart ct-chart-wrong-' + random_number_2 + '">';
        final_content += chart_text_html_2 +'</div>';
        final_content += '<script>new Chartist.Line(".ct-chart-wrong-' + random_number_2 + '",{labels:[' + String(wrong_labels_x) + '],series:[[' + String(args.wrong_marks) + ']]},{width: "650px", height: "240px", axisY: {onlyInteger: true, low: 0}, chartPadding:{right:40}});</script>';
    }

    send_result("test 14 is passed", test_number, final_content);
}


function results_test_15(args, test_number) {
    let final_content = "";
    let points = args.points;
    let test_result;
    let result = "Качества лидера ";
    if (points <= 9) result += "выражены очень слабо";
    if ((points <= 24) && (points >= 10)) result += "выражены слабо";
    if ((points <= 34) && (points) >= 25) result += "выражены средне";
    if ((points <= 39) && (points) >= 35) result += "выражены сильно";
    if (points >= 40) result += "выражены очень сильно";

    final_content += result;
    let result_field = document.getElementById("result_field");
    result_field.innerHTML = final_content;
    if (args.points >= 50) {
        test_result = "лидерские качества";
    } else
        test_result = "no";
    send_result(test_result, test_number, final_content);
}


function find_result_creator(test_number, args) {
    switch (test_number) {
        case 1:
            results_test_1(args, test_number);
            break;
        case 2:
            results_test_2(args, test_number);
            break;
        case 3:
            results_test_3(args, test_number);
            break;
        case 4:
            results_test_4(args, test_number);
            break;
        case 5:
            results_test_5(args, test_number);
            break;
        case 6:
            results_test_6(args, test_number);
            break;
        case 7:
            results_test_7(args, test_number);
            break;
        case 8:
            results_test_8(args, test_number);
            break;
        case 9:
            results_test_9(args, test_number);
            break;
        case 10:
            results_test_10(args, test_number);
            break;
        case 11:
            results_test_11(args, test_number);
            break;
        case 12:
            results_test_12(args, test_number);
            break;
        case 13:
            results_test_13(args, test_number);
            break;
        case 14:
            results_test_14(args, test_number);
            break;
        case 15:
            results_test_15(args, test_number);
            break;
        default:
            break;
    }
}