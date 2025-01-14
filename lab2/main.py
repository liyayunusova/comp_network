# main.py
import numpy as np
import time
from threading import Thread
from designated_router import DesignatedRouter
from router import Router
from connection import Connection

designed_router: DesignatedRouter = None
stop_flag = False
printer_flag = False
blink_conn_arr = []

def router_run(neighbors):
    global designed_router
    global blink_conn_arr

    conn, index = designed_router.add_connection()
    router = Router(conn, index)
    router.neighbors = neighbors.copy()
    router.router_start()

    while True:
        router.proc_message()
        if blink_conn_arr[router.index]:
            router.router_off()
            time.sleep(2)
            router.router_start()
            blink_conn_arr[router.index] = False

        if stop_flag:
            break

def designed_router_run():
    global designed_router
    global printer_flag
    designed_router = DesignatedRouter()

    while True:
        designed_router.proc_message()
        if printer_flag:
            designed_router.print_shortest_ways()
            printer_flag = False
        if stop_flag:
            break

def stopper():
    global stop_flag
    time.sleep(10)
    stop_flag = True

def printer():
    global printer_flag
    while True:
        time.sleep(1)
        printer_flag = True
        if stop_flag:
            break

def connections_breaker():
    global blink_conn_arr
    time.sleep(2)
    threshold = 0.5
    while True:
        time.sleep(0.01)
        val = np.random.rand()
        if val >= threshold:
            index = np.random.randint(0, len(blink_conn_arr))
            blink_conn_arr[index] = True
            time.sleep(2)

        if stop_flag:
            break

def simulate(nodes, neighbors):
    global blink_conn_arr

    dr_thread = Thread(target=designed_router_run, args=())

    node_threads = [Thread(target=router_run, args=(neighbors[i],)) for i in range(len(nodes))]
    blink_conn_arr = [False for i in range(len(nodes))]

    dr_thread.start()
    for i in range(len(nodes)):
        node_threads[i].start()

    printer_thread = Thread(target=printer, args=())
    conn_breaker_thread = Thread(target=connections_breaker, args=())
    conn_breaker_thread.start()
    printer_thread.start()

    time.sleep(5)
    global stop_flag
    stop_flag = True
    for i in range(len(nodes)):
        node_threads[i].join()

    dr_thread.join()

def main():
    linear = {
        "name": "linear",
        "nodes": [0, 1, 2],
        "neighbors": [[1], [0, 2], [1]]
    }
    star = {
        "name": "star",
        "nodes": [0, 1, 2, 3],
        "neighbors": [[1], [0, 2, 3], [1], [1]]
    }
    circle = {
        "name": "circle",
        "nodes": [0, 1, 2],
        "neighbors": [[2, 1], [0, 2], [1, 0]]
    }

    cur_topology = circle
    print(f"\ntopology: {cur_topology['name']}\n")
    simulate(cur_topology["nodes"], cur_topology["neighbors"])

if __name__ == '__main__':
    main()
