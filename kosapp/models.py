from django.db import models
from django.shortcuts import reverse

class Client(models.Model):
	date_creat = models.DateField(auto_now_add=True)
	case_number = models.CharField(max_length=50, blank=True, null=True)
	claimant = models.CharField(max_length=200)
	date_of_birth = models.DateField()
	defendant = models.CharField(max_length=200)	
	email = models.EmailField(max_length=200)
	email_password = models.CharField(max_length=200)
	date_of_inspection = models.DateField()

	class Meta:
		ordering = ["-date_creat"]

	def __str__(self):
		return self.claimant


class ClientDocs(models.Model):
	client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
	claimant = models.CharField(max_length=200)
	document = models.FileField(upload_to='docs/pdfs/')

	def __str__(self):
		return self.claimant


class Reminder(models.Model):
	client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
	date_creat = models.DateField(auto_now_add=True)
	days_to_completion =  models.IntegerField()
	date_completion =   models.DateField()
	description = models.CharField(max_length=200)


class StateMovement(models.Model):
	client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
	date = models.DateField()
	condition = models.CharField(max_length=200)
	document_base = models.CharField(max_length=200, blank=True, null=True)
	url_mosgorsud = models.CharField(max_length=200, blank=True, null=True)

	class Meta:
		ordering = ["date"]





class CourtSessions(models.Model):
	client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
	date = models.DateField()
	hall = models.CharField(max_length=200)
	stage = models.CharField(max_length=200)
	result = models.CharField(max_length=200)
	base = models.CharField(max_length=200, blank=True, null=True)
	video_was_recorded = models.CharField(max_length=200, blank=True, null=True)
	url_mosgorsud = models.CharField(max_length=200, blank=True, null=True)

	class Meta:
		ordering = ["date"]


class JudicialActs(models.Model):
	client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
	date = models.DateField()
	type_of_document = models.CharField(max_length=200)
	document_text = models.CharField(max_length=200, blank=True, null=True)
	url_mosgorsud = models.CharField(max_length=200, blank=True, null=True)

	class Meta:
		ordering = ["date"]


class Alert(models.Model):
	client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
	date = models.DateField()
	description = models.CharField(max_length=200)


class UrlMosgorsud(models.Model):
	client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
	url_mosgorsud = models.CharField(max_length=200)


class LocationCaseMovement(models.Model):
	client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
	date = models.DateField()
	location = models.CharField(max_length=200)
	comment = models.CharField(max_length=200, blank=True, null=True)

	class Meta:
		ordering = ["date"]
