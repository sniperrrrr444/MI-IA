from dataclasses import dataclass
from queue import Queue

@dataclass
class GenerationJob:
    messages: list[dict]
    max_new_tokens: int
    temperature: float

class InferenceScheduler:
    def __init__(self):
        self.queue = Queue()

    def submit(self, job):
        self.queue.put(job)

    def pending(self):
        return self.queue.qsize()
