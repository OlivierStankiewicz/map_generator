from classes.Objects.PropertiesBase import Properties

class Sign(Properties):
    @classmethod
    def create_default(cls) -> 'Sign':
        return cls(
            message= ''
        )

    def __init__(self, message: str) -> None:
        self.message = message
        self.unknown = [0, 0, 0, 0]

    def to_dict(self) -> dict:
        return {
            'message': self.message,
            'unknown': self.unknown
        }