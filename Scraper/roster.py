from Scraper.teamStats import TeamStats


class Roster:

    def __init__(self, team_name, home_away, team_id):
        self.home_away = home_away
        self.team_name = team_name
        self.id = team_id
        self.team_players = []
        self.team_goalies = []
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

    def is_goalie_on_team(self, potential_goalie_name):
        for goalie in self.team_goalies:
            if goalie.name == potential_goalie_name:
                return True
            return False

    def get_player_by_name(self, potential_player_name):
        for player in self.team_players:
            if player.name == potential_player_name:
                return player
        return None

    def get_goalie_by_name(self, potential_goalie_name):
        for goalie in self.team_goalies:
            if goalie.name == potential_goalie_name:
                return goalie
        return None

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
        for goalie in self.team_goalies:
            self.__update_saves__(goalie)
            self.__update_goals_against__(goalie)

    def show_team_stats(self):
        try:
            print('Stats for {0}: \n\tShots: {1} \n\tGoals: {2}\n\tFaceoff Win%: {3} \n\tSave%:'.format(self.team_name,
                                    len(self.team_stats.shots) + len(self.team_stats.goals), len(self.team_stats.goals),
                                    (self.team_stats.faceoffs_won / self.team_stats.faceoffs_taken) * 100),
                  self.team_stats.saves/(self.team_stats.goals_against + self.team_stats.saves))
        except ZeroDivisionError:  # Print saves instead of save%
            print('Stats for {0}: \n\tShots: {1} \n\tGoals: {2}\n\tFaceoff Win%: {3} \n\tSaves:'.format(self.team_name,
                                    len(self.team_stats.shots) + len(self.team_stats.goals), len(self.team_stats.goals),
                        (self.team_stats.faceoffs_won / self.team_stats.faceoffs_taken) * 100), self.team_stats.saves)
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

    def __update_saves__(self, goalie):
        self.team_stats.saves += goalie.stats.saves

    def __update_goals_against__(self, goalie):
        self.team_stats.goals_against += goalie.stats.goals_against