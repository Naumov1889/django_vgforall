let popbox = new Popbox();


(function () {
    if (Boolean(document.querySelector('.js-password-visibility'))) {
        document.querySelectorAll('.js-password-visibility').forEach(toggler => {
            toggler.addEventListener('click', e => {
                let password_input = toggler.closest('.input-container').querySelector('input');

                if (password_input.type === "password") {
                    password_input.type = "text";

                    toggler.querySelector('i').classList.remove('icon_eye_1');
                    toggler.querySelector('i').classList.add('icon_eye_2');
                } else {
                    password_input.type = "password";

                    toggler.querySelector('i').classList.remove('icon_eye_2');
                    toggler.querySelector('i').classList.add('icon_eye_1');
                }
            });
        })
    }
}());

(function () {
    if (Boolean(document.querySelector('.accordion'))) {
        let acc = document.getElementsByClassName("accordion");

        for (let i = 0; i < acc.length; i++) {
            let accordion_title = acc[i].querySelector('.accordion__title');
            accordion_title.addEventListener("click", function () {
                this.closest(".accordion").classList.toggle("accordion_active");

                let content = this.nextElementSibling;
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";

                }

                if (acc[i].closest('.accordion_type-2') && (!acc[i].classList.contains('accordion_type-2'))) {
                    let accordion_parent = acc[i].closest('.accordion_type-2');
                    let parent_content = accordion_parent.querySelector(".accordion__content");
                    parent_content.style.maxHeight = parent_content.scrollHeight + "px";
                    console.log('yes', acc[i].classList)
                    setTimeout(function () {

                    }, 300);

                }

            });
        }
    }
}());
(function () {

}());

