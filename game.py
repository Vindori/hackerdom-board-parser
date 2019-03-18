from time import sleep
import parser

def ref(obj):
	obj.refresh()


class AD_Game(object):
	"""This class is combined with 
	pasrser of HackerDom's A&D scoreboard."""
	def __init__(self, ip):
		self.ip = ip
		global info, rounds
		info, rounds = parser.get_by_address(self.ip)
		self.rounds = rounds
		self.teams = [team_info['name'] for team_info in info]		

	def refresh(self):
		info, rounds = parser.get_by_address(self.ip)
		self.teams = [team_info['name'] for team_info in info]

	def info_by_name(self, name):
		for team in info:
			if team['name'] == name:
				return team
		return None

	def info_by_ip(self, ip):
		for team in info:
			if team['ip'] == ip:
				return team
		return None

	def refresh(self):
		info, rounds = parser.get_by_address(self.ip)
		self.teams = [team_info['name'] for team_info in info]
		self.rounds = rounds
		print('ok. refreshed')


current = AD_Game('scoreboard.spb.ctf.su')
print(current.teams)
