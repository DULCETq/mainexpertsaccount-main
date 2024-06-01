import json
from .forms import LoginForm, RegisterForm, ResetForm, ClientFullRegistrationForm, ExpertFullRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .functions import register, full_registration_client, full_registration_expert, attach_subjects_to_expert
from django.contrib.sessions.models import Session
from .models import Account, Client, ExpertCalendar, Expert


# Create your views here.

@api_view(['GET', 'POST'])
def LoginView(request):
    """Функция под обработку авторизации пользователей"""
    form = LoginForm
    if request.method == 'POST':
        """Отправка запроса на авторизацию"""
        form = form(request.POST)
        context = {'success': False}
        if form.is_valid():
            print(form.is_valid())
            user = User.objects.filter(username=form.data['username'], password=form.data['password'])
            if user:
                user = User.objects.get(username=form.data['username'], password=form.data['password'])
                login(request, user)
                request.session['active_session'] = True
                for key, value in request.session.items():
                    print('{} => {}'.format(key, value))
                success = True
                print(success)
                print(request.session['active_session'])
                context['client_id'] = user.id
                context['success'] = True
                context['session_id'] = request.session.session_key
                context['user_type'] = Account.objects.get(user=user).user_type
            return Response(json.dumps(context))
        else:
            success = False
            return Response(json.dumps(context))


@api_view(['GET', 'POST'])
def RegisterView(request):
    """Функция под обработку авторизации пользователей"""
    form = RegisterForm

    if request.method == 'POST':
        """Отправка запроса на авторизацию"""
        form = form(request.POST)
        success = False
        print(request.POST)
        print(form.data)
        if form.is_valid() or request.POST.get('role', None) == 'admin':
            print(form.cleaned_data)
            data = dict(form.cleaned_data)

            data['email'] = request.POST['email']
            print(data)
            result = register(data)
            if result['success']:
                success = True
                return Response(json.dumps({
                    'success': success}))
            else:
                return Response(json.dumps({'success': False,
                                            'error': result['error']}))
        return Response(json.dumps({
            'success': success,
            'error': 'Form is invalid'}))


@api_view(['GET', 'POST'])
def ResetView(request):
    """Функция под обработку авторизации пользователей"""
    form = ResetForm

    if request.method == 'POST':
        """Отправка запроса на авторизацию"""
        form = form(request.POST)
        success = False
        if form.is_valid():
            account = register(form.cleaned_data)
            if account:
                success = True
                return Response(json.dumps({
                    'success': success}))
        return Response(json.dumps({
            'success': success}))


@api_view(['GET', 'POST'])
def LogoutView(request):
    """Функция под обработку выхода пользователя из личного кабинета"""

    if request.method == 'POST':
        """Отправка запроса на выход"""
        request.session['active_session'] = False
        s = Session.objects.get(session_key=request.POST['token'])
        sess = s.get_decoded()
        sess['active_session'] = False
        Session.objects.save(s.session_key, sess, s.expire_date)
        print(s.get_decoded())
        print(sess['active_session'])
        logout(request)
        return Response(json.dumps({
            'success': True}))


@api_view(['POST'])
def UserInfoAdmin(request):
    phone = request.data['phone']
    if '-' in phone:
        phone = phone.split('-')
        phone[1] = phone[1][1:-1]
        clean_phone = ''.join(phone)
    else:
        clean_phone = phone
    account = Account.objects.get(phone=clean_phone) if Account.objects.filter(phone=clean_phone) else None
    if account:
        client = Client.objects.filter(account=account)
        expert = Expert.objects.filter(user=account)
        context = {
            'success': True,
            'error': None,
            'user_id': account.user.id,
            'name': account.name,
            'phone': account.phone,
            'email': account.user.email,
            'client_id': client[0].id if client else None,
            'expert_id': expert[0].id if expert else None
        }
    else:
        context = {
            'success': False,
            'error': 'User not found'
        }
    return Response(json.dumps(context))


