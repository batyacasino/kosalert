from django.urls import path
from .views import *




urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('delete_alert/<int:pk>/', DeleteAlertView.as_view(), name='delete_alert_url'),
	path('delete_all/', deleteall, name='deleteall'),
	path('test/', test, name='test'),
	path('client_list/', client_list, name='client_list_url'),	
	path('add_client/', AddClient.as_view(), name='add_client_url'),
	path('detail_client/<int:pk>/', ClientDetail.as_view(), name='detail_client_url'),
	path('detail_client/<int:pk>/upload_docs/', UploadDocs.as_view(), name='upload_docs_url'),
	path('detail_client/<int:pk>/yandex_oauth/', yandex_oauth, name='yandex_oauth_url'),
	path('detail_client/<int:pk>/reminder/', ReminderView.as_view(), name='reminder_url'),
	path('detail_client/<int:pk>/delete_reminder/', DeleteReminderView.as_view(), name='delete_reminder_url'),
	
	path('detail_client/<int:pk>/mosgorsud_progress/', MosgorsudView.as_view(), name='mosgorsud_view_url'),


]

