from django import forms
from .models import Account
from django.contrib.auth.models import User
from django.contrib.postgres.forms import SimpleArrayField


class LoginForm(forms.Form):
    """форма авторизации"""
    username = forms.CharField()
    password = forms.CharField()


class RegisterForm(forms.Form):
    """форма регистрации аккаунта"""
    user_type = forms.CharField()
    phone = forms.CharField()
    email = forms.CharField()
    name = forms.CharField()
    lname = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_phone(self):
        """метод очистки телефона от лишних символов"""
        phone = self.cleaned_data['phone']
        phone = phone.split('-')
        phone[1] = phone[1][1:-1]
        clean_phone = ''.join(phone)
        if Account.objects.filter(phone=clean_phone).exists():
            raise forms.ValidationError(u'Phone "%s" is already in use.' % phone)
        return clean_phone

    def clean_email(self):
        """метод проверки email на уникальность"""
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(u'Email "%s" is already in use.' % email)
        return email


class ResetForm(forms.Form):
    """форма сброса пароля"""
    phone = forms.CharField()
    email = forms.CharField()


class ClientFullRegistrationForm(forms.Form):
    """форма полной регистрации клиента для работы с сервисом и брони занятия"""
    client_id = forms.CharField()
    fname = forms.CharField()
    lname = forms.CharField()
    phone = forms.CharField(required=False)
    email = forms.CharField(required=False)
    place_of_study_name = forms.CharField(required=False)
    education_date_start = forms.DateField(required=False)
    education_date_end = forms.DateField(required=False)
    education_type = forms.CharField(required=False)
    location_2_address = forms.CharField(required=False)
    location_2_name = forms.CharField(required=False)
    home_address = forms.CharField(required=False)
    birth = forms.DateField(required=False)
    favorite_lessons = SimpleArrayField(forms.CharField(max_length=100, required=False), required=False)
    goals = SimpleArrayField(forms.CharField(max_length=100), required=False)


class ExpertFullRegistrationForm(forms.Form):
    """форма полной регистрации клиента для работы с сервисом и брони занятия"""
    fname = forms.CharField()
    lname = forms.CharField()
    phone = forms.CharField()
    email = forms.CharField()
    locations = SimpleArrayField(forms.CharField(max_length=100, required=False), required=False)
    subjects = SimpleArrayField(forms.CharField(max_length=100), required=False)

    def clean_phone(self):
        """метод очистки телефона от лишних символов"""
        phone = self.cleaned_data['phone']
        phone = phone.split('-')
        phone[1] = phone[1][1:-1]
        clean_phone = ''.join(phone)
        if User.objects.filter(username=clean_phone).exists():
            raise forms.ValidationError(u'Phone "%s" is already in use.' % phone)
        return clean_phone


'''class ExpertFullRegistrationForm(forms.Form):
    """форма полной регистрации клиента для работы с сервисом и брони занятия"""
    client_id = forms.CharField()
    place_of_study_name = forms.CharField(required=False)
    education_date_start = forms.DateField()
    education_date_end = forms.DateField()
    education_type = forms.CharField()
    favorite_lessons = SimpleArrayField(forms.CharField(max_length=100, required=False), required=False)
    goals = SimpleArrayField(forms.CharField(max_length=100), required=False)'''

class CheckAuthenticationForm(forms.Form):
    """форма проверки авторизации"""
    client_id = forms.CharField()
