class Teams:

    # alternative no-argument constructor
    @classmethod
    def create_default(cls):
        return cls(
            num_teams=0
        )

    def __init__(self, num_teams: int):
        self.num_teams = num_teams

    def to_dict(self):
        return {
            "num_teams": self.num_teams
        }