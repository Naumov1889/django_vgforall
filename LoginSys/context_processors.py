def login(request):
    # args = {}
    # args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            try:
                User.objects.get(username=username)
                args['login_error'] = "Пользователь не активирован"
                return render_to_response('login.html')
            except:
                args['login_error'] = "Пользователь не найден"
                return render_to_response('login.html')
    # else:
    #     return render_to_response('login.html', args)