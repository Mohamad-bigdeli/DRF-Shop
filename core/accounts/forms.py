from django import forms
from .models import ShopUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class ShopUserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model = ShopUser
        fields = ["phone", "email", "is_verified"]

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("passwords doesn't match")

        return password1

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if ShopUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone already exist.")
        if not phone.isdigit():
            raise forms.ValidationError("Invalid phone number.")
        if not phone.startswith("09"):
            raise forms.ValidationError("Phone must start with 09 digits.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class ShopUserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = ShopUser
        fields = ["phone", "email", "is_verified", "is_active"]

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Phone already exist.')
        else:
            if ShopUser.objects.filter(phone=phone).exists(): 
                raise forms.ValidationError('Phone already exist.')
        if not phone.isdigit():
            raise forms.ValidationError("Invalid phone number.")
        if not phone.startswith("09"):
            raise forms.ValidationError("Phone must start with 09 digits.")
        return phone