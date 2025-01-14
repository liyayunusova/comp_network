from __future__ import annotations
import pickle


class Message:
    def __init__(self):
        pass

    def encode(self) -> bytes:
        return pickle.dumps(self.__dict__)

    @staticmethod
    def decode(data: bytes) -> dict:
        return pickle.loads(data)


class Node2Node(Message):
    def __init__(self, src_node_id: int, dest_node_id: int, filename: str, size: int = -1):

        super().__init__()
        self.src_node_id = src_node_id
        self.dest_node_id = dest_node_id
        self.filename = filename
        self.size = size    # size = -1 means a node is asking for size


class Node2Tracker(Message):
    def __init__(self, node_id: int, mode: int, filename: str):

        super().__init__()
        self.node_id = node_id
        self.filename = filename
        self.mode = mode


class Tracker2Node(Message):
    def __init__(self, dest_node_id: int, search_result: list, filename: str):

        super().__init__()
        self.dest_node_id = dest_node_id
        self.search_result = search_result
        self.filename = filename


class ChunkSharing(Message):
    def __init__(self, src_node_id: int, dest_node_id: int, filename: str,
                 range: tuple, idx: int = -1, chunk: bytes = None):

        super().__init__()
        self.src_node_id = src_node_id
        self.dest_node_id = dest_node_id
        self.filename = filename
        self.range = range
        self.idx = idx
        self.chunk = chunk
