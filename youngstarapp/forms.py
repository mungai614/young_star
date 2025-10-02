# core/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Contribution

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ContributionForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Member",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    month = forms.ChoiceField(
        choices=[(m, m) for m in [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
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

from django import forms
from django.contrib.auth.models import User

MONTH_CHOICES = [
    ('', 'All Months'),
    ('January', 'January'), ('February', 'February'), ('March', 'March'),
    ('April', 'April'), ('May', 'May'), ('June', 'June'),
    ('July', 'July'), ('August', 'August'), ('September', 'September'),
    ('October', 'October'), ('November', 'November'), ('December', 'December')
]

YEAR_CHOICES = [('', 'All Years')] + [(str(y), str(y)) for y in range(2020, 2031)]

class ContributionFilterForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label="Member")
    month = forms.ChoiceField(choices=MONTH_CHOICES, required=False)
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
