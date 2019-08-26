import Scraper as scrape
import matplotlib.pyplot as plt

# TODO make tutorial

games = scrape.DailySchedule(2019, 4, 1)
if games.did_team_play("New Jersey Devils"):
    devils_game = games.get_game_by_teamname("New Jersey Devils")

for team in devils_game.teams:
    print(team.team_name)

devils = devils_game.get_team_by_name("New Jersey Devils")
# for player in devils.team_players:
#     player.show_stats()
# #     print(player.name)
# for goalie in devils.team_goalies:
#     goalie.show_stats()
devils.update_team_stats()
devils.show_team_stats()

# rangers = devils_game.get_team_by_name("New York Rangers")
predators = devils_game.get_home_team()
for player in predators.team_players:
    player.show_stats()

devils_shots_x = []
devils_shots_y = []
rangers_shots = [[], []]


for player in devils.team_players:
    current_devils_shots_x, current_devils_shots_y = player.get_shot_locations()
    devils_shots_x += current_devils_shots_x
    devils_shots_y += current_devils_shots_y



# fig, ax1 = plt.subplots()
# img = plt.imread('bev_rink_v1.jpg')
# ax1.imshow(img, extent=[-100, 100, -43, 43])
# plt.title("{}-{} Shot Map {}".format(devils_game.teams[0].team_name, devils_game.teams[1].team_name, daily_games.date))
# devils_shots = (devils_shots_y, devils_shots_y)
# ax1.plot(devils_shots_x, devils_shots_y, 'ro', marker='>')
# ax1.plot(np.array(rangers_shots), 'bo')


# plt.show()
