from django import forms
from django.forms import ModelForm
from datetime import date, timedelta

from .models import *
from .yandex_pdd import app
from .services import *

class ClientForm(ModelForm):
	class Meta:
		model = Client
		fields = ('claimant', 'case_number','date_of_birth', 'defendant', 'date_of_inspection')
		widgets = {
			"claimant": forms.TextInput(attrs={'type':'text',  'class':'form-control text-center', 'placeholder':'Фамилия имя отчество'}),
			"case_number": forms.TextInput(attrs={'type':'text',  'class':'form-control text-center', 'placeholder':'Номер дела'}),
			"date_of_birth": forms.DateInput(attrs={'class':'form-control text-center', 'type':'date', 'id':'datepicker', 'data-date-format':"yyyy/mm/dd", 'placeholder':'Дата рождения'}),
			"defendant": forms.TextInput(attrs={'type':'text', 'class':'form-control text-center', 'placeholder':'Страховая компания'}),
			"date_of_inspection": forms.DateInput(attrs={'class':'form-control text-center', 'type':'date', 'id':'datepicker', 'data-date-format':"yyyy/mm/dd", 'placeholder':'Дата осмотра'}),
			}


class UploadDocsForm(ModelForm):
	class Meta:
		model = ClientDocs
		fields = ('claimant', 'document')
		widgets = {
			"claimant": forms.TextInput(attrs={'class':'form-control text-center', 'placeholder':'Введите название файла'}),
			"document": forms.FileInput(attrs={"class": "custom-file-input", 'type':"file", 'id':"customFileLang", 'lang':"ru"})
			}


class ReminderForm(ModelForm):
	class Meta:
		model = Reminder
		fields = ('days_to_completion', 'description')
		widgets = {
			"description": forms.TextInput(attrs={'class':'form-control text-center', 'placeholder':'Описание'})}		


