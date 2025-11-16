from classes.Objects.Properties.Helpers.DetailsQuest import Details

class Quest:
    @classmethod
    def create_default(cls) -> "Quest":
        return cls(
            type= 0,
            details= Details.create_default(),
            deadline= 0,
            proposal= '',
            progress= '',
            completion= ''
        )

    def __init__(self, type: int,
				details: Details,
				deadline: int,
				proposal: str,
				progress: str,
				completion: str) -> None:
        self.type = type
        self.details = details
        self.deadline = deadline
        self.proposal = proposal
        self.progress = progress
        self.completion = completion

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "details": self.details.to_dict(),
            "deadline": self.deadline,
            "proposal": self.proposal,
            "progress": self.progress,
            "completion": self.completion
        }