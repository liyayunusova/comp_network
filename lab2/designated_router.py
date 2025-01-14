# designated_router.py
from message import Message
from msg_type import MsgType
import topology as topology_class
from connection import Connection

class DesignatedRouter:
    def __init__(self):
        self.connections = []
        self.topology = topology_class.Topology()

    def add_connection(self):
        new_connection = Connection()
        new_index = len(self.connections)
        self.connections.append(new_connection)
        return new_connection, new_index

    def add_node(self, index, neighbors):
        self.topology.add_new_node(index)
        for j in neighbors:
            self.topology.add_new_link(index, j)

    def delete_node(self, index):
        self.topology.delete_node(index)

    def send_all_exclude_one(self, exclude_index,  msg):
        for conn_ind in range(len(self.connections)):
            conn = self.connections[conn_ind]
            if conn is None:
                continue
            if conn_ind == exclude_index:
                continue
            conn.send_message(msg, 1)

    def proc_msg_neighbors(self, conn_ind, input_msg):
        self.add_node(conn_ind, input_msg.data)

        msg = Message()
        msg.type = MsgType.NEIGHBORS
        msg.data = {"index": conn_ind,
                    "neighbors": input_msg.data
                    }

        self.send_all_exclude_one(conn_ind, msg)

    def proc_msg_off(self, conn_ind, input_msg):
        self.delete_node(conn_ind)

        msg = Message()
        msg.type = MsgType.OFF
        msg.data = conn_ind

        self.send_all_exclude_one(conn_ind, msg)

    def print_shortest_ways(self):
        msg = Message()
        msg.type = MsgType.PRINT_WAYS
        for conn in self.connections:
            conn.send_message(msg, 1)

    def proc_message(self):
        for conn_ind in range(len(self.connections)):
            conn = self.connections[conn_ind]
            if conn is None:
                continue

            input_msg = conn.get_message(1)

            if input_msg is None:
                continue

            print(f"dr({conn_ind}): {input_msg}\n", end="")

            if input_msg.type == MsgType.NEIGHBORS:
                self.proc_msg_neighbors(conn_ind, input_msg)

            elif input_msg.type == MsgType.GET_TOPOLOGY:
                msg = Message()
                msg.type = MsgType.SET_TOPOLOGY
                msg.data = self.topology.copy()
                conn.send_message(msg, 1)

            elif input_msg.type == MsgType.OFF:
                self.proc_msg_off(conn_ind, input_msg)

            else:
                print("DR: unexpected msf type:", input_msg.type)
