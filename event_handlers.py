'''event handler code'''
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import exceptions
import pygame.event
from actions import Action, ActionEscape, ActionEscape, ActionQuit, ActionBump, ActionWait, ActionFullscreen, ActionMouseMove, ActionPickup

from keyboard_layout import MOVE_KEYS, WAIT_KEYS
from config import Config as CONFIG
from entity import Item

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
                try:
                    something_happened = action.perform()
                except exceptions.Impossible as exc:
                    self.engine.message_log.add_message(
                        exc.args[0], CONFIG.get_colour("error"))
                    return False

            if something_happened:
                # let the baddies go
                self.engine.handle_enemy_turns()
                # update FOV
                self.engine.update_fov()

        return something_happened

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
            elif event.key == pygame.K_g:
                response = ActionPickup(player)

        if event.type == pygame.MOUSEMOTION:
            response = ActionMouseMove(self.engine, pygame.mouse.get_pos())

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


class AskUserEventHandler(EventHandler):
    """Handle user input for actions that require special input"""

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

        response = None
        # quit keys
        if event.type == pygame.QUIT:
            # Exit the game
            # response['exit'] = True
            response = ActionQuit()
        # ignore modifier keys
        if event.type not in [pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LCTRL,  pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT]:
            response = ActionEscape()

        # Send back the response
        if response is not None:
            return response


class InventoryEventHandler(AskUserEventHandler):
    """Handle selections from the inventory"""
