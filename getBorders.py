class GetBorders:
    def __init__(self, widget):
        self.top_left = (widget.x, widget.y)
        self.top_right = (widget.x + widget.width, widget.y)
        self.bottom_right = (widget.x + widget.width, widget.y + widget.height)
        self.bottom_left = (widget.x, widget.y + widget.height)