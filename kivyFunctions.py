from kivy.graphics import Color, Rectangle
highlight_color = [2, 0, 0]
hover_color = [0.5, 0.5, 0.5]
normal_color = [0, 0, 0, 0]

def change_color(widget):
    if widget.state == 'normal':
        widget.background_color = normal_color
    else:
        widget.background_color = highlight_color
    widget.color = 'white'