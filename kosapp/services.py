from random import randint
from transliterate import translit
from re import findall
from datetime import date, timedelta

from .models import *
from .yandex_pdd import app

def check_allert(allerts):
	client_allert = []
	try:
		for allert in allerts:
			client = Client.objects.filter(claimant=allert.client_id)
			for c_id in client:
				alrt = {
					'id': allert.id,
					'client_id': c_id.id,
					'date': allert.date,
					'client': allert.client_id,
					'description': allert.description}
				client_allert.append(alrt)
	except:
		client = Client.objects.filter(claimant=allerts.client_id)
		for c_id in client:
				alrt = {
					'id': allerts.id,
					'client_id': c_id.id,
					'date': allerts.date,
					'client': allerts.client_id,
					'description': allerts.description}
				return alrt
	return client_allert

def check_reminder(reminders):
	client_reminders = []
	for reminder in reminders:
		days_to_reminder = reminder.date_completion - date.today()
		if days_to_reminder.days <= 0:
			client = Client.objects.filter(claimant=reminder.client_id)
			for c_id in client:
				remind = {
					'client_id': c_id.id,
					'client': reminder.client_id,
					'description': reminder.description,
					'find_days': days_to_reminder.days}
				client_reminders.append(remind)
	return client_reminders


def check_email(clients):
	clients_list_email = []
	for client in clients:
		email_count = app.email_counters(client.email[:-15])
		if email_count['unread'] != 0:
			client_dict = {
				'id': client.id,
				'claimant': client.claimant,
				'email_count': email_count['unread']
			}
			clients_list_email.append(client_dict)
	return clients_list_email


def email_login(claimant):
	find_name = findall(r'[\w]+', claimant)
	unique_login = randint(1, 1000000)
	try:
		last_name = translit(find_name[0], reversed=True)
	except:
		last_name = find_name[0]
	return f'{last_name}{unique_login}'


def email_password():
	password = ''
	for n in range(randint(10, 16)):
		printable = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*'
		x = randint(0, len(printable) - 1)
		password += printable[x]
	return password