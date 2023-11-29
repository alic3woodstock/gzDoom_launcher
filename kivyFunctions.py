from kivy.graphics import Color, Rectangle
highlight_color = [2, 0, 0]

def rectBtnActive(widget):
    print(widget.state)
    if widget.state == 'normal':
        widget.background_color = 'black'
    else:
        widget.background_color = highlight_color