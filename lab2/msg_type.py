# msg_type.py
import enum

class MsgType(enum.Enum):
    NEIGHBORS = enum.auto()
    GET_TOPOLOGY = enum.auto()
    SET_TOPOLOGY = enum.auto()
    OFF = enum.auto()
    PRINT_WAYS = enum.auto()
