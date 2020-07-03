let hide = true; //глобальная переменная, отвечающая будет ли строка передана в подсказку

// Показываем подсказку
function showHint(text){
    if (window.innerWidth > 900) {
        let _x = event.clientX;
        let _y = event.clientY;
        let _dx = 5;
        let left = false;
        let right = false;
        let hint_is_needed = false;
        let separator = "***";
        let html_text = "";

        if(text) {
            hint_is_needed = true;
            let arrayOfTerms = text.split(separator);
            for (let current_term = 0; current_term < arrayOfTerms.length; current_term++) {
                html_text = html_text + arrayOfTerms[current_term] + '<br>';
            }
        }

        if(_dx + _x + HintBlock.clientWidth > document.body.clientWidth){_x = document.body.clientWidth - HintBlock.clientWidth - _dx; left=true;}
        if(_dx + _y + HintBlock.clientHeight > document.body.clientHeight){_y = document.body.clientHeight - HintBlock.clientHeight - _dx; right=true;}
        if(left&&right) _y = document.body.clientHeight - HintBlock.clientHeight - _dx*4;
        HintBlock.style.left = _x + 10 + 'px';
        HintBlock.style.top = _y + 10 + document.body.scrollTop + 'px';
        if(hide && hint_is_needed){
            HintBlock.innerHTML = html_text;
            HintBlock.style.visibility = "visible";
            HintBlock.style.opacity = "1";
            hide = false;
        }
    } else {
        document.querySelector('[data-js=popbox-test-hint]').innerHTML = text;
        popbox.open('popbox-test-hint');
    }
}

// Убираем подсказку
function hideHint(){
    HintBlock.style.visibility="hidden";
    HintBlock.style.opacity="0";
    HintBlock.innerHTML="";
    HintBlock.style.top=0;
    HintBlock.style.left=0;
    hide=true;
}


// Таймер обратного отсчета
function Timer(critical_time) {
    if (critical_time !== 0){
        let idInt = setInterval(function() {
        let minutes = Math.floor(critical_time/60);
        let seconds = critical_time % 60;
        document.getElementById("siteTimerMinutes").innerHTML = minutes;
        document.getElementById("siteTimerSeconds").innerHTML = seconds;

        if (critical_time === 0) {
            let tagNames = ["textarea", "input"];
            for (let tagName = 0; tagName < tagNames.length; tagName++){
                let AllElements = document.getElementsByTagName(tagNames[tagName]);
                for(let element = 0; element< AllElements.length; element++){
                    AllElements[element].setAttribute('readonly', 'readonly');

                }
            }

            clearInterval(idInt);
            // alert("Время вышло!!!");
            document.querySelector('form').submit();
        }
        critical_time = critical_time - 1;
        }, 1000);
    }
}


// Определяем, если пользователь уже прошел тест, то перенаправляем в личный кабинит
function was_finished(is_finished) {
    console.log(is_finished);
    if (is_finished === 1) {
       window.location.replace("http://127.0.0.1/account/");
    }
    else {
        return 0;
    }
}


// Активирует функции при старте страницы, таймер, если надо, и определение завершенности
function start_page(critical_time, is_finished, test_lesson){
    if (Boolean(document.querySelector('.popbox-test-description .btn'))) {
        document.querySelector('.popbox-test-description .btn').addEventListener('click', e => {
            Timer(critical_time);
        });
    } else {
        Timer(critical_time);
    }
    was_finished(is_finished);
    if (test_lesson === 14)
    {
        document.getElementById("FinishButton").setAttribute("disabled", "true");
    }
}


// Скрывает адио контролы при паузе или завершении
function control_audio(audio_id) {
    document.querySelectorAll('.test_14_audition_number').forEach(div => {
        div.innerHTML = '';
    });

    let current_audio = document.getElementById(audio_id);
    current_audio.removeAttribute("controls");
    let form_id = audio_id.split("_")[0] + "_form";
    let current_form = document.getElementById(form_id);
    current_form.removeAttribute("style");
}


// Пауза
function sleep(ms) {
    ms += new Date().getTime();
    while (new Date() < ms){}
}


function delete_hidden_div() {
    let hidden_div = document.getElementById("hidden_div");
    if (typeof hidden_div != 'undefined' && hidden_div != null){document.body.removeChild(hidden_div);}
}


function sleep_Timer(ms) {

    let hidden_div = document.createElement("div");
    hidden_div.setAttribute("id","hidden_div");
    hidden_div.setAttribute("class","hidden_div");
    document.body.appendChild(hidden_div);

    let sleep_Timer = document.getElementById("Timer");
    sleep_Timer.removeAttribute("style");

    let idInt = setInterval(function() {
        let minutes = Math.floor(ms/60);
        let seconds = ms % 60;
        document.getElementById("siteTimerMinutes").innerHTML = minutes;
        document.getElementById("siteTimerSeconds").innerHTML = seconds;

        if (ms === 0) {
            sleep_Timer.style.display = "none";
            clearInterval(idInt);
        }
        ms = ms - 1;
        }, 1000);
}



// Действия при нажатии кнопки в тесте 15
var test_14_audition_number = 1;
function button_clicked(question_id) {
    test_14_audition_number += 1;
    document.querySelectorAll('.test_14_audition_number').forEach(div => {
        div.innerHTML = String(test_14_audition_number) + " прослушивание";
    });
    let current_block = document.getElementById(question_id + "_block");
    let next_block = document.getElementById(question_id + 1 + "_block");
    let last_block = document.getElementById(question_id + 2 + "_block");

    current_block.style.display = "none";

    if ((typeof last_block === 'undefined' || last_block === null) && (typeof next_block === 'undefined' || next_block === null)) {
        document.getElementById("FinishButton").removeAttribute("disabled");
        document.getElementById("FinishButton").classList.add("active");
    }
    else {
        next_block.removeAttribute("style");
    }
    if ((typeof last_block === 'undefined' || last_block === null) && (typeof next_block != 'undefined' && next_block != null))
    {
        let seconds_for_waiting = 10;
        sleep_Timer(seconds_for_waiting);
        setTimeout(delete_hidden_div, seconds_for_waiting * 1000 + 5);
    }
}