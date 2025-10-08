from classes.Objects.Properties.Helpers.IsBuilt import IsBuilt
from classes.Objects.Properties.Helpers.IsDisabled import IsDisabled


class Buildings:
    @classmethod
    def create_default(cls) -> 'Buildings':
        return cls(
            is_built=IsBuilt.create_default(),
            is_disabled=IsDisabled.class_default()
        )

    def __init__(self, is_built: IsBuilt, is_disabled: IsDisabled) -> None:
        self.is_built = is_built
        self.is_disabled = is_disabled

    def to_dict(self) -> dict:
        return {
            'is_built': self.is_built,
            'is_disabled': self.is_disabled,
        }