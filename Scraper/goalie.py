from Scraper.goalieStats import GoalieStats


class Goalie:

    def __init__(self, name):
        self.name = name
        self.stats = GoalieStats()

    def update_stats(self, event, play_type):
        if event == 'Shot':
            self.__update_shot__(play_type)
        elif event == 'Goal':
            self.__update_goal__(play_type)

    def show_stats(self):
        print(self.name + ':')
        print('''\t\tSaves: {0:>10}
        Goals Against: {1:>1}
        Save %: {2:>13}
        '''.format(self.stats.saves, self.stats.goals_against,
                   self.stats.saves/(self.stats.saves + self.stats.goals_against)))

    # Private Methods

    def __update_shot__(self, play_type):
        if play_type == 'Goalie':
            self.stats.update_saves()

    def __update_goal__(self, play_type):
        if play_type == 'Goalie':
            self.stats.update_goals_against()