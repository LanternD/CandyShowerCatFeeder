import time

class basic_device_handler(object):
    """Use this handler to keep multiple Amazon Echo devices from reacting to
       the same voice command.
    """
    DEBOUNCE_SECONDS = 0.3 # time window to prevent multiple Echo reacting
    time_stamp = 0 # time stamp that record the TURN ON time

    def __init__(self):
        self.lastEcho = time.time()

    def on(self, client_address, name):
        if self.debounce():
            return True
        return self.act(client_address, True, name)

    def off(self, client_address, name):
        if self.debounce():
            return True
        return self.act(client_address, False, name)

    def act(self, client_address, state):
        pass

    def debounce(self):
        # make sure the device response to the first Amazon Echo that hears the voice.
        
        if (time.time() - self.lastEcho) < self.DEBOUNCE_SECONDS:
            return True

        self.lastEcho = time.time()
        return False


