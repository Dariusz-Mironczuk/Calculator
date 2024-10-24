from customtkinter import CTkButton
from settings import *


class Button(CTkButton):
    def __init__(self, parent, text, function, row, column, font, color = 'dark-gray', span = 1):
        super().__init__(
            master = parent,
            text = text,
            command = function,
            corner_radius = STYLING['corner-radius'],
            font = font,
            fg_color = COLORS[color]['fg'],
            hover_color = COLORS[color]['hover'],
            text_color = COLORS[color]['text']
        )

        self.grid(column = column,
                  columnspan = span,
                  row = row,
                  sticky = 'nsew',
                  padx = STYLING['gap'],
                  pady = STYLING['gap'])
        
class NumButton(Button):
    def __init__(self, parent, text, function, row, column, font, span, color = 'light-gray'):
        super().__init__(
            parent = parent,
            text = text,
            function = lambda: function(text),
            row = row,
            column = column,
            font = font,
            span = span,
            color = color)
        
class MathButton(Button):
    def __init__(self, parent, text, operator, function, row, column, font, color = 'purple'):
        super().__init__(
            parent = parent,
            text = text,
            function = lambda: function(operator),
            row = row,
            column = column,
            font = font,
            color = color)