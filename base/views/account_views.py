from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.template.response import TemplateResponse
from django.contrib.auth import login
from django.urls import reverse
from django.contrib import messages

from base.models import Profile
from base.forms import UserCreationForm, LoginForm


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = '/login/'
    template_name = 'pages/signup.html'

    def form_valid(self, form):
        messages.warning(self.request, '登録が完了しました。次にログインしてください')
        return super().form_valid(form)

class Login(LoginView):
    success_url = '/'
    template_name = 'pages/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'ログインしました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '入力情報に誤りがあります。')
        return super().form_invalid(form)

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'pages/account.html'
    fields = ['username', 'email']
    success_url = '/account/'

    def get_object(self):
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'pages/profile.html'
    success_url = '/profile/'
    fields = ['first_name', 'last_name', 'zipcode', 'prefecture',
              'address1', 'address2', 'phone_num']
    
    def get_object(self):
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()