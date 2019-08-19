import requests
import NHL_Scraper as scrap
import matplotlib.pyplot as plt

# for play in plays:
#     if 'players' in play.keys():
#         game.add_play(scrap.Play(play))
daily_games = scrap.DailySchedule(2019, 4, 1)
# daily_games.show_all_games()
if daily_games.did_team_play('New Jersey Devils'):
    devils_game = daily_games.get_game_by_teamname('New Jersey Devils')


# for game_play in devils_game.game_plays:
#     game_play.parse_play(devils_game.teams)

# for player in devils_game.get_team_by_name("New Jersey Devils").team_players:
#     # player.show_stats()
#
# for player in devils_game.get_team_by_name("New York Rangers").team_players:
#    # player.show_stats()

devils = devils_game.get_team_by_name("New Jersey Devils")
# for player in devils.team_players:
#     player.show_stats()
# #     print(player.name)
# for goalie in devils.team_goalies:
#     goalie.show_stats()
devils.update_team_stats()
devils.show_team_stats()

# rangers = devils_game.get_team_by_name("New York Rangers")

devils_shots_x = []
devils_shots_y = []
rangers_shots = [[], []]


for player in devils.team_players:
    current_devils_shots_x, current_devils_shots_y = player.get_shot_locations()
    devils_shots_x += current_devils_shots_x
    devils_shots_y += current_devils_shots_y


# for player in rangers.team_players:
#     rangers_shots += player.get_shot_locations()


fig, ax1 = plt.subplots()
img = plt.imread('bev_rink_v1.jpg')
ax1.imshow(img, extent=[-100, 100, -43, 43])
plt.title("{}-{} Shot Map {}".format(devils_game.teams[0].team_name, devils_game.teams[1].team_name, daily_games.date))
devils_shots = (devils_shots_y, devils_shots_y)
ax1.plot(devils_shots_x, devils_shots_y, 'ro', marker='>')
# ax1.plot(np.array(rangers_shots), 'bo')


plt.show()




