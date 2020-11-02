import json
            
class CatchThiefMessageListener:
    def __init__(self, state_machine, message_bus):
        self._sm = state_machine
        message_bus.add_listener("suitceyes/kyd/CatchThief", self._handle_message)
    
    def _handle_message(self, data):
        self._sm.change_to("catch-thief")
        return

class SetProgressMessageListener:
    def __init__(self, message_bus, game):
        self._game = game
        message_bus.add_listener("suitceyes/kyd/SetProgress", self._handle_message)
        
    def _handle_message(self, data):
        payload = json.loads(data.payload)
        self._game.progress = int(payload["Value"])

if __name__ == "__main__":
    from MqttMessageService import MqttMessageService
    class Game:
        def __init__(self):
            self.progress = 0
    
    class StateMachine:
        def change_to(self, state):
            pass
    
    game = Game()
    sm = StateMachine()
    with MqttMessageService() as message_bus:
       CatchThiefMessageListener(sm, message_bus)
       SetProgressMessageListener(message_bus, game)

       while True:
           pass 