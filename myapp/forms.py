from django import forms
from .models import School, Collage, Hospital, Bank

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'

class CollageForm(forms.ModelForm):
    class Meta:
        model = Collage
        fields = '__all__'

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = '__all__'
