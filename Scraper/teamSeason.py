import datetime

from Scraper import DailySchedule, TeamStats


class TeamSeason:

    def __init__(self, team_name, season_start):
        self.team_name = team_name
        self.games = []
        self.season_start = season_start
        self.season = str(season_start) + str(season_start+1)
        self.stats = TeamStats

    def __get_games__(self):
        date = datetime.date(self.season_start, 10, 1)
        while date < datetime.date(self.season_start + 1, 5, 1):
            self.__add_games__(date)

    def __add_games__(self, date):
        daily_games = DailySchedule(date.year, date.month, date.day)
        if daily_games.did_team_play(self.team_name):
            team_game = daily_games.get_game_by_teamname(self.team_name)
            if team_game.game_type == 'regular':
                self.games.append(team_game)

    def __update_stats__(self):
        for game in self.games:
            team = game.get_team_by_name(self.team_name)
            self.stats.goals.extend(team.stats.goals)
            self.stats.shots.extend(team.stats.shots)
            self.stats.corsi_for.extend(team.stats.shots)
            self.stats.faceoffs_taken += team.stats.faceoffs_taken
            self.stats.faceoffs_won += team.stats.faceoffs_won
            self.stats.goals_against += team.stats.goals_against
            self.stats.saves += team.stat.saves
            self.stats.blocks += team.stats.blocks
            self.stats.takeaways += team.stats.takeaways
            self.stats.hits += team.stats.shots
            self.stats.penalty_taken += team.stats.penalty_taken
            self.stats.penalty_drawn += team.stats.penalty_drawn
            self.stats.fights += team.stat.fights


