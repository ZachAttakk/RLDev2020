
'''event handler code'''
from typing import Optional
import pygame.event
from actions import Action, ActionEscape, ActionMove, ActionEscape, ActionQuit, ActionBump


def handle_event(event) -> Optional[Action]:
    '''Handles events and passes back actions'''

    response = None
    # quit keys
    if event.type == pygame.QUIT:
        # Exit the game
        # response['exit'] = True
        response = ActionQuit()

    # Movement keys and escape to quit
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            response = ActionBump(0, -1)
        elif event.key == pygame.K_DOWN:
            response = ActionBump(0, 1)
        elif event.key == pygame.K_LEFT:
            response = ActionBump(-1, 0)
        elif event.key == pygame.K_RIGHT:
            response = ActionBump(1, 0)
        elif event.key == pygame.K_ESCAPE:
            response = ActionEscape()

    # Send back the response
    if response is not None:
        return response
