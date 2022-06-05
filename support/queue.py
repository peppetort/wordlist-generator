import threading
from collections import deque


class Queue:
    def __init__(self):
        self.lock = threading.Lock()
        self.queue = deque()

    def enqueue(self, element_list: []):
        self.lock.acquire()
        self.queue.extend(element_list)
        self.lock.release()

    def dequeue(self) -> str:
        self.lock.acquire()
        element = self.queue.popleft()
        self.lock.release()
        return element
