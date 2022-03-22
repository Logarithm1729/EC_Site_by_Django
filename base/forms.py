from django import forms
from django.contrib.auth import get_user_model


class UserCreationForm(forms.ModelForm):
    password2 = forms.CharField(label='確認用パスワード', required=True, widget=forms.PasswordInput(attrs={'placeholder': '確認用パスワード'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'パスワード'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder': 'ユーザー名'}
        self.fields['email'].widget.attrs = {'placeholder': 'Eメール'}
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("※パスワードと確認用パスワードが合致しません。")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


#学習用
class LoginForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder': 'ユーザー名'}
        self.fields['password'].widget.attrs = {'placeholder': 'パスワード'}
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            self.user = get_user_model().objects.get(username=username)
            # password = get_user_model().objects.get(password=password)
        except:
            forms.ValidationError('ユーザー名もしくはパスワードが違います。再確認してください。')
        
        if not self.user.check_password(password):
            raise forms.ValidationError('正しいパスワードを入力してください')
    
    def get_user(self):
        return self.user
