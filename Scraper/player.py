from Scraper.playerStats import PlayerStats


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
                   self.stats.hits, self.stats.faceoffs_taken, self.stats.faceoffs_won))

    def update_stats(self, event, play_type, period, location):
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