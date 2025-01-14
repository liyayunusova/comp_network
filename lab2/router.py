# router.py
import time
from message import Message
from msg_type import MsgType
import topology as topology_class

class Router:
    def __init__(self, conn, index):
        self.DR_connection = conn
        self.topology = topology_class.Topology()
        self.shortest_roads = None
        self.index = index
        self.neighbors = []

    def print_shortest_ways(self):
        shortest_ways = self.topology.get_shortest_ways(self.index)
        print(f"{self.index}: {shortest_ways}\n", end="")

    def send_neighbors(self):
        msg = Message()
        msg.type = MsgType.NEIGHBORS
        msg.data = self.neighbors.copy()
        self.DR_connection.send_message(msg)

    def get_topology(self):
        msg = Message()
        msg.type = MsgType.GET_TOPOLOGY
        self.DR_connection.send_message(msg)

    def router_start(self):
        self.send_neighbors()
        self.get_topology()

    def router_off(self):
        msg = Message()
        msg.type = MsgType.OFF
        self.DR_connection.send_message(msg)

    def add_node(self, index, neighbors):
        self.topology.add_new_node(index)
        for j in neighbors:
            self.topology.add_new_link(index, j)

        if index in self.neighbors:
            if index not in self.topology.topology[self.index]:
                msg = Message()
                msg.type = MsgType.NEIGHBORS
                msg.data = [index]
                self.DR_connection.send_message(msg)

    def delete_node(self, index):
        self.topology.delete_node(index)

    def proc_message(self):
        input_msg = self.DR_connection.get_message()

        if input_msg is None:
            return

        print(f"r({self.index}) : {input_msg}\n", end="")

        if input_msg.type == MsgType.NEIGHBORS:
            index = input_msg.data["index"]
            neighbors = input_msg.data["neighbors"]
            self.add_node(index, neighbors)
        elif input_msg.type == MsgType.SET_TOPOLOGY:
            new_topology = input_msg.data
            self.topology = new_topology
        elif input_msg.type == MsgType.OFF:
            index = input_msg.data
            self.delete_node(index)
        elif input_msg.type == MsgType.PRINT_WAYS:
            self.print_shortest_ways()
        else:
            print("DR: unexpected msf type:", input_msg.type)
