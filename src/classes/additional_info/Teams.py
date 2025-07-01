class Teams:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "Teams":
        return cls(
            num_teams=0
        )

    def __init__(self, num_teams: int) -> None:
        self.num_teams = num_teams

    def to_dict(self) -> dict:
        return {
            "num_teams": self.num_teams
        }