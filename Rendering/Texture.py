"""includes the texture and associated objects."""

try:
    from pip._internal import main as _pip_install
except ImportError:
    from pip import main as _pip_install
try:
    from PIL import Image
except:
    _pip_install(["install", "windows-curses"])
    from PIL import Image

class Colour:
    """Curses has an 8bit colour depth. this class converts between standard 24bit depth and the 8bit depth encoding
    Curses uses. it also includes some maths functions to average colours together."""
    __STORAGE_ACCURACY = 192    # standard 24bit colour depth
    def __init__(self, colour, accuracy = __STORAGE_ACCURACY):
        """
        colour - (r, g, b)\n
        accuracy - the maximum value a colour can be ie 2^bitdepth
        """
        r, g, b = colour                                        # unpack the tuple of rgb colours
        self.r = int(self.__STORAGE_ACCURACY / accuracy * r)    # redistribute the colour range over 0-Storage accuracy
        self.g = int(self.__STORAGE_ACCURACY / accuracy * g)
        self.b = int(self.__STORAGE_ACCURACY / accuracy * b)

    def FromID(ID): 
        """python doesnt allow multiple constructors so this'll do"""
        ID -= 16        # 0-216
        r = ID // 36     
        ID -= r * 36    # 0-36
        g = ID // 6
        ID -= g * 6     # 0-6
        b = ID
        return Colour((r, g, b), 6)

    def getID(self) -> int:
        """gets the Curses Colour encoding"""
        return 16 +                                         \
            int(self.r * 6 / self.__STORAGE_ACCURACY) * 36 +\
            int(self.g * 6 / self.__STORAGE_ACCURACY) * 6 + \
            int(self.b * 6 / self.__STORAGE_ACCURACY)
    
    def Avg(c1, c2, c3, c4):
        """averages 4 colours together."""
        col = Colour(((c1.r + c2.r + c3.r + c4.r) / 4, 
                      (c1.g + c2.g + c3.g + c4.g) / 4, 
                      (c1.b + c2.b + c3.b + c4.b) / 4))
        return col

class Texture:
    """A collection of images at different levels of detail for smooth texture compression"""
    def __init__(self, images):
        self.images = images

   
    def get_Pixel(self, lineheight : int, x : float, y : float):
        for image in self.images:
            if lineheight >= len(image):
                return image[int(y * len(image))][int(x * len(image[0]))]
        
        return image[int(y * len(image))][int(x * len(image[0]))]

    def Load(filepath, mipmap = 0):
        """loads image from local file in the same folder as the script"""

        img = Image.open(filepath).convert('RGB')
        images = [
            [[Colour(img.getpixel((x, y)), 256).getID() 
            for x in range(img.width)] 
            for y in range(img.width)], 
        ]
        for i in range(mipmap):
            images.append([[Colour.Avg(
                    Colour.FromID(images[i - 1][y * 2]    [x * 2]),         # compress the last mipmap by half
                    Colour.FromID(images[i - 1][y * 2]    [x * 2 + 1]),     # generate a new colour for from the 4 corresponding pixels
                    Colour.FromID(images[i - 1][y * 2 + 1][x * 2]),         # half the size and repeat
                    Colour.FromID(images[i - 1][y * 2 + 1][x * 2 + 1])
                    ).getID() 
                for x in range(img.width  // 2 ** (i + 1))] 
                for y in range(img.height // 2 ** (i + 1))])

        return Texture(images)
