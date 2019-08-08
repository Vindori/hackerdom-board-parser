from time import sleep
import board_parser

class AD_Game(object):
	"""This class is combined with 
	   pasrser of HackerDom's A&D scoreboard."""
	def __init__(self, ip):
		global soup, info, delta
		delta = []
		self.ip = ip
		soup = board_parser.get_soup_by_address(self.ip)
		self.round = board_parser.get_current_round(soup)
		info = board_parser.get_teams_info(soup)

	def get_info_by_name(self, name):
		for team in info:
			if team['name'].lower() == name.lower():
				return team
		raise KeyError(f"There is no {name} team")

	def get_info_by_ip(self, ip):
		for team in info:
			if team['ip'] == ip:
				return team
		raise KeyError(f"There is no team with ip {ip}")

	def get_delta_by_name(self, name):
		for team in delta:
			if team['name'] == name:
				return team
		raise KeyError(f"There is no {name} team")

	def get_delta_by_ip(self, ip):
		for team in delta:
			if team['ip'] == ip:
				return team
		raise KeyError(f"There is no team with ip {ip}")



	def refresh(self): # returns True if refreshed
		global info

		new_soup = board_parser.get_soup_by_address(self.ip)
		new_info = board_parser.get_teams_info(new_soup)
		current_round = board_parser.get_current_round(new_soup)
		if self.round != current_round:
			self.__recalculate_delta(new_info)
			info = new_info.copy()
			self.round = current_round
			return True
		else:
			return False

	def __recalculate_delta(self, new_info):
		global delta
		delta = []
		for team_new in new_info:
			try:
				team_old = self.get_info_by_ip(team_new['ip'])
				services = board_parser.get_services(soup)
				delta_services = {}
				for service in services:
					team_got_new_flags = team_new['info'][service]['flags']['got'] \
										 - team_old['info'][service]['flags']['got']
					team_lost_new_flags = team_new['info'][service]['flags']['lost'] \
										  - team_old['info'][service]['flags']['lost']

					delta_services[service] = {
												'status': team_new['info'][service]['status'],
												'flags': {
															 'got': team_got_new_flags, # can't be negative
															 'lost': team_lost_new_flags # can't be negative
														 }
											  }

				delta.append(
								{
									'name': team_new['name'], # it's not delta, actually
									'ip': team_new['ip'], # and this, as well
									'place': team_old['place'] - team_new['place'], # if positive then up, if negative then down
									'score': round(team_new['score'] - team_old['score'], 2), # if positive then more score
									'info': delta_services
								}
							)
			except KeyError as e:
				continue

