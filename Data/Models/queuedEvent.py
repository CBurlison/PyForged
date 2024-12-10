from typing import Callable

class QueuedEvent:
    def __init__(self, caller, event: Callable[[], None]):
        self.caller = caller
        self.event: Callable[[], None] = event
