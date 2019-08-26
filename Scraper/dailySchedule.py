import datetime
import requests

from Scraper.game import Game
from Scraper.roster import Roster


class DailySchedule:

    def __init__(self, year, month, day):
        self.date = datetime.date(year, month, day)
        self.games = self.get_daily_games()

    def get_daily_games(self):
        r = requests.get('https://statsapi.web.nhl.com/api/v1/schedule/?date={0}'.format(self.date))
        games_dictionary = r.json()
        return games_dictionary['dates'][0]['games']

    def show_all_games(self):
        print('Games played on {}'.format(self.date))
        print("*" * 45)
        for game in self.games:
            print('{} @ {}'.format(game['teams']['away']['team']['name'], game['teams']['home']['team']['name']))

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