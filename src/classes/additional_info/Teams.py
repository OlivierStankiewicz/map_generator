class Teams:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "Teams":
        return cls(
            num_teams=0,
            team_for_player=[] # int array
        )

    def __init__(self, num_teams: int, team_for_player: list[int]) -> None:
        self.num_teams = num_teams
        self.team_for_player = team_for_player

    def to_dict(self) -> dict:
        return {
            "num_teams": self.num_teams,
            "team_for_player": self.team_for_player
        }