from kivy.graphics import Color, Rectangle

highlight_color = [2, 0, 0]
normal_highlight_color = [0.5, 0, 0, 1]
border_color = [1, 1, 1, 1]
hover_color = [0.3, 0, 0, 1]
normal_color = [0, 0, 0, 1]
button_height = 42
button_width = 128

class GetBorders:
    def __init__(self, widget):
        self.top_left = (widget.x, widget.y)
        self.top_right = (widget.x + widget.width, widget.y)
        self.bottom_right = (widget.x + widget.width, widget.y + widget.height)
        self.bottom_left = (widget.x, widget.y + widget.height)

def change_color(widget):
    if widget.state == 'normal':
        widget.background_color = normal_color
    else:
        widget.background_color = highlight_color
        # widget.color = 'white'
    widget.color = 'white'


