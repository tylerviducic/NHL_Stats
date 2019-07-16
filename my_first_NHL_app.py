import requests
import NHL_Scrapper as scrap


# r = requests.get("https://statsapi.web.nhl.com/api/v1/teams/1/roster")
# roster_dict = r.json()
#
# devils = Roster('New Jersey Devils')
#
# for x in roster_dict['roster']:
#     devils.players.append(Player(x['person']['fullName']))
#     # print(x['person']['fullName'])



# print(roster_dict)
# person_list = roster_dict['roster']
# for person in person_list:
#     if person['person']['fullName'] == 'Taylor Hall':
#         print('8 More Years')

p = requests.get('https://statsapi.web.nhl.com/api/v1/schedule/?date=2019-04-01')
json_dict = p.json()

game_link = ''

#print(json_dict['dates'][0]['games'])
games = json_dict['dates'][0]['games']
for game in games:
    # print('game')
    #print(game['teams'])
    home_team = game['teams']['home']
    away_team = game['teams']['away']
    # print('home team:  ' + home_team['team']['name'])
    # print('away team:  ' + str(away_team))
    if 'New Jersey Devils' == home_team['team']['name'] or 'New Jersey Devils' == away_team['team']['name']:
        print('found game')
        #print(game)
        # print(home_team['team']['name'] + ': ' + str(home_team['score']) + "  " + away_team['team']['name'] + ':  ' +
        #       str(away_team['score']))
        game_link = 'http://statsapi.web.nhl.com' + game['link']

s = requests.get(game_link)
game_feed = s.json()
print(game_feed)

nyd = scrap.Roster('New Jersey Devils')
nyr = scrap.Roster('New York Rangers')
# game_players = game_feed['gameData']['players']

game = scrap.Game(nyd, nyr, game_feed)


# for plur in game_players:
#     plr = scrap.Player(game_players[plur]['fullName'])
#     if 'currentTeam' in game_players[plur].keys() and game_players[plur]['currentTeam']['name'] == nyd.team_name:
#         nyd.team_players.append(plr)
#     else:
#         nyr.team_players.append(plr)
#
# game = scrap.Game(nyd, nyr)

# plays = game_feed['liveData']['plays']['allPlays']

#Start here after you have both rosters set. Iterate over the events. Document all the possible playerTypes.
#assign stats based on what happens there.


# for play in plays:
#     if 'players' in play.keys():
#         game.add_play(scrap.Play(play))


for game_play in game.game_plays:
    game_play.parse_play(game)

for player in game.get_team_by_name("New Jersey Devils").team_players:
    player.show_stats()





