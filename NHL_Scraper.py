import requests
import datetime
import matplotlib.pyplot as mp


class DailySchedule:

    def __init__(self, year, month, day):
        self.games = []
        self.date = datetime.date(year, month, day)
        self.get_daily_games()

    def get_daily_games(self):
        r = requests.get('https://statsapi.web.nhl.com/api/v1/schedule/?date={0}'.format(self.date))
        games_dictionary = r.json()
        self.games = games_dictionary['dates'][0]['games']

    def did_team_play(self, team_name):
        for game in self.games:
            teams = self.__get_teams__(game)
            if teams['homeTeam'].team_name == team_name or teams['awayTeam'].team_name == team_name:
                return True
        return False

    def get_game_by_teamname(self, team_name):
        for game in self.games:
            teams = self.__get_teams__(game)
            if teams['homeTeam'].team_name == team_name or teams['awayTeam'].team_name == team_name:
                gamefeed = self.__get_gamefeed__(game)
                return Game(Roster(teams['homeTeam'].team_name), Roster(teams['awayTeam'].team_name), gamefeed)
        return

    # Private Methods

    @staticmethod
    def __get_teams__(game):
        home_team = Roster(game['teams']['home']['team']['name'])
        away_team = Roster(game['teams']['away']['team']['name'])
        return {'homeTeam': home_team,
                'awayTeam': away_team}

    @staticmethod
    def __get_gamefeed__(game):
        gamelink = 'http://statsapi.web.nhl.com' + game['link']
        return requests.get(gamelink).json()


class Game:

    def __init__(self, roster1, roster2, game_feed):
        self.teams = (roster1, roster2)
        self.game_plays = []
        self.fill_rosters(game_feed['gameData']['players'])
        for play in game_feed['liveData']['plays']['allPlays']:
            if 'players' in play.keys():
                self.add_play(Play(play))

    def add_teams(self, roster1, roster2):
        self.teams = (roster1, roster2)

    def add_play(self, play):
        self.game_plays.append(play)

    def fill_rosters(self, player_list):
        for player in player_list:
            current_player = Player(player_list[player]['fullName'])
            if 'currentTeam' in player_list[player].keys() and player_list[player]['currentTeam']['name'] == self.teams[
                0].team_name:
                self.teams[0].team_players.append(current_player)
            elif 'currentTeam' in player_list[player].keys() and player_list[player]['currentTeam']['name'] == \
                    self.teams[1].team_name:
                self.teams[1].team_players.append(current_player)
            else:
                team_index = self.__ask_user_for_team__(current_player)
                self.teams[team_index - 1].team_players.append(current_player)

    def get_team_by_name(self, name):
        for team in self.teams:
            if team.team_name == name:
                return team
        return Roster("Invalid")

    def is_team_in_game(self, name):
        for team in self.teams:
            if team.team_name == name:
                return True
        return False

    def __ask_user_for_team__(self, player):
        while True:
            player_team = int(input("What team is {0} on?  Enter 1 for {1} or Enter 2 for {2}: ".format(player.name,
                self.teams[0].team_name, self.teams[1].team_name)))
            if 3 > player_team > 0:
                break
        return player_team


