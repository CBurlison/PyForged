class QueuedEvent:
    def __init__(self, caller, event):
        self.caller = caller
        self.event = event
