from typing import List, Reversible, Tuple
import numpy as np

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

    @staticmethod
    def render_messages(size: Tuple[int, int],
                        messages: Reversible[Message],
                        font: pygame.font) -> None:
        """Render the messages provided and return them on a surface
        """

        con = pygame.Surface(size).convert_alpha()
        # start the first one 2 pixels off the bottom
        y_offset = size[1] - font.get_linesize()

        for message in reversed(messages):
            for line in reversed(MessageLog.wrap_text(message.full_text, font, int(size[0]))):
                print_pos = (0, y_offset)
                render_functions.render_text(
                    con, line, print_pos, message.fg_col, font)
                y_offset -= font.get_linesize()

            if y_offset < 0:
                break  # log is full

        return con

    @staticmethod
    def wrap_text(text, font, width):
        """Returns list of strings that all fit within pixel width using given font"""
        results = []

        seperator = " "

        _split_words = text.split()

        # Quick check if the whole string fits
        # (also removes extra whitespace)
        _check = seperator.join(_split_words)
        if font.size(_check)[0] <= width:
            return [text, ]

        # do this until we're out of words
        while len(_split_words) > 0:
            # temporary variable with the last result that fit
            _last_fit = ""
            for i in range(1, len(_split_words)+1):
                # make line with one more word than last time
                _check = seperator.join(_split_words[:i])
                # check if it's too long, in which case we store the last one that fit
                if (font.size(_check)[0] > width):
                    # add last fit
                    results.append(_last_fit)
                    # remove those from the list
                    _split_words = _split_words[i-1:]
                    # kill the loop so we can start over
                    break
                elif i == len(_split_words):
                    # this was the last iteration
                    # if it reaches here, we know the remaining part is short enough
                    results.append(_check)
                    # still remove the part we stored
                    _split_words = _split_words[i:]
                else:
                    # it fits, so prep to try one longer
                    _last_fit = _check
        # done while, return results
        return results
