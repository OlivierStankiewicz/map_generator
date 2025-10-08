from classes.Objects.PropertiesBase import Properties

class Sign(Properties):
    @classmethod
    def create_default(cls) -> 'Sign':
        return cls(
            message= '',
            unknown= []
        )

    def __init__(self, message: str, unknown: list[int]) -> None:
        self.message = message
        self.unknown = unknown

    def to_dict(self) -> dict:
        return {
            'message': self.message,
            'unknown': self.unknown
        }