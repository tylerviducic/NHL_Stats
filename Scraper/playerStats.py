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