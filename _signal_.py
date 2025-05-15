class Signal:
    def __init__(self):
        self._subscribers : list = []
        
        self.disconnect()

    def connect(self, callback):
        self._subscribers.append(callback)

    def disconnect(self, *callback) -> list:
        r : list = []
        for c in callback:
            if c in self._subscribers:
                r.append(c)
                self._subscribers.remove(c)
        return r
        

    def disconnect_all(self) -> list: # Removes all connections to signal, returns a list off the old subscribers.
        r = self._subscribers.copy()
        self._subscribers.clear()
        return r

    def emit(self, *args, **kwargs):
        for callback in self._subscribers:
            callback(*args, **kwargs)