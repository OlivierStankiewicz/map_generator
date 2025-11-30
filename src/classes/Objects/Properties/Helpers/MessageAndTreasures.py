from classes.Objects.Properties.Helpers.Resources import Resources

class MessageAndTreasures:
    @classmethod
    def create_default(cls) -> 'MessageAndTreasures':
        return cls(
            message= "",
            resources = Resources.create_default(),
            artifact= 65535
        )

    def __init__(self, message: str, resources: Resources, artifact: int) -> None:
        self.message = message
        self.resources = resources
        self.artifact = artifact

    def to_dict(self) -> dict:
        return {
            'message': self.message,
            'resources': self.resources.to_dict(),
            'artifact': self.artifact,
        }