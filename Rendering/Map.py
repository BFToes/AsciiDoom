class Map:
    """a wrapper for a 2d array which contains the current world data"""
    Sprites = []
    def __init__(self, level):
        """
        
        """
        self.image = level
        self.height = len(self.image)
        self.width = len(self.image[0])

    def __getitem__(self, pos):
        x, y = pos
        return self.image[y][x]

    def IsWall(self, pos):
        x, y = pos
        return self.image[y][x] > 0

    def IsSprite(self, pos): # not done yet
        x, y = pos
        return self.image[y][x] < 0
