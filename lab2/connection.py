# connection.py

class Connection:
    def __init__(self):
        self.right_queue = []
        self.left_queue = []

    def __str__(self):
        return f"(->:{self.right_queue}\n<-:{self.right_queue})"

    @staticmethod
    def __get_message(queue):
        if len(queue) > 0:
            result = queue[0]
            queue.pop(0)
            return result
        else:
            return None

    def get_message(self, direction=0):
        if direction == 0:
            return self.__get_message(self.right_queue)
        else:
            return self.__get_message(self.left_queue)

    def send_message(self, message, direction=0):
        if direction == 0:
            self.left_queue.append(message)
            return
        else:
            self.right_queue.append(message)
            return
