import ortc
import json

class RealtimeMessageBus:
    def __init__(self):
        self._ortc_client = ortc.OrtcClient()
        self._ortc_client.set_on_connected_callback(self._on_connected)
        self._ortc_client.set_on_subscribed_callback(self._on_subscribed) 
        self._ortc_client.cluster_url = "http://ortc-developers.realtime.co/server/2.1"
        self._ortc_client.connect("Rb7lul")
        self._listeners = { }
    
    def _on_connected(self, sender):
        print('Connected')
        self._ortc_client.subscribe('ACI_KYD', True, self._on_message)
        
    def _on_message(self, sender, channel, message):
        print('Message received ('+channel+'): ' + message)
        try:
            data = json.loads(message) 
            msg = data["FunctionName"]       
            if msg is None:
                return
            
            if msg in self._listeners:
                handler = self._listeners[msg]
                handler(data)
        except ValueError:
            pass
        except Exception as e:
            print('An exception occured while deserializing message: ' + e)
 
    def _on_subscribed(self, sender, channel):
        print('Subscribed to channel: ' + channel)
        
    def add_listener(self, message, listener):
        if message not in self._listeners:
            #print('adding listener for message: ' + message)
            self._listeners[message] = listener
            
class CatchThiefMessageListener:
    def __init__(self, state_machine, message_bus):
        self._sm = state_machine;
        message_bus.add_listener("CatchThief", self._handle_message)
    
    def _handle_message(self, data):
        self._sm.change_to("catch-thief")
        return

class SetProgressMessageListener:
    def __init__(self, message_bus, game):
        self._game = game
        message_bus.add_listener("SetProgress", self._handle_message)
        
    def _handle_message(self, data):
        self._game.progress = int(data["Value"])

if __name__ == "__main__":
    mb = RealtimeMessageBus()
    while True:
        pass