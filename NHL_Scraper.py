import requests
import datetime
import matplotlib.pyplot as mp


# Created by Tyler Viducic
# I should be doing my research insteadclass Play:

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
                    team.get_player_by_name(player['Name']).update_stats(self.event, player['Type'], self.period,
                        self.play_coordinates)

    def __add_plays__(self, play_dict):
        for player in play_dict['players']:
            player_name = player['player']['fullName']
            player_type = player['playerType']
            self.players.append({'Name': player_name, 'Type': player_type})
            self.event = play_dict['result']['event']
            self.play_coordinates.update(play_dict['coordinates'])
            self.period = play_dict['about']['period']
# TODO Add goalies
# TODO add a season class for full season player analysis


class PlayerStats:

    def __init__(self):
        self.shots = []
        self.goals = []
        self.corsi_for = []
        self.assists = 0
        self.hits = 0
        self.blocks = 0
        self.faceoffs_taken = 0
        self.faceoffs_won = 0
        self.takeaways = 0
        self.fights = 0
        self.penalty_drawn = 0
        self.penalty_taken = 0

    def update_shot(self, period, location):
        self.shots.append({'period': period, 'location': location})

    def update_goal(self, period, location):
        self.goals.append({'period': period, 'location': location})

    def update_corsi_for(self, period, location):
        self.corsi_for.append({'period': period, 'location': location})

    def update_assist(self):
        self.assists += 1

    def update_hits(self):
        self.hits += 1

    def update_blocks(self):
        self.blocks += 1

    def update_faceoffs_taken(self):
        self.faceoffs_taken += 1

    def update_faceoffs_won(self):
        self.faceoffs_won += 1

    def update_takeaways(self):
        self.takeaways += 1

    def update_fights(self):
        self.fights += 1

    def update_pen_taken(self):
        self.penalty_taken += 1

    def update_pen_drawn(self):
        self.penalty_drawn += 1


class Player:

    def __init__(self, name):
        self.name = name
        self.stats = PlayerStats()

    def show_stats(self):
        # RIP this absolute beauty print({}.format(self.name), end = '')
        print(self.name + ':')
        print('''\t\tShots: {0:>8}
        Goals: {1:>8}
        Assists: {2:>6}
        Hits: {3:>9}
        Faceoffs: {4:>5}
        FO Won: {5:>7}
        '''.format(len(self.stats.shots) + len(self.stats.goals), len(self.stats.goals), self.stats.assists,
            self.stats.hits,
            self.stats.faceoffs_taken, self.stats.faceoffs_won))

    def update_stats(self, event, play_type, period, location):
        # this isn't working as a switch, so if/elif it is.
        if event == 'Shot':
            self.__update_shot__(play_type, period, location)
        elif event == 'Faceoff':
            self.__update_faceoff__(play_type)
        elif event == 'Hit':
            self.__update_hit__(play_type)
        elif event == 'Blocked Shot':
            self.__update_shotblock__(play_type, period, location)
        elif event == 'Takeaways':
            self.__update_takeaway__(play_type)
        elif event == 'Goal':
            self.__update_goal__(play_type, period, location)
        elif event == 'Penalty':
            self.__update_penalty__(play_type)
        elif event == 'Missed Shot':
            self.__update_shotattempt__(period, location)

    def get_shot_locations(self):
        return self.get_shot_locations_x(), self.get_shot_locations_y()

    def get_shot_locations_x(self):
        shot_locations_x = []
        shots = self.stats.shots
        for shot in shots:
            if shot['period'] == 2:
                shot_locations_x.append(-shot['location']['x'])
            else:
                shot_locations_x.append(shot['location']['x'])
        return shot_locations_x

    def get_shot_locations_y(self):
        shot_locations_y = []
        shots = self.stats.shots
        for shot in shots:
            if shot['period'] == 2:
                shot_locations_y.append(-shot['location']['y'])
            else:
                shot_locations_y.append(shot['location']['y'])
        return shot_locations_y

        # Private Methods

    def __update_penalty__(self, player_type):
        if player_type == 'PenaltyOn':
            self.stats.update_pen_taken()
        elif player_type == 'DrewBy':
            self.stats.update_pen_taken()

    def __update_goal__(self, player_type, period, location):
        if player_type == 'Scorer':
            self.stats.update_goal(period, location)
            self.__update_shotattempt__(period, location)
        elif player_type == 'Assist':
            self.stats.update_assist()

    def __update_takeaway__(self, player_type):
        if player_type == 'PlayerID':
            self.stats.update_takeaways()

    def __update_shotattempt__(self, period, location):
        self.stats.update_corsi_for(period, location)

    def __update_shotblock__(self, play_type, period, location):
        if play_type == 'Blocker':
            self.stats.update_blocks()
        if play_type == 'Shooter':
            self.__update_shotattempt__(period, location)

    def __update_shot__(self, play_type, period, location, ):
        if play_type == 'Shooter':
            self.stats.update_shot(period, location)
            self.__update_shotattempt__(period, location)

    def __update_faceoff__(self, play_type):
        if play_type == 'Winner':
            self.stats.update_faceoffs_taken()
            self.stats.update_faceoffs_won()
        elif play_type == 'Loser':
            self.stats.update_faceoffs_taken()

    def __update_hit__(self, play_type):
        if play_type == 'Hitter':
            self.stats.update_hits()


