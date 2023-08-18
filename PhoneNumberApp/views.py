import time

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from PhoneNumberApp.forms import PhoneForm, CodeForm, InviteCode
from PhoneNumberApp.models import CustomUser, authenticate
import string
import random
from django.core.cache import cache

# Символы, которые будут использоваться для генерации кода
CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits

"""
ввиду небольшого количества представляемой информации решил использовать FBV а не CBV
"""


def login_required(url_login='http://127.0.0.1:8000/'):
    """
    Проверяет авторизован ли пользователь, а именно есть ли в сессии user
    :param url_login: url на которой будет перенаправлен не авторизованный пользователь
    :return: HttpResponse
    """
    def decorator(foo):
        def _wrapper(*args, **kwargs):
            try:
                user = args[0].session['user']
                return foo(*args, **kwargs)
            except KeyError:
                return redirect(url_login)
        return _wrapper
    return decorator


def gen_key(size: int):
    """
    :param size: размер кода
    :return: код соответствует данному рег. выражению: [\dA-Za-z]{6}
    """
    return ''.join(random.choice(CHARS) for _ in range(size))


@require_http_methods(['GET', 'POST'])
def authorization(request):
    # пустая форма
    if request.method == 'GET':
        form = PhoneForm()
        return render(request, 'authorization.html', {'form': form})
    # роверяем введеный номер "отправляем код"
    if request.method == 'POST':
        form = PhoneForm({"number": request.POST['number']})
        if form.is_valid():
            # сохраняем данные в session
            request.session['number'] = form.cleaned_data['number'].as_international
            request.session['activate_code'] = gen_key(size=4)
            time.sleep(2)
            return redirect(activate_code)
        else:
            return render(request, 'authorization.html', {'form': form, 'error': form.as_div()})


@require_http_methods(['GET', 'POST'])
def activate_code(request):
    # берем код активации
    try:
        user_activate_code = request.session['activate_code']
    except KeyError:
        return redirect(authorization)
    # Так как мы только имитируем отправку кода, сам код будет уже вставлен в форму
    if request.method == 'GET':
        form = CodeForm({'code': user_activate_code})
        return render(request, 'activate_code.html', {'form': form})

    if request.method == 'POST':
        try:
            number = request.session['number']
        except KeyError:
            return redirect(request, 'authorization')
        code = request.POST['code']
        if code == user_activate_code:
            # пытаемся авторизовать
            user = authenticate(number)
            if user:
                request.session['user'] = number
                return redirect(profile)
            else:
                # регистрируем
                codes = CustomUser.objects.all().values('invite_code')
                key = gen_key(size=6)
                while key in codes:
                    key = gen_key(size=6)
                CustomUser.objects.create(phone_number=number, invite_code=key)
                request.session['user'] = number
            return redirect(profile)


@login_required(url_login='/authenticate/')
@require_http_methods(['GET', 'POST'])
def profile(request):
    error = ''
    user = CustomUser.objects.get(phone_number=request.session['user'])
    if request.method == 'POST':
        try:
            code = request.POST['code']
        except KeyError:
            return redirect(profile)
        # проверяем введенный code, если корректный - сохраняем
        c = code_is_valid(code, user)
        if c:
            user.invitation_code = c
            user.save()
        else:
            error = 'некорректный код'

    # пользователь уже ввел код приглашения?
    form = False
    if user.invitation_code is None:
        code = InviteCode()
        form = True
    else:
        code = user.invitation_code.invite_code
    invited_persons = user.custom_user.all().values('phone_number')
    return render(request, 'profile.html', {'user': user,
                                            'form': form,
                                            'code': code,
                                            'numbers': invited_persons,
                                            'error': error})


def logout(request):
    """выходим из аккаунта - очищаем session"""
    request.session.flush()
    return redirect(authorization)


def code_is_valid(code, user):
    """Возвращаем владельца кода, если он существует и не равен текущему пользователю"""
    try:
        invite_user = CustomUser.objects.get(invite_code=code)
        if invite_user != user:
            return invite_user
        else:
            return False
    except CustomUser.DoesNotExist:
        return False
