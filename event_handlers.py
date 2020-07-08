'''event handler code'''
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from typing import Optional
import pygame.event
from actions import Action, ActionEscape, ActionMove, ActionEscape, ActionQuit, ActionBump

if TYPE_CHECKING:
    from engine import Engine


class EventHandler:
    def __init__(self, engine: Engine):
        self.engine = engine

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
            if event.key == pygame.K_UP:
                response = ActionBump(player, 0, -1)
            elif event.key == pygame.K_DOWN:
                response = ActionBump(player, 0, 1)
            elif event.key == pygame.K_LEFT:
                response = ActionBump(player, -1, 0)
            elif event.key == pygame.K_RIGHT:
                response = ActionBump(player, 1, 0)
            elif event.key == pygame.K_ESCAPE:
                response = ActionEscape(player)

        # Send back the response
        if response is not None:
            return response