@api_view(['GET', 'POST'])
def ClientInfo(request, client_id=''):
    form = ClientFullRegistrationForm

    if request.method == 'GET':
        print('get info')
        account = Account.objects.get(user_id=client_id)
        print(account)
        client = Client.objects.filter(account=account)
        success = False
        data = []
        print(client)
        if client:
            inst = Client.objects.get(account=account)
            data = dict(inst.__dict__)
            data.pop('_state')
            data.pop('created')
            data.pop('updated')
            data['birth'] = inst.birth.strftime('%d.%m.%Y') if inst.birth else None
            data['phone'] = account.phone
            data['email'] = account.user.email
            data['avatar'] = account.avatar.url if account.avatar else None
            data['name'] = account.name
            print(data)
            success = True
        return Response(json.dumps({
            'success': success,
            'data': data
        }))

    if request.method == 'POST':
        """Отправка запроса на регистрацию клиента"""
        print(request.POST)
        form = form(request.POST)
        print(form.is_valid())
        success = False
        if form.is_valid():
            account = full_registration_client(form.data, request.FILES['avatar'] if request.FILES else None)
            if account:
                success = True
                Response(json.dumps({
                    'success': success}))
        return Response(json.dumps({
            'success': success}))


@api_view(['GET', 'POST'])
def ExpertInfo(request):
    if request.method == 'GET':
        success = False
        data = []
        print(request.data)
        print(request.data.get('role', None) == 'admin')
        if request.data.get('role', None) == 'admin':
            expert = Expert.objects.get(id=request.data['expert_id'])
            account = expert.user

        else:
            account = Account.objects.get(user_id=request.data['expert_id'])
            expert = Expert.objects.filter(user=account)
        if expert:
            inst = Expert.objects.get(user=account)
            data = dict(inst.__dict__)
            data.pop('_state')
            data.pop('created')
            data.pop('updated')
            data['phone'] = account.phone
            data['email'] = account.user.email
            data['id'] = inst.id
            data['name'] = account.name
            success = True
            print(data)
        return Response(json.dumps({
            'success': success,
            'data': data
        }))
    if request.method == 'POST':
        """Отправка запроса на регистрацию клиента"""
        form = ExpertFullRegistrationForm
        form = form(request.POST)
        success = False
        if form.is_valid():
            account = full_registration_expert(form.data)
            if account:
                success = True
                Response(json.dumps({
                    'success': success}))
        return Response(json.dumps({
            'success': success}))


@api_view(['POST'])
def CheckAuthenticationView(request):
    print(request.session.items())
    if request.method == 'POST':
        if 'token' in request.POST:
            s = Session.objects.get(session_key=request.POST['token'])
            print(s.get_decoded())
            return Response(json.dumps({'auth_status': s.get_decoded()['active_session'],
                                        }))
        else:
            return Response(json.dumps({'auth_status': False,
                                        }))


@api_view(['GET', 'POST'])
def Clients(request):
    if 'role' in request.data:
        clients = []
        data = Client.objects.all()
        print(data)
        for client in data:
            clients.append(
                {'id': client.account.user.id, 'name': client.account.name, 'phone': client.account.phone, 'email': client.account.user.email})
        print(clients)
        return Response(json.dumps({
            'clients': clients}))


@api_view(['GET', 'POST'])
def Experts(request):
    if 'role' in request.data:
        experts = []
        data = Expert.objects.all()
        for expert in data:
            experts.append({'id':expert.id,'name': expert.user.name, 'phone': expert.user.phone, 'email': expert.user.user.email})
        return Response(json.dumps({
            'experts': experts}))

    if 'get_experts_for_lesson' in request.data:
        import datetime
        ids = []
        for i in request.data.getlist('experts'):
            ids.append(int(i))
        experts = Expert.objects.filter(id__in=request.data.getlist('experts'))
        date = datetime.datetime(int(request.data['year']),
                                 int(request.data['month']),
                                 int(request.data['day']),
                                 int(request.data['hour']),
                                 int(request.data['minute']))
        day = date.weekday() + 1
        time_start = date.time()
        time_end = (date + datetime.timedelta(hours=int(request.data['duration']))).time()
        calendars = ExpertCalendar.objects.filter(expert__in=experts,
                                                  day=day,
                                                  time_start__lte=time_start,
                                                  time_end__gte=time_end)
        expert = experts.filter(id__in=calendars.values_list('expert_id'))
        if expert:
            expert = expert.order_by('rating')[0].id
        else:
            expert = []
        return Response(json.dumps({
            'expert': expert}))
