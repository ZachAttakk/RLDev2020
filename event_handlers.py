
'''event handler code'''
import pygame


def handle_events(events):
    '''Handles events and passes back messages'''

    # create list for responses
    response = {}

    # loop through them and build the dict
    for event in events:

        # quit keys
        if event.type == pygame.QUIT:
            # Exit the game
            response['exit'] = True

        # Movement keys and escape to quit
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                response['move'] = (0, -1)
            elif event.key == pygame.K_DOWN:
                response['move'] = (0, 1)
            elif event.key == pygame.K_LEFT:
                response['move'] = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                response['move'] = (1, 0)
            elif event.key == pygame.K_ESCAPE:
                response['exit'] = True
    # return results
    return response
