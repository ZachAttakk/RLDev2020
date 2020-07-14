'''event handler code'''
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from typing import Optional
import pygame.event
from actions import Action, ActionEscape, ActionMove, ActionEscape, ActionQuit, ActionBump, ActionWait, ActionFullscreen

from keyboard_layout import MOVE_KEYS, WAIT_KEYS

if TYPE_CHECKING:
    from engine import Engine


class EventHandler:
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self):
        raise NotImplementedError()


class MainGameEventHandler(EventHandler):
    def __init__(self, engine):
        super().__init__(engine)

    def handle_events(self):
        something_happened = False
        events = pygame.event.get(pump=True)
        if len(events) > 0:
            for event in events:
                action = self.process_event(event)
                if action is None:
                    continue
                # do the thing.
                # actions will handle their own validation
                action.perform()
                something_happened = True

            if something_happened:
                # let the baddies go
                self.engine.handle_enemy_turns()
                # update FOV
                self.engine.update_fov()

    def process_event(self, event) -> Optional[Action]:
        '''Handles events and passes back actions'''

        player = self.engine.PLAYER
        response = None
        # quit keys
        if event.type == pygame.QUIT:
            # Exit the game
            # response['exit'] = True
            response = ActionQuit()
        # Movement keys and escape to quit
        if event.type == pygame.KEYDOWN:
            if event.key in MOVE_KEYS:
                dir = MOVE_KEYS[event.key]
                response = ActionBump(player, *dir)
            elif event.key in WAIT_KEYS:
                response = ActionWait(player)
            elif event.key == pygame.K_ESCAPE:
                response = ActionEscape()
            elif event.key == pygame.K_F11:
                response = ActionFullscreen()

        # Send back the response
        if response is not None:
            return response


class GameOverEventHandler(EventHandler):

    def handle_events(self):
        events = pygame.event.get(pump=True)
        if len(events) > 0:
            for event in events:
                action = self.process_event(event)
                if action is None:
                    continue
                # do the thing.
                # actions will handle their own validation
                action.perform()

    def process_event(self, event) -> Optional[Action]:
        '''Handles events and passes back actions'''

        player = self.engine.PLAYER
        response = None
        # quit keys
        if event.type == pygame.QUIT:
            # Exit the game
            # response['exit'] = True
            response = ActionQuit()
        # Escape to quit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                response = ActionEscape()
            elif event.key == pygame.K_F11:
                response = ActionFullscreen()

        # Send back the response
        if response is not None:
            return response
