class AffectedPlayers:
    @classmethod
    def create_default(cls) -> 'AffectedPlayers':
        return cls(
            red= True,
            blue= True,
            tan= True,
            green= True,
            orange= True,
            purple= True,
            teal= True,
            pink= True
        )

    def __init__(self, red: bool,
				blue: bool,
				tan: bool,
				green: bool,
				orange: bool,
				purple: bool,
				teal: bool,
				pink: bool) -> None:
        self.red = red
        self.blue = blue
        self.tan = tan
        self.green = green
        self.orange = orange
        self.purple = purple
        self.teal = teal
        self.pink = pink

    def to_dict(self) -> dict:
        return {
            'red': self.red,
            'blue': self.blue,
            'tan': self.tan,
            'green': self.green,
            'orange': self.orange,
            'purple': self.purple,
            'teal': self.teal,
            'pink': self.pink
        }
