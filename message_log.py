from typing import List, Reversible, Tuple
import textwrap
import numpy as np

import tcod
import pygame
from config import Config as CONFIG
import render_functions


class Message:
    def __init__(self, text: str, fg: str):
        self.plain_text = text
        self.fg_col = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        """Full text of this messafe, including the count if necessary"""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        else:
            return self.plain_text


class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(self, text: str, fg: str = "white", *, stack: bool = True) -> None:
        """Add a message to the log.
            `text` is the message text, `fg` is the text color.
            If `stack` is True then the message can stack with a previous message
            of the same text. """
        # if it's stacking and the last message is the same as this, just increase the count
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    @staticmethod
    def render_messages(size: Tuple[int, int],
                        messages: Reversible[Message],
                        font: pygame.font) -> None:
        """Render the messages provided and return them on a surface
        """

        con = pygame.Surface(size).convert_alpha()
        # start the first one 2 pixels off the bottom
        y_offset = size[1] - 10

        for message in reversed(messages):
            for line in reversed(textwrap.wrap(message.full_text, int(size[0]))):
                print_pos = (0, y_offset)
                render_functions.render_text(
                    con, line, print_pos, message.fg_col, font)
                y_offset -= 8

            if y_offset < 0:
                break  # log is full

        return con
