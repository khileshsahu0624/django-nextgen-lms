from django import forms
from .models import CustomUser

class InstructorCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-input', 'style': 'padding-right: 35px;'}), required=True, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-input', 'style': 'padding-right: 35px;'}), required=True, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'profile_photo', 'gender', 'dob', 'address', 'city', 'state', 'country', 'pincode',
            'bio', 'qualification', 'linkedin_link', 'facebook_link', 'twitter_link', 'is_active',
            'course', 'batch', 'admission_date', 
            'payment_amount', 'payment_date'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Password and Confirm Password do not match.")
        
        return cleaned_data

class InstructorChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'profile_photo', 'gender', 'dob', 'address', 'city', 'state', 'country', 'pincode',
            'bio', 'qualification', 'linkedin_link', 'facebook_link', 'twitter_link', 'is_active',
            'course', 'batch', 'admission_date', 
            'payment_amount', 'payment_date'
        ]

class StudentCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-input', 'style': 'padding-right: 35px;'}), required=True, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-input', 'style': 'padding-right: 35px;'}), required=True, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'profile_photo', 'gender', 'dob', 'address', 'city', 'state', 'country', 'pincode',
            'is_active', 'course', 'batch', 'admission_date', 'enrollment_status', 
            'payment_amount', 'payment_date', 'payment_status', 
            'guardian_name', 'guardian_phone',
            'linkedin_link', 'facebook_link', 'twitter_link'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Password and Confirm Password do not match.")
        
        return cleaned_data

class StudentChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'profile_photo', 'gender', 'dob', 'address', 'city', 'state', 'country', 'pincode',
            'is_active', 'course', 'batch', 'admission_date', 'enrollment_status', 
            'payment_amount', 'payment_date', 'payment_status', 
            'guardian_name', 'guardian_phone',
            'linkedin_link', 'facebook_link', 'twitter_link'
        ]

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-input', 'placeholder': 'Enter password'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-input', 'placeholder': 'Confirm password'}), required=True)

    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = ['is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login', 'groups', 'user_permissions', 'initial_password', 'student_code']
        widgets = {
            'role': forms.Select(attrs={'class': 'custom-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = ['is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login', 'groups', 'user_permissions', 'initial_password', 'student_code', 'password']
        widgets = {
            'role': forms.Select(attrs={'class': 'custom-input'}),
        }