(function () {
    document.querySelectorAll(".js-login-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            let form = this.closest("form");

            let csrfValue = form.querySelector("input[name=csrfmiddlewaretoken]").value;

            let usernameInput = form.querySelector("input[name=username]");
            let usernameValue = usernameInput.value;

            let passwordInput = form.querySelector("input[name=password]");
            let passwordValue = passwordInput.value;

            let should_redirect_to_tests_input = form.querySelector("input[name=should_redirect_to_tests]");
            let should_redirect_to_tests_value = should_redirect_to_tests_input.value;

            postAjax('/auth/login/', {
                    csrfmiddlewaretoken: csrfValue,
                    username: usernameValue,
                    password: passwordValue,
                }, function (data) {
                    let data_parsed = JSON.parse(data);

                    form.querySelectorAll('.error_message').forEach(error_message => {
                        error_message.remove();
                    });

                    form.querySelectorAll('input').forEach(input => {
                        input.classList.remove('isInvalid');
                        input.classList.add('isValid');
                    });

                    if ('errors' in data_parsed) {

                        for (let key in data_parsed['errors']) {
                            if (key == "__all__") {
                                let final_error_message = '';
                                for (let i in data_parsed['errors'][key]) {
                                    final_error_message += '<li><small>' + data_parsed['errors'][key][i] + '</small></li>>'
                                }

                                document.querySelector('.my-spinner').style.display = "none";

                                form.querySelector('.js-login-btn').insertAdjacentHTML('beforebegin', '<ul class="error_message" style="width: 100%;margin: -0.75rem 0 0.5rem 0;text-align: left;">' + final_error_message + '</ul>');

                            } else {
                                let input_with_error = form.querySelector('[name=' + key + ']');
                                input_with_error.classList.add('isInvalid');

                                let final_error_message = '';
                                for (let i in data_parsed['errors'][key]) {
                                    final_error_message += '<li><small>' + data_parsed['errors'][key][i] + '</small></li>>'
                                }

                                document.querySelector('.my-spinner').style.display = "none";

                                input_with_error.closest('.input-container').insertAdjacentHTML('afterend', '<ul class="error_message" style="width: 100%;margin: -0.75rem 0 0.5rem 0;text-align: left;">' + final_error_message + '</ul>');
                            }

                        }

                        new Popbox();  // reinit
                    } else {
                        popbox.close(form.closest(".popbox"));

                    }
//
                    if ('success' in data_parsed) {
                        form.reset();
                        document.querySelector('.my-spinner').style.display = "none";


                        location.reload();
                    }

                }
            );

            document.querySelector('.my-spinner').style.display = "inline-block";

        });
    });

    document.querySelectorAll(".js-register-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            let form = this.closest("form");

            let csrfValue = form.querySelector("input[name=csrfmiddlewaretoken]").value;

            let checkbox_object = form.querySelector('.checkbox');
            let checkbox_input = form.querySelector('.checkbox__input');
            let isCheckboxValid = validateCheckbox(checkbox_input);
            if (!isCheckboxValid) inputErrorAnimation(checkbox_object);

            let usernameInput = form.querySelector("input[name=username]");
            let usernameValue = usernameInput.value;
            if (!usernameValue) inputErrorAnimation(usernameInput);

            let password_1_Input = form.querySelector("input[name=password1]");
            let password_1_Value = password_1_Input.value;

            let password_2_Input = form.querySelector("input[name=password2]");
            let password_2_Value = password_2_Input.value;

            if (!password_1_Value) inputErrorAnimation(password_1_Input);
            if (!password_2_Value) inputErrorAnimation(password_2_Input);

            let emailInput = form.querySelector("input[name=email]");
            let emailValue = emailInput.value;
            let isEmailValid = validateEmail(emailValue);
            if (!isEmailValid) inputErrorAnimation(emailInput);

            let isFormValid = isCheckboxValid /*&& isEmailValid && usernameValue && password_1_Value && password_2_Value*/;

            if (isFormValid) {
                postAjax('/auth/registration/', {
                    csrfmiddlewaretoken: csrfValue,
                    username: usernameValue,
                    password1: password_1_Value,
                    password2: password_2_Value,
                    email: emailValue,
                }, function (data) {
                    let data_parsed = JSON.parse(data);

                    form.querySelectorAll('.error_message').forEach(error_message => {
                        error_message.remove();
                    });

                    form.querySelectorAll('input').forEach(input => {
                        input.classList.remove('isInvalid');
                        input.classList.add('isValid');
                    });

                    if ('errors' in data_parsed) {

                        for (let key in data_parsed['errors']) {
                            let input_with_error = form.querySelector('[name=' + key + ']');
                            input_with_error.classList.add('isInvalid');

                            let final_error_message = '';
                            for (let i in data_parsed['errors'][key]) {
                                final_error_message += '<li><small>' + data_parsed['errors'][key][i] + '</small></li>>'
                            }

                            document.querySelector('.my-spinner').style.display = "none";

                            input_with_error.closest('.input-container').insertAdjacentHTML('afterend', '<ul class="error_message" style="width: 100%;margin: -0.75rem 0 0.5rem 0;text-align: left;">' + final_error_message + '</ul>');
                        }

                        new Popbox();  // reinit
                    } else {
                        popbox.close(form.closest(".popbox"));

                    }
//
                    if ('success' in data_parsed) {
                        form.reset();
                        document.querySelector('.my-spinner').style.display = "none";


                        document.querySelector('.js-popbox-result .title_h2').innerHTML = '<span class="text_color_primary">Успех!</span> Для завершения регистрации подтвердите почту.';
                        popbox.open("popbox-result");
                    }

                });
                document.querySelector('.my-spinner').style.display = "inline-block";
            }
        });
    });


    document.querySelectorAll(".js-reset-password-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            let form = this.closest("form");

            let csrfValue = form.querySelector("input[name=csrfmiddlewaretoken]").value;

            let emailInput = form.querySelector("input[name=email]");
            let emailValue = emailInput.value;
            let isEmailValid = validateEmail(emailValue);
            if (!isEmailValid) inputErrorAnimation(emailInput);

            let isFormValid = true;

            if (isFormValid) {
                postAjax('/reset-password/', {
                    csrfmiddlewaretoken: csrfValue,
                    email: emailValue,
                }, function (data) {
                    let data_parsed = JSON.parse(data);

                    form.querySelectorAll('.error_message').forEach(error_message => {
                        error_message.remove();
                    });

                    form.querySelectorAll('input').forEach(input => {
                        input.classList.remove('isInvalid');
                        input.classList.add('isValid');
                    });

                    if ('errors' in data_parsed) {

                        for (let key in data_parsed['errors']) {
                            let input_with_error = form.querySelector('[name=' + key + ']');
                            input_with_error.classList.add('isInvalid');

                            let final_error_message = '';
                            for (let i in data_parsed['errors'][key]) {
                                final_error_message += '<li><small>' + data_parsed['errors'][key][i] + '</small></li>>'
                            }

                            document.querySelector('.my-spinner').style.display = "none";

                            input_with_error.closest('.input-container').insertAdjacentHTML('afterend', '<ul class="error_message" style="width: 100%;margin: -0.75rem 0 0.5rem 0;text-align: left;">' + final_error_message + '</ul>');
                        }

                        new Popbox();  // reinit
                    } else {
                        popbox.close(form.closest(".popbox"));

                    }
//
                    if ('success' in data_parsed) {
                        form.reset();
                        document.querySelector('.my-spinner').style.display = "none";


                        document.querySelector('.js-popbox-result .title_h2').innerHTML = 'Мы отправили инструкцию по восстановлению пароля на вашу почту.';
                        popbox.open("popbox-result");
                    }

                });
                document.querySelector('.my-spinner').style.display = "inline-block";
            }
        });
    });


    document.querySelectorAll(".js-callback-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            let form = this.closest("form");

            let csrfValue = form.querySelector("input[name=csrfmiddlewaretoken]").value;

            let nameInput = form.querySelector("input[name=name]");
            let nameValue = nameInput.value;
            let isNameValid = validateName(nameValue);

            let emailInput = form.querySelector("input[name=email]");
            let emailValue = emailInput.value;
            let isEmailValid = validateEmail(emailValue);

            let textInput = form.querySelector("textarea[name=text]");
            let textValue = textInput.value;

            if (!isNameValid) inputErrorAnimation(nameInput);
            if (!isEmailValid) inputErrorAnimation(emailInput);

            let isFormValid = isNameValid && isEmailValid;

            if (isFormValid) {
                postAjax('/record_callback/', {
                    csrfmiddlewaretoken: csrfValue,
                    name: nameValue,
                    email: emailValue,
                    text: textValue,
                }, function (data) {
                    document.querySelector('.my-spinner').style.display = "none";
                    document.querySelector('.js-popbox-result .title_h2').innerHTML = '<span class="text_color_primary">Спасибо, <br></span> ваша заявка отправлена';
                    popbox.open("popbox-result")
                }, function (data) {
                    document.querySelector('.my-spinner').style.display = "none";
                    document.querySelector('.js-popbox-result .title_h2').innerHTML = '<span class="text_color_primary">Ошибка!</span> Пожалуйста, перезагрузите страницу и попробуйте отправить запрос снова.';
                    popbox.open("popbox-result")
                });
                form.reset();

                popbox.close(form.closest(".popbox"));
                document.querySelector('.my-spinner').style.display = "inline-block";
            }

        });
    });


    function validateName(inputNameValue) {
        let name_format = /^[A-Za-z\u0400-\u04FF\s]+$/;
        return !!inputNameValue.match(name_format);
    }

    function validatePhone(inputPhoneValue) {
        return !!(inputPhoneValue.length === 15);
    }

    function validateEmail(inputEmailValue) {
        let mail_format = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        return !!inputEmailValue.match(mail_format);
    }

    function validateCheckbox(input) {
        return input.checked;
    }

    function inputErrorAnimation(input) {
        input.classList.add("bounce");
        setTimeout(function () {
            input.classList.remove("bounce");
        }, 1000);
    }

    function postAjax(url, data, success/*, fail*/) {
        let params = typeof data == 'string' ? data : Object.keys(data).map(
            function (k) {
                return encodeURIComponent(k) + '=' + encodeURIComponent(data[k])
            }
        ).join('&');

        let xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
        xhr.open('POST', url);
        xhr.onreadystatechange = function () {
            if (xhr.readyState > 3 && xhr.status === 200) {
                success(xhr.responseText);
            }
        };
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send(params);
        return xhr;
    }


}());

(function () {
    document.querySelector(".burger").addEventListener("click", function () {
        document.querySelector(".overlay").classList.add("overlay_active");
        document.querySelector(".sidebar").classList.add("sidebar_active");
        document.querySelector(".pusher").classList.add("pusher_active");
    });

    document.querySelector(".overlay").addEventListener("click", function () {
        document.querySelector(".overlay").classList.remove("overlay_active");
        document.querySelector(".pusher").classList.remove("pusher_active");
        document.querySelector(".sidebar").classList.remove("sidebar_active");
    });

    document.querySelectorAll(".js-sidebar-nav-item").forEach(nav_item => {
        nav_item.addEventListener("click", function () {
            document.querySelector(".overlay").classList.remove("overlay_active");
            document.querySelector(".pusher").classList.remove("pusher_active");
            document.querySelector(".sidebar").classList.remove("sidebar_active");
        });
    })
}());