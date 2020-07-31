from typing import Iterable, List, Reversible, Tuple
import numpy as np

import pygame
from config import Config as CONFIG


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

    def add_message(self, text: str, fg: pygame.Color = None, *, stack: bool = True) -> None:
        """Add a message to the log.
            `text` is the message text, `fg` is the text color.
            If `stack` is True then the message can stack with a previous message
            of the same text. """

        # If to colour passed, default to white
        if not fg:
            fg = pygame.Color("white")
        # if it's stacking and the last message is the same as this, just increase the count
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))
