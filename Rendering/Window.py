try:
    from pip._internal import main as _pip_install
except ImportError:
    from pip import main as _pip_install

try:
    import curses
except:
    _pip_install(["install", "windows-curses"])
    import curses


from .RayCast import RayCast
from .Camera import Camera
from .Map import Map




class Window:
    """a class that outputs to the terminal"""
    MAX_DEPTH = 20
    map : Map
    cam : Camera
    def __init__(self):
        self.closed = False

    def Run(self):
        curses.wrapper(self.main)

    def main(self, screen):
        # curses uses this V wrapper function to reset the terminal after use
        self.scr = curses.initscr() # initiate curses
        
        # use colours
        curses.start_color()
        for color_id in range(16, 232):             # initiate colours : colour cube = 16-232 and greyscale = 232-256
            curses.init_pair(color_id, 0, color_id) # creates a pairs of black text and the background colour

        self.height, self.width = screen.getmaxyx()
        screen.keypad(True)
        screen.nodelay(True)

        curses.noecho()
        curses.cbreak()

    def DrawScene(self):
        """Draws scene to the terminal"""
        # clear screen
        self.height, self.width = self.scr.getmaxyx()
        if curses.is_term_resized(self.height, self.width):
            curses.resizeterm(self.height + 1, self.width + 1)

        self.scr.clear()

        for x in range(self.width):
            raycast = RayCast(self.cam.posX, self.cam.posY,                     # send a ray, from player position
                self.cam._dirX + self.cam._planeX * (2 * x / self.width - 1), # rotate ray relative to the middle of the screen
                self.cam._dirY + self.cam._planeY * (2 * x / self.width - 1))
            
            for i in range(self.MAX_DEPTH):
                mapvalue = self.map[raycast.Step()]           # iterate raycast along line
                if (mapvalue > 0):                           # if collision with wall
                    depth, tex_u = raycast.IntersectData()   # get intersect data
                    
                    lineheight = int(self.height / max(1e-30, depth))               # line height relative to the screens height
                    start = int(self.height // 2 - lineheight * (self.cam.posZ))    # start = middle minus half lineheight (if camera in middle)

                    for y in range(max(start, 0), min(start + lineheight, self.height - 1)):     # clamps range
                        self.scr.addch(y, x, ord('a'), curses.color_pair(self.Textures[mapvalue - 1].get_Pixel(lineheight, tex_u, (y - start) / lineheight)))
                    break
