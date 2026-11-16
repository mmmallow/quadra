class EventManager:
    def __init__(self):
        self.listeners = {}

    def Subscribe(self, event, listener):
        if (event in self.listeners):
            self.listeners[event].append(listener)
        else:
            self.listeners[event] = [listener]

    def Unsubscribe(self, event, listener):
        if (event in self.listeners):
            self.listeners[event].remove(listener)
        else:
            return

        if (len(self.listeners[event]) == 0):
            del self.listeners[event]

    def Notify(self, event, data):
        if (event in self.listeners):
            for listener in self.listeners[event]:
                listener.Listen(event, data)