class TeamStats:

    def __init__(self):
        self.shots = []
        self.goals = []
        self.corsi_for = []
        self.hits = 0
        self.blocks = 0
        self.faceoffs_taken = 0
        self.faceoffs_won = 0
        self.takeaways = 0
        self.fights = 0
        self.penalty_drawn = 0
        self.penalty_taken = 0

    def update_shot(self, period, location):
        self.shots.append({'period': period, 'location': location})

    def update_goal(self, period, location):
        self.goals.append({'period': period, 'location': location})

    def update_corsi_for(self, period, location):
        self.corsi_for.append({'period': period, 'location': location})

    def update_hits(self):
        self.hits += 1

    def update_blocks(self):
        self.blocks += 1

    def update_faceoffs_taken(self):
        self.faceoffs_taken += 1

    def update_faceoffs_won(self):
        self.faceoffs_won += 1

    def update_takeaways(self):
        self.takeaways += 1

    def update_fights(self):
        self.fights += 1

    def update_pen_taken(self):
        self.penalty_taken += 1

    def update_pen_drawn(self):
        self.penalty_drawn += 1


class Roster:

    # TODO add a shotmap function
    def __init__(self, team_name, home_away, team_id):
        self.home_away = home_away
        self.team_name = team_name
        self.id = team_id
        self.team_players = []
        self.team_stats = TeamStats()

    def is_home(self):
        if self.home_away == 'home':
            return True
        else:
            return False

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
        print('Stats for {0}: \n\tShots: {1} \n\tGoals: {2}\n\tFaceoff Win%: {3}'.format(self.team_name,
            len(self.team_stats.shots) + len(self.team_stats.goals), len(self.team_stats.goals),
            (self.team_stats.faceoffs_won / self.team_stats.faceoffs_taken) * 100))

    # Private methods

    def __update_shots__(self, player):
        for shot in player.stats.shots:
            self.team_stats.update_shot(shot['period'], shot['location'])

    def __update_goals__(self, player):
        for goal in player.stats.goals:
            self.team_stats.update_goal(goal['period'], goal['location'])

    def __update_faceoffs__(self, player):
        self.team_stats.faceoffs_taken += player.stats.faceoffs_taken
        self.team_stats.faceoffs_won += player.stats.faceoffs_won


class DailySchedule:

    def __init__(self, year, month, day):
        self.date = datetime.date(year, month, day)
        self.games = self.get_daily_games()

    def get_daily_games(self):
        r = requests.get('https://statsapi.web.nhl.com/api/v1/schedule/?date={0}'.format(self.date))
        games_dictionary = r.json()
        return games_dictionary['dates'][0]['games']

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
                return Game(gamefeed)
        return

    # Private Methods

    @staticmethod
    def __get_teams__(game):
        home_team = Roster(game['teams']['home']['team']['name'], 'home', game['teams']['home']['team']['id'])
        away_team = Roster(game['teams']['away']['team']['name'], 'away', game['teams']['away']['team']['id'])
        return {'homeTeam': home_team,
                'awayTeam': away_team}

    @staticmethod
    def __get_gamefeed__(game):
        gamelink = 'http://statsapi.web.nhl.com' + game['link']
        return requests.get(gamelink).json()


class Game:

    def __init__(self, game_feed):
        self.date = datetime.datetime.strptime(game_feed['gameData']['datetime']['dateTime'],
            '%Y-%m-%dT%H:%M:%SZ').date()
        away_team = Roster(game_feed['gameData']['teams']['away']['name'], 'away', game_feed['gameData']['teams']\
            ['away']['id'])
        home_team = Roster(game_feed['gameData']['teams']['home']['name'], 'away', game_feed['gameData']['teams'] \
            ['home']['id'])
        self.teams = (home_team, away_team)
        self.game_plays = []
        self.fill_rosters(game_feed['gameData']['players'])
        for play in game_feed['liveData']['plays']['allPlays']:
            if 'players' in play.keys():
                self.add_play(Play(play))
        self.__parse_plays__()

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
                # team_index = self.__ask_user_for_team__(current_player)
                # self.teams[team_index - 1].team_players.append(current_player)
                self.__add_inactive__player__(current_player)

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

    def __parse_plays__(self):
        for play in self.game_plays:
            play.parse_play(self.teams)

    def __add_inactive__player__(self, player):
        for team in self.teams:
            season_roster = SeasonRoster(team, self.date)
            if season_roster.was_player_on_team(player.name):
                team.team_players.append(player)


class SeasonRoster:

    def __init__(self, roster, date):
        self.roster = roster
        self.date = date
        self.season = self.__get_season__(date)
        self.players = self.__get_players__()

    def was_player_on_team(self, player_name):
        if player_name in self.players:
            return True
        return False

    # Private Methods

    @staticmethod
    def __get_season__(date):
        if date.month >= 10:
            start_year = date.year
            end_year = date.year + 1
        else:
            start_year = date.year - 1
            end_year = date.year
        return '{}{}'.format(start_year, end_year)

    def __get_players__(self):
        team_dict = requests.get('https://statsapi.web.nhl.com/api/v1/teams/{}/?expand=team.roster&season={}'.format(
            self.roster.id, self.season)).json()
        players = []
        for person in team_dict['teams'][0]['roster']['roster']:
            players.append(person['person']['fullName'])
        return players
