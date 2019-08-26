class GoalieStats:

    def __init__(self):
        self.saves = 0
        self.goals_against = 0

    def update_saves(self):
        self.saves += 1

    def update_goals_against(self):
        self.goals_against += 1