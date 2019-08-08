# hackerdom-board-parser
* This parser was created to make it easier to find out that your service is down or you are losing flags.
## Usage:
1. You can simply start daemon.py with scoreboard and team ip and get up to date statistics:

```python3 daemon.py scoreboard_ip team_ip```

2. You can import game.py into your project and get any statistics right in your python script:

```import game
ad = game.AD_Game(scoreboard_ip)
current_round = ad.round
team_info = ad.get_info_by_ip(team_ip)
team_info = ad.get_info_by_name(team_name) # Case insensetive
ad.refresh() # You have to manually refresh game state, it returns True if round has been changed
```
