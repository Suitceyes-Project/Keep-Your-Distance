from abc import ABC, abstractmethod

class State (ABC):
    @abstractmethod
    def enter(self):
        pass
    
    @abstractmethod
    def update(self, deltaTime):
        pass
    
    @abstractmethod
    def exit(self):
        pass


class StateMachine:
    def __init__(self):
        self._states = {}
        self._current = None

    def add_state(self, stateName, state):
        self._states[stateName] = state

    def change_to(self, stateName):
        if self._current != None:
            self._current.exit()
        
        self._current = self._states[stateName]
        self._current.enter()

    def update(self, deltaTime):
        if self._current != None:
            self._current.update(deltaTime)