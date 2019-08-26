import requests


class SeasonRoster:

    def __init__(self, roster, date):
        self.roster = roster
        self.date = date
        self.season = self.__get_season__(date)
        self.players = self.__get_players__()

    def was_player_on_team(self, player_name):
        if player_name in self.players:
            return True
        return False

    # Private Methods

    @staticmethod
    def __get_season__(date):
        if date.month >= 10:
            start_year = date.year
            end_year = date.year + 1
        else:
            start_year = date.year - 1
            end_year = date.year
        return '{}{}'.format(start_year, end_year)

    def __get_players__(self):
        team_dict = requests.get('https://statsapi.web.nhl.com/api/v1/teams/{}/?expand=team.roster&season={}'.format(
            self.roster.id, self.season)).json()
        players = []
        for person in team_dict['teams'][0]['roster']['roster']:
            players.append(person['person']['fullName'])
        return players

