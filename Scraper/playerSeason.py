import datetime

from Scraper.dailySchedule import DailySchedule


class PlayerSeason:

    def __init__(self, player_name, player_team, season_start_year):
        self.player_name = player_name
        self.player_team = player_team
        self.season_start = season_start_year
        self.games_list = []
        self.__get_games_list__(self.season_start)

    # Private methods

    def __get_games_list__(self, season_start):
        date = datetime.date(season_start, 10, 1)
        while date < datetime.date(season_start + 1, 4, 5):
            self.__add_players_games__(date)
            date += 1

    def __add_players_games__(self, date):
        daily_games = DailySchedule(date.year, date.month, date.day)
        if daily_games.did_team_play(self.player_team):
            self.games_list.append(daily_games.get_game_by_teamname(self.player_team))