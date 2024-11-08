class FontInfo:
    def __init__(self, 
                 font: str = "Arial", 
                 size: int = 16, 
                 color: tuple[int, int, int] = (0, 0, 0), 
                 bold: bool = False, 
                 italic: bool = False) -> None:
        self.font: str = font
        self.size: int = size
        self.color: tuple[int, int, int] = color
        self.bold: bool = bold
        self.italic: bool = italic