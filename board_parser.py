import requests
import re
from bs4 import BeautifulSoup

def prettify(text):
	return text.strip().replace('\n', '').replace(' ', '')

def remove_trash(text):
	trash = re.findall('\([+|-][0-9]+\)', text)
	for t in trash:
		text = text.replace(t, '')
	return text

def get_services(soup):
	return [ service.text for service in soup.findAll('th', 'service_name') ]

def get_services_info(soup, services):
	services_html = soup.findAll('td', 'team_service')
	services_status = [ service['class'][1] for service in services_html ]
	services_sla = [ prettify(sla.find('div', 'param_value').text) for sla in soup.findAll('div', 'sla') ]
	services_fp = [ prettify(fp.find('div', 'param_value').text) for fp in soup.findAll('div', 'fp') ]
	services_flags = [ prettify(flags.find('div', 'param_value').text).split('/') for flags in soup.findAll('div', 'flags') ]
	services_flags = [ [ abs(int(i)) for i in flags ] if len(flags) == 2 else [int(flags[0]), 0] for flags in services_flags ]
	services_flags = [ { 'got': flags[0], 'lost': flags[1] } for flags in services_flags ]
	services_info = \
	[
		{
			'status': service_info[0],
			'sla': float(service_info[1][:-1]),
			'flag_points': float(service_info[2]),
			'flags': service_info[3],
		}
		for service_info in zip(services_status, services_sla, services_fp, services_flags)
	]
	return { services[number % len(services)]: info for number, info in enumerate(services_info) }


def get_teams_info(soup):
	services = get_services(soup)
	teams_html = soup.findAll('tr', attrs={'class': 'team'})[1:]
	teams = \
	[
		{
			'name': team.find('div', 'team_name').text.strip(),
			'place': int(remove_trash(team.find('td', 'place').text.strip())),
			'score': float(team.find('td', 'score').text.strip()),
			'ip': team.find('div', 'team_server').text.strip(),
			'info': get_services_info(team, services)
		}
		for team in teams_html
	]
	return teams

def get_current_round(soup):
	current_round = re.findall('[0-9]+', soup.find('div', attrs={'id': 'round'}).text.strip())[0]
	return int(current_round)

def get_soup_by_address(address):
	if not address.startswith('http'):
		address = 'http://' + address
	html = requests.get(address)

	return BeautifulSoup(html.text, 'html.parser')