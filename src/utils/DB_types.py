import dataclasses


@dataclasses.dataclass
class Column:
    name: str
    type: str
