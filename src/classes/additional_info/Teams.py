class Teams:
    @classmethod
    def from_default(self):
       self.num_teams = 0

    def __init__(self, num_teams: int):
        self.num_teams = num_teams

    def to_dict(self):
        return {
            "num_teams": self.num_teams
        }