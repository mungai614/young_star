from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Contribution, LoanInquiry

# Registration form
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Contribution form
class ContributionForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Member",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    month = forms.ChoiceField(
        choices=[(i, name) for i, name in [
            (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'),
            (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
        ]],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    year = forms.ChoiceField(
        choices=[(y, y) for y in range(2030, 2019, -1)],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'})
    )

    class Meta:
        model = Contribution
        fields = ['user', 'amount', 'month', 'year']

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        month = cleaned_data.get('month')
        year = cleaned_data.get('year')

        if all([user, month, year]):
            if Contribution.objects.filter(user=user, month=month, year=year).exists():
                raise forms.ValidationError(
                    f"Contribution for {month} {year} already exists for {user.username}."
                )

# Filter form for searching contributions
MONTH_CHOICES = [('', 'All Months')] + [(i, name) for i, name in [
    (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'),
    (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
]]
YEAR_CHOICES = [('', 'All Years')] + [(y, y) for y in range(2020, 2031)]

class ContributionFilterForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label="Member")
    month = forms.ChoiceField(choices=MONTH_CHOICES, required=False)
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)

# Loan inquiry form
class LoanInquiryForm(forms.ModelForm):
    class Meta:
        model = LoanInquiry
        fields = ['amount', 'reason', 'banked']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'banked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
