import datetime

from Scraper.goalie import Goalie
from Scraper.play import Play
from Scraper.player import Player
from Scraper.roster import Roster
from Scraper.seasonRoster import SeasonRoster


class Game:

    def __init__(self, game_feed):
        print(game_feed)
        self.type = self.__get_game_type__(game_feed)
        self.date = datetime.datetime.strptime(game_feed['gameData']['datetime']['dateTime'],
                                               '%Y-%m-%dT%H:%M:%SZ').date()
        away_team = Roster(game_feed['gameData']['teams']['away']['name'], 'away', game_feed['gameData']['teams']
        ['away']['id'])
        home_team = Roster(game_feed['gameData']['teams']['home']['name'], 'away', game_feed['gameData']['teams']
        ['home']['id'])
        self.teams = (home_team, away_team)
        self.game_plays = []
        for play in game_feed['liveData']['plays']['allPlays']:
            if 'players' in play.keys():
                self.add_play(Play(play))
        self.fill_rosters(game_feed)
        self.__parse_plays__()

    def add_teams(self, roster1, roster2):
        self.teams = (roster1, roster2)

    def add_play(self, play):
        self.game_plays.append(play)

    def fill_rosters(self, game_feed):
        player_list = game_feed['gameData']['players']
        home_season_roster = SeasonRoster(self.get_home_team(), self.date)
        away_season_roster = SeasonRoster(self.get_away_team(), self.date)
        for player in player_list:
            player_name = player_list[player]['fullName']
            player_type = player_list[player]['primaryPosition']['type']
            if self.__was_player_traded__(player_name, home_season_roster, away_season_roster):
                self.__assign_traded_player__(player_name, player_type, game_feed)
            elif player_name in home_season_roster.players:
                self.add_to_team(self.teams[0], player_name, player_type)
            elif player_name in away_season_roster.players:
                self.add_to_team(self.teams[1], player_name, player_type)

    def add_to_team(self, team, player_name, player_type):
        if player_type != 'Goalie':
            player = Player(player_name)
            self.__add_player_to_team__(team, player)
        else:
            goalie = Goalie(player_name)
            self.__add_goalie_to_team__(team, goalie)

    def get_team_by_name(self, name):
        for team in self.teams:
            if team.team_name == name:
                return team
        return None

    def get_home_team(self):
        return self.teams[0]

    def get_away_team(self):
        return self.teams[1]

    def is_team_in_game(self, name):
        for team in self.teams:
            if team.team_name == name:
                return True
        return False

    # Private Methods
    @staticmethod
    def __was_player_traded__(player_name, season_roster1, season_roster2):
        if player_name in season_roster1.players and player_name in season_roster2.players:
            return True
        return False

    def __assign_traded_player__(self, player_name, player_type, game_feed):
        ignored_player_types = ['Hittee', 'Loser']
        for play in game_feed['liveData']['plays']['allPlays']:
            if 'players' in play.keys():
                for player in play['players']:
                    if player_name == player['player']['fullName'] and player['playerType'] not in ignored_player_types:
                        team_name = play['team']['name']
                        self.__add_by_team_name__(team_name, player_name, player_type)
                        return
        team_number = self.__ask_user_for_team__(Player(player_name))
        self.teams[team_number - 1].team_players.append(Player(player_name))

    def __add_by_team_name__(self, team_name, player_name, player_type):
        for team in self.teams:
            if team_name == team.team_name:
                self.add_to_team(team, player_name, player_type)

    @staticmethod
    def __add_player_to_team__(team, player):
        team.team_players.append(player)

    @staticmethod
    def __add_goalie_to_team__(team, goalie):
        team.team_goalies.append(goalie)

    def __ask_user_for_team__(self, player):
        while True:
            player_team = int(input("What team did {0} play for on {1}?  Enter 1 for {2} or Enter 2 for {3}: ".format(
                player.name, self.date, self.teams[0].team_name, self.teams[1].team_name)))
            if 3 > player_team > 0:
                break
        return player_team

    def __parse_plays__(self):
        for play in self.game_plays:
            play.parse_play(self.teams)

    def __get_game_type__(self, game_feed):
        dict_game_type = game_feed['gameData']['game']['type']
        game_type = self.__parse_game_type__(dict_game_type)
        return game_type

    @staticmethod
    def __parse_game_type__(game_type):
        if game_type == 'R':
            return 'regular'
        elif game_type == 'PR':
            return 'pre'
        else:
            return 'playoff'
