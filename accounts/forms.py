from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email manzilingiz'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label="Ism",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Familiya",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangiz'})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': "O'zingiz haqida qisqacha ma'lumot kiriting...",
                'maxlength': 500,
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
            }),
        }
        labels = {
            'bio': "O'zingiz haqida",
            'avatar': "Profil rasmi",
            'website': "Veb-sayt",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            self.user.save()
        if commit:
            profile.save()
        return profile