class Player:

    def __init__(self, name):
        self.name = name
        self.stats = {'shots': {'number': 0, 'locations': []},
                      'goals': 0,
                      'assists': 0,
                      'cf': 0,
                      'hits': 0,
                      'blocks': 0,
                      'faceoffs_taken': 0,
                      'faceoffs_won': 0,
                      'takeaways': 0,
                      'fights': 0,
                      'pen_drawn': 0,
                      'pen_taken': 0}

    def show_stats(self):
        # RIP this absolute beauty print({}.format(self.name), end = '')
        print(self.name, end='')
        print(self.stats)

    def update_stats(self, event, play_type, location):
        # this isn't working as a switch, so if/elif it is.
        if event == 'Shot':
            self.__update_shot__(play_type, location)
        elif event == 'Faceoff':
            self.__update_faceoff__(play_type)
        elif event == 'Hit':
            self.__update_hit__(play_type)
        elif event == 'Blocked Shot':
            self.__update_shotblock__(play_type)
        elif event == 'Takeaways':
            self.__update_takeaway__(play_type)
        elif event == 'Goal':
            self.__update_goal__(play_type)
        elif event == 'Penalty':
            self.__update_penalty__(play_type)
        elif event == 'Missed Shot':
            self.__update_shotattempt__()

    def get_shot_locations(self):
        # should I make this a tuple?
        return [self.get_shot_locations_x(), self.get_shot_locations_y()]

    def get_shot_locations_x(self):
        shot_locations_x = []
        locations = self.stats['shots']['locations']
        for location in locations:
            shot_locations_x.append(location['x'])
        return shot_locations_x

    def get_shot_locations_y(self):
        shot_locations_y = []
        locations = self.stats['shots']['locations']
        for location in locations:
            shot_locations_y.append(location['y'])
        return shot_locations_y

    # Private Methods

    def __update_penalty__(self, player_type):
        if player_type == 'PenaltyOn':
            self.stats['pen_taken'] += 1
        elif player_type == 'DrewBy':
            self.stats['pen_drawn'] += 1

    def __update_goal__(self, player_type):
        if player_type == 'Scorer':
            self.stats['goals'] += 1
            self.__update_shotattempt__()
        elif player_type == 'Assist':
            self.stats['assists'] += 1

    def __update_takeaway__(self, player_type):
        if player_type == 'PlayerID':
            self.stats['takeaways'] += 1

    def __update_shotattempt__(self):
        self.stats['cf'] += 1

    def __update_shotblock__(self, play_type):
        if play_type == 'Blocker':
            self.stats['blocks'] += 1
        if play_type == 'Shooter':
            self.__update_shotattempt__()

    def __update_shot__(self, play_type, location):
        print('Updating shot')
        if play_type == 'Shooter':
            self.stats['shots']['number'] += 1
            self.__update_shot_location(location)
            self.__update_shotattempt__()

    def __update_shot_location(self, location):
        self.stats['shots']['locations'].append(location)

    def __update_faceoff__(self, play_type):
        if play_type == 'Winner':
            self.stats['faceoffs_taken'] += 1
            self.stats['faceoffs_won'] += 1
        elif play_type == 'Loser':
            self.stats['faceoffs_taken'] += 1

    def __update_hit__(self, play_type):
        if play_type == 'Hitter':
            self.stats['hits'] += 1


class Roster:

    def __init__(self, team_name):
        self.team_name = team_name
        self.team_players = []
        self.team_stats = {"corsi": 0,
                           "cf": 0,
                           "ca": 0,
                           "penalties": 0,
                           "faceoffs_taken": 0,
                           "faceoffs_won": 0,
                           "shots": {'number': 0, 'locations': []},
                           "goals": 0}

    def is_player_on_team(self, potential_player_name):
        for player in self.team_players:
            if player.name == potential_player_name:
                return True
        return False

    def get_player_by_name(self, potential_player_name):
        for player in self.team_players:
            if player.name == potential_player_name:
                return player
        return "Invalid"

    def get_player_index(self, potential_player_name):
        for player in self.team_players:
            if player.name == potential_player_name:
                return self.team_players.index(player)
        return -1

    def update_team_stats(self):
        for player in self.team_players:
            self.__update_shots__(player)
            self.__update_goals__(player)
            self.__update_faceoffs__(player)

    def show_team_stats(self):
        print('Stats for {0}: \n\tShots: {1} \n\tGoals: {2}\n\tFaceoff Win%: {3}'.format(self.team_name, self.team_stats['shots']['number']
            , self.team_stats['goals'], (self.team_stats['faceoffs_won']/self.team_stats['faceoffs_taken']) * 100))

    # Private methods

    def __update_shots__(self, player):
        self.team_stats['shots']['number'] += player.stats['shots']['number']
        self.team_stats['shots']['locations'] += player.stats['shots']['locations']

    def __update_goals__(self, player):
        self.team_stats['goals'] += player.stats['goals']

    def __update_faceoffs__(self, player):
        self.team_stats['faceoffs_taken'] += player.stats['faceoffs_taken']
        self.team_stats['faceoffs_won'] += player.stats['faceoffs_won']


class Play:

    def __init__(self, play_dict):
        self.players = []
        self.event = ''
        self.play_coordinates = {'x': 0,
                                 'y': 0}
        self.__add_plays__(play_dict)

    def parse_play(self, teams):
        for team in teams:
            for player in self.players:
                if team.is_player_on_team(player['Name']):
                    # team.team_players[team.get_player_index(player['Name'])].update_stats(self.event, player['Type'],
                        #self.play_coordinates)
                    team.get_player_by_name(player['Name']).update_stats(self.event, player['Type'], self.play_coordinates)

    def __add_plays__(self, play_dict):
        print(play_dict)
        for player in play_dict['players']:
            player_name = player['player']['fullName']
            player_type = player['playerType']
            self.players.append({'Name': player_name, 'Type': player_type})
            self.event = play_dict['result']['event']
            self.play_coordinates.update(play_dict['coordinates'])
