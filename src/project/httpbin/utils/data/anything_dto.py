from attr import dataclass

@dataclass
class AnythingDto:
    key_string: str = None
    key_boolean: bool = None
    key_number: int = None
    key_array_string: list[str] = None
    key_array_obj: list[dict[str:str] | str | int | bool] = None
