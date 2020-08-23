import requests
from bs4 import BeautifulSoup

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

def get_msg(casenumber, client, tabs):
	s = requests.Session()
	header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
	main_domain = 'https://www.mos-gorsud.ru'
	url = f'{main_domain}/mgs/search?formType=shortForm&courtAlias=&caseNumber={casenumber}&participant={client}'
	r = requests.get(url, headers=header)
	soup = BeautifulSoup(r.text, 'lxml')
	tbody = soup.find('a', {'class':"detailsLink"})['href']
	url2 = f'{main_domain}{tbody}'

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

data = get_msg('02-1946/2019', 'Волков', 1)


data = data[0][0][0]
year = data[6:10]
mounth = data[3:5]
day = data[:2]
date_formate = f'{year}-{mounth}-{day}'
print(date_formate)
