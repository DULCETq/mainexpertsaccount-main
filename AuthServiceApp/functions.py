from .models import Account, Client, Education, Expert
from django.contrib.auth.models import User
import requests
import json
import sys


def register(form_data):
    try:
        name = '{} {}'.format(form_data['name'], form_data['lname']) if 'lname' in form_data else form_data['name']
        if not User.objects.filter(email=form_data['email']):
            user = User.objects.create(username=form_data['email'],
                                       email=form_data['email'],
                                       password=form_data['password'])
        else:
            return {'success': False, 'error': 'User already exists'}
        if not Account.objects.filter(user=user):
            account = Account.objects.create(user=user,
                                             user_type=form_data['user_type'],
                                             phone=form_data['phone'],
                                             name=name,
                                             is_active=True,
                                             available_balance=0,
                                             age=0)

        else:
            account = Account.objects.get(user=user)
            account.user_type = form_data['user_type']
            account.phone = form_data['phone']
            account.name = name
            account.is_active = True
            account.available_balance = 0
            account.age = 0
            account.save()
        if form_data['user_type'] == 'Expert':
            if not Client.objects.filter(account=account):

                Expert.objects.get_or_create(user=account)
            else:
                return {'success': False, 'error': 'This user is already registered as expert'}

        elif form_data['user_type'] == 'Client':
            if not Expert.objects.filter(user=account):
                client, _ = Client.objects.get_or_create(account=account)
                client.fname = form_data['name']
                client.lname = form_data['lname']
                client.save()
            else:
                return {'success': False, 'error': 'This user is already registered as expert'}
        return {'success': True, 'error': None, 'account': account}
    except Exception as e:
        print(e)
        print(sys.exc_info()[2])
        return {'success': False, 'error': str(e)}


def full_registration_client(form_data, avatar):
    try:
        user = Account.objects.get(user_id=form_data['client_id'])
    except:
        error = 'User not found'
        return {'success': False, 'error': error}
    user.phone = form_data['phone']
    if avatar:
        user.avatar = avatar
    user.save()
    if Client.objects.filter(account=user):
        client = Client.objects.get(account=user)
        client.goals = form_data['goals'] if 'goals' in form_data else None
        client.fav_lessons = form_data['favorite_lessons'] if 'favorite_lessons' in form_data else None
        client.birth = form_data['birth']
        client.fname = form_data['fname']
        client.lname = form_data['lname']
        client.home_address = form_data['home_address']
        client.location_2_address = form_data['location_2_address'] if 'location_2_address' in form_data else None
        client.location_2_name = form_data['location_2_name'] if 'location_2_name' in form_data else None
        client.save()
        user.name = '{} {}'.format(form_data['fname'], form_data['lname'])
        user.save()
    else:
        Client.objects.create(account=user,
                              goals=form_data['goals'] if 'goals' in form_data else None,
                              fav_lessons=form_data['favorite_lessons'] if 'favorite_lessons' in form_data else None,
                              birth=form_data['birth'],
                              fname=form_data['fname'],
                              lname=form_data['lname'],
                              home_address=form_data['home_address'],
                              location_2_address=form_data['location_2_address'],
                              location_2_name=form_data['location_2_name'],
                              )
    if 'place_of_study_name' in form_data:
        Education.objects.create(user=user,
                                 education_type=form_data['education_type'],
                                 place_of_study_name=form_data['place_of_study_name'],
                                 date_start=form_data['education_date_start'],
                                 date_end=form_data['education_date_end'], )
    return True


def full_registration_expert(form_data):
    if not 'expert_id' in form_data:
        user = Account.objects.get(user_id=form_data['client_id'])
        expert = Expert.objects.get_or_create(user=user)
    else:
        expert = Expert.objects.get(id=form_data['expert_id'])
        user = expert.user

    '''expert.skills = form_data['expert']['skills'] if 'skills' in form_data['expert'] else ''
    expert.personal_description = form_data['expert']['personal_description'] if 'personal_description' in form_data[
        'expert'] else ''
    expert.additional_info = form_data['expert']['additional_info'] if 'additional_info' in form_data['expert'] else ''
    '''
    expert.lname = form_data['lname']
    expert.fname = form_data['fname']
    expert.save()
    user.user.email = form_data['email']
    user.user.save()
    return True


def attach_subjects_to_expert(form_data):
    subjects = form_data['subjects']
    print(subjects)
    for subject in subjects:
        subject['expert'] = form_data['client_id']
        print(subject)
        res = requests.post('http://206.81.25.251:8001/booking/expert/subject', data=json.dumps(subject))
        print(res)
    return True


def update_data_client(form_data):
    user = Account.objects.get(user_id=form_data['client_id'])
    client = Client.objects.get(account=user).update(goals=form_data['goals'],
                                                     fav_lessons=form_data['favorite_lessons']
                                                     )
    Education.objects.get(account=user).update(
        education_type=form_data['education_type'],
        place_of_study_name=form_data['place_of_study_name'],
        date_start=form_data['education_date_start'],
        date_end=form_data['education_date_end'], )
    return client
