from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView
from django.core.files.storage import FileSystemStorage
from random import randint
from datetime import date, timedelta
from django.db.models import Q
from urllib.parse import unquote

from .models import *
from .forms import *
from .utils import *
from .yandex_pdd import app
from .services import *
from .mosgorsud import *

def client_list(request):
	""" Список клиентов """
	search_id = request.GET.get('search_id', '')
	search_case = request.GET.get('search_case', '')
	search_fio = request.GET.get('search_fio', '')
	if search_id:
		clients = Client.objects.filter(id__icontains=search_id)
	elif search_case:
		clients = Client.objects.filter(case_number__icontains=search_case)
	elif search_fio:
		clients = Client.objects.filter(claimant__icontains=search_fio)		
	else:
		clients = Client.objects.all()
	return render(request, 'kosapp/client_list.html', {'clients': clients})

class Index(View):
	""" Главная страница """
	def get(self, request):
		all_reminder = Reminder.objects.all()
		all_client = Client.objects.all()
		all_allert = Alert.objects.all()
		reminders = check_reminder(all_reminder)
		emails = check_email(all_client)
		allerts = check_allert(all_allert)
		return render(request, 'kosapp/index.html', {
													'reminders': reminders,
													'len_reminders': len(reminders),
													'emails': emails,
													'len_emails': len(emails),
													'allerts': allerts,
													'len_allert': len(allerts),
													})
'''
Номер дела:

02-1946/2019
Клиент:

Волков Роман Владимирович
дата рождения:

12 декабря 1960 г.
Страховая компания:

СПАО "Ингосстрах"
Дата осмотра:

16 июля 2020 г.
'''

def yandex_oauth(request, pk):
	""" Авторизация в почте """
	client = Client.objects.get(id=pk)
	link = app.passport_oauth('https://mail.yandex.ru/', email=client.email)
	return render(request, 'kosapp/yandex_oauth.html', {'link':link[1:]})


class ClientDetail(ObjectDetailMixin, View):
	""" Кабинет клиента """
	model = Client
	template = 'kosapp/detail_client.html'


class AddClient(View):
	""" Добавление клиента """
	def get(self, request):
		form = ClientForm()
		return render(request, 'kosapp/add_client.html', {"form": form})

	def post(self, request):
		form = ClientForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			login = email_login(form.claimant)
			password = email_password()
			app.email_add(login, password)
			form.email = f'{login}@botpromokot.ru'
			form.email_password = password
			form.save()
		return redirect(f"/detail_client/{form.id}")


class UploadDocs(View):
	""" Загрузка документа """
	def get(self, request, pk):
		client = Client.objects.get(id=pk)
		form = UploadDocsForm()
		return render(request, 'kosapp/upload_docs.html', {"form": form, "client": client})

	def post(self, request, pk):
		form = UploadDocsForm(request.POST, request.FILES)
		client = Client.objects.get(id=pk)
		if form.is_valid():
			form = form.save(commit=False)
			form.client_id = Client.objects.get(id=pk)
			form.save()
		return redirect(f"/detail_client/{pk}")


class ReminderView(View):
	""" Добавить напоминание """
	def get(self, request, pk):
		client = Client.objects.get(id=pk)
		form = ReminderForm()
		return render(request, 'kosapp/reminder.html', {"form": form, "client": client})

	def post(self, request, pk):
		form = ReminderForm(request.POST)
		client = Client.objects.filter(id=pk)
		if form.is_valid():
			form = form.save(commit=False)
			form.date_completion =  date.today() + timedelta(days=int(form.days_to_completion))
			form.client_id = Client.objects.get(id=pk)
			form.save()
		return redirect(f"/detail_client/{pk}")

class DeleteReminderView(View):
	""" Удалить напоминание """
	def get(self, request, pk):
		reminder = Reminder.objects.get(id=pk)
		return render(request, 'kosapp/delete_reminder.html',{"reminder": reminder})

	def post(self, request, pk):
		reminder = Reminder.objects.get(id=pk)
		clients = Client.objects.filter(claimant=reminder.client_id)
		reminder.delete()
		for client in clients:
			return redirect(f"/detail_client/{client.id}")

class DeleteAlertView(View):
	""" Удалить напоминание """
	def get(self, request, pk):
		alert = Alert.objects.get(id=pk)
		client = Client.objects.filter(claimant=alert.client_id)
		for i in client:
			url_msg = UrlMosgorsud.objects.filter(client_id=i.id)
		return render(request, 'kosapp/delete_alert.html',{"alert": alert,
															"client": client,
															'url_msg': url_msg
															})

	def post(self, request, pk):
		alert = Alert.objects.get(id=pk)
		clients = Client.objects.filter(claimant=alert.client_id)
		alert.delete()
		for client in clients:
			return redirect(f"/detail_client/{client.id}/mosgorsud_progress")

class MosgorsudView(View):
	""" Мосгорсуд """
	def get(self, request, pk):
		client = Client.objects.get(id=pk)
		get_mosgordata(client)
		statemovements = StateMovement.objects.filter(client_id=client)
		courtsessions = CourtSessions.objects.filter(client_id=client)
		judicialacts = JudicialActs.objects.filter(client_id=client)

		return render(request, 'kosapp/mosgorsud_progress.html', 
			{
			"statemovements": statemovements,
			'courtsessions': courtsessions,
			'judicialacts': judicialacts
			})
		

def test(request):
	client = Client.objects.get(id=8)
	get_mosgordata(client)
	statemovements = JudicialActs.objects.filter(client_id=client)
	print(len(statemovements))
	for i in statemovements:
		try:
			print(i.document_text)
		except:
			print('huy')
	
	return redirect("/")


def deleteall(request):
	""" Пизда базе """
	client = Client.objects.all().delete()
	return redirect("/")

