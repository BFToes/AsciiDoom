"""Example"""
import os
dir_path = __file__.removesuffix(os.path.basename(__file__))

from Rendering import Window, Map, Camera, Texture


Levels = { "example" : [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],   # a number greater than 1 is a wall
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],   # a number less than 1 is a sprite
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],   
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],   # the number value corresponds to the textures in window. 
    [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 1],   # 1 will draw a wall with the texture of textures[0] 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],   # 2 will draw a wall with the texture of textures[1]...
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],   
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],   # (WIP - ie not working)
    [1, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 1],   # -1 will draw a sprite with the texture of textures[0]
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],   # -2 will draw a sprite with the texture of textures[1]...
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
}

class Game(Window):
    def __init__(self):         # game ctor
        Window.__init__(self)   # window ctor -> important
        self.Textures = [
            Texture.Load(dir_path + 'Textures/tex_metal_1.png', 3),
            Texture.Load(dir_path + 'Textures/tex_metal_2.png', 3),
            Texture.Load(dir_path + 'Textures/tex_stone_1.png', 3),
            Texture.Load(dir_path + 'Textures/tex_stone_2.png', 3),
            ]
        self.cam = Camera(2, 2, 0.5) 
        self.map = Map(Levels["example"])
    
    def main(self, screen = None):
        Window.main(self, screen)

        while not self.closed:
            self.DrawScene()

            event = self.scr.getch()    # dequeues an event
            while (event != -1):        # while there are events to process
                
                if event == ord('q'):   self.cam.Rotate(0.05)   # rotate right
                elif event == ord('e'): self.cam.Rotate(-0.05)  # rotate left
                
                elif event == ord('w'): self.cam.MoveTangent(0.05)      # move forwards
                elif event == ord('s'): self.cam.MoveTangent(-0.05)     # move backwards
                elif event == ord('a'): self.cam.MoveNormal(0.05)       # move left
                elif event == ord('d'): self.cam.MoveNormal(-0.05)      # move right
                
                elif event == ord('r'): self.cam.posZ = max(0, min(self.cam.posZ - 0.05, 1))    # change height up
                elif event == ord('f'): self.cam.posZ = max(0, max(self.cam.posZ + 0.05, 0))    # change height down

                elif event == ord('p'): exit()  # p to exit program

                event = self.scr.getch() # dequeue the next event
            
if __name__ == "__main__":
    game = Game()
    game.Run()
            
            