from django.shortcuts import render, get_object_or_404
from datetime import date, timedelta

from .models import *
from .forms import *

class ObjectDetailMixin:
	""" Миксин кабинета клиента """
	model = None
	template = None

	def get(self, request, pk):
		obj = get_object_or_404(self.model, pk=pk)
		email_count = app.email_counters(obj.email[:-15])
		files = ClientDocs.objects.filter(client_id=obj)
		reminders = Reminder.objects.filter(client_id=obj)
		client_reminders = []
		if reminders:
			for reminder in reminders:
				how_time = reminder.date_completion - date.today()
				remind = {
					'id':reminder.id,
					'description':reminder.description,
					'days_to_reminder':how_time.days}
				client_reminders.append(remind)

		return render(request, 'kosapp/detail_client.html', {
																"client": obj, 
																"files": files,
																'email_count':email_count,
																'reminders': client_reminders,
															})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        return render(request, self.template, {self.model.__name__.lower(): obj})

    def post(self, request, pk):
        obj = self.model.objects.get(id=pk)
        obj.delete()
        return redirect(reverse(self.redirect_url))
