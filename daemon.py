import sys
import json
import game

"""Example of using this parser
   for calculating and reporting
   your team status."""

def follow(game_obj, team_ip):
	state = False
	while not state:
		state = game_obj.refresh()
	return game_obj.get_delta_by_ip(team_ip)

def generate_message(data):
	team_name = data['name']
	team_ip = data['ip']
	delta_place = data['place']
	delta_score = data['score']
	services_info = { key: info for key, info in data['info'].items() }
	message = f'Team: {team_name}, ip: {team_ip}\n'
	if delta_score > 0:
		message += f'You have earned {abs(delta_score)}.\n'
	elif delta_score < 0:
		message += f'You have lost {abs(delta_score)}.\n'

	message += 'Services report:\n'
	services_report = [f'{service}: +{info["flags"]["got"]} / -{info["flags"]["lost"]}, status {info["status"].replace("status_", "")}' for service, info in services_info.items()]
	message += '\n'.join(services_report)
	message += '\n\n'
	return message

args = sys.argv

if len(args) != 3:
	print('\n<Usage>: python3 {} scoreboard_ip team_ip\n'.format(args[0]))
	exit()

scoreboard = args[1]
team_ip = args[2]
AD = game.AD_Game(scoreboard)
AD.get_info_by_ip(team_ip)

while True:
	print(generate_message(follow(AD, team_ip)))

