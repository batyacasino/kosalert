import requests
from bs4 import BeautifulSoup
from re import findall

from .models import *

def test():
	print(get_data('10-135650/2020', 'Абдурахманов', '2'))

def html_to_list(content):
	soup = BeautifulSoup(content, "html.parser")
	rows = soup.find_all("tr")
	data = []
	for row in rows:
		cells = row.find_all("td")
		items = []
		for cel in cells:
			a = cel.find('a')		
			if a:
				href = a['href']
				link = f"https://www.mos-gorsud.ru{href}"
				items.append(link)
			else:
				items.append(cel.text.strip())
		data.append(items)
	return data[1:]
#lesbocoder@gmail.com otfpyypbN123

def get_data(client, casenumber, last_name, tabs):
	s = requests.Session()
	header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
	main_domain = 'https://www.mos-gorsud.ru'
#	https://www.mos-gorsud.ru/search?formType=shortForm&courtAlias=&uid=&instance=&processType=&letterNumber=&caseNumber=&participant=Борзаев+Х.А.+Росгосстрах
	url = f'{main_domain}/mgs/search?formType=shortForm&courtAlias=&caseNumber={casenumber}&participant={last_name}'
	r = requests.get(url, headers=header)
	soup = BeautifulSoup(r.text, 'lxml')
	tbody = soup.find('a', {'class':"detailsLink"})['href']
	url2 = f'{main_domain}{tbody}'
	
	url_msg = UrlMosgorsud.objects.filter(client_id=client.id)
	if not url_msg:
		UrlMosgorsud.objects.create(
						client_id=client,
						url_mosgorsud = url2,
						)

	r2 = requests.get(url2, headers=header)
	soup2 = BeautifulSoup(r2.text, 'lxml')
	div = soup2.find('div', {'id' : f'tabs-{tabs}'})
	tables = div.find_all('table', { 'class' : 'mainTable' })
	data = []
	if tabs == 1:		
		my_data1 = html_to_list(str(tables[0]))
		my_data2 = html_to_list(str(tables[1]))
		data.append(my_data1)
		data.append(my_data2)
		
	else:
		my_data1 = html_to_list(str(tables))
		data.append(my_data1)
	
	return data


def date_format(date):
	year = date[6:10]
	mounth = date[3:5]
	day = date[:2]
	return f'{year}-{mounth}-{day}'


def get_mosgordata(client):
	find_name = findall(r'[\w]+', client.claimant)
	for i in range(1, 4):
		try:
			mosgordata = get_data(client, client.case_number, find_name[0], i)
			for mosgor in mosgordata[0]:
				
				if i == 1:
					statemovements_db_creat(client, mosgor)
					
				if i == 2:

					courtsessions_db_creat(client, mosgor)
				if i == 3:
					judicialacts_db_creat(client, mosgor)					
		except:
			print(f'Нет таблицы {i}')

def create_db_allert(client, date, description):
	Alert.objects.create(
						client_id=client,
						date = date,
						description = description,
						)

def statemovements_db_creat(client, data):
	date_formate = date_format(data[0])

	statemovements_date = StateMovement.objects.filter(client_id=client)

	if statemovements_date:
		for statemovements_dt in statemovements_date:
			if statemovements_dt.condition == data[1]:
				return

	StateMovement.objects.create(
								client_id=client,
								date = date_formate,
								condition = data[1],
								document_base = data[2]
								)

	create_db_allert(client, date_formate, data[1])


def courtsessions_db_creat(client, data):
	date_formate = date_format(data[0])
	courtsessions_date = CourtSessions.objects.filter(client_id=client)
	if courtsessions_date:
		for courtsessions_dt in courtsessions_date:
			if courtsessions_dt.stage == data[2]:
				return

	CourtSessions.objects.create(
								client_id=client,
								date = date_formate,
								hall = data[1],
								stage = data[2],
								result = data[3],
								base = data[4],
								video_was_recorded = data[5],
								)

	create_db_allert(client, date_formate, data[2])

def judicialacts_db_creat(client, data):
	date_formate = date_format(data[0])
	judicialacts_date = JudicialActs.objects.filter(client_id=client)
	if judicialacts_date:
		for judicialacts_dt in judicialacts_date:
			if judicialacts_dt.type_of_document == data[1]:
				return

	JudicialActs.objects.create(
								client_id=client,
								date = date_formate,
								type_of_document = data[1],
								document_text = data[2],
								)

	create_db_allert(client, date_formate, data[1])


'''
def locationcasemovement_db_creat(client, data):
	date_formate = date_format(data['date'])
	locationcasemovement_date = LocationCaseMovement.objects.filter(date=date_formate)
	if locationcasemovement_date:
		for locationcasemovement_dt in locationcasemovement_date:
			if locationcasemovement_dt.location == data['location']:
				return

	LocationCaseMovement.objects.create(
										client_id=client,
										date = date_formate,
										location = data[1],
										comment = data[2]
										)
'''
