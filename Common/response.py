from dataclasses import dataclass

@dataclass
class Response :
    data : str
    message : str
    success : bool

