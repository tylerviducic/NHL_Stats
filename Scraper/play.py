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
                elif team.is_goalie_on_team(player['Name']):
                    team.get_goalie_by_name(player['Name']).update_stats(self.event, player['Type'])

    def __add_plays__(self, play_dict):
        for player in play_dict['players']:
            player_name = player['player']['fullName']
            player_type = player['playerType']
            self.players.append({'Name': player_name, 'Type': player_type})
            self.event = play_dict['result']['event']
            self.play_coordinates.update(play_dict['coordinates'])
            self.period = play_dict['about']['period']