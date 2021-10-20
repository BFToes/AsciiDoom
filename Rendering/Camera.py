from math import cos, sin

class Camera:
    """a camera for raycasting."""
    def __init__(self, posX : float, posY : float, posZ : float, rotation = 0):
        """
        posx - the x cooridinate of the position\n
        posy - the y coordinate of the position\n
        posz - the z coordinate of the position\n
        rotation - the rotation from north of the position
        """
        self.posX = posX
        """the x component of the position"""
        self.posY = posY
        """the y component of the position"""
        self.posZ = posZ
        """the z component of the position"""
        # a vector of the direction
        self._dirX = -1
        """the normalized x component of the direction vector.\n\n warning - dont set directly"""
        self._dirY = 0
        """the normalized y component of the direction vector.\n\n warning - dont set directly"""
        # the camera plane
        self._planeX = 0.0
        """the normalized x component of the plane vector.\n\n warning - dont set directly"""  
        self._planeY = 0.66
        """the normalized y component of the plane vector.\n\n warning - dont set directly""" 
        self.Rotate(rotation)

    def Rotate(self, angle : float):
        """
        rotates the camera by angle(radians) from the current angle.
        """
        olddirx = self._dirX
        self._dirX = cos(angle) * self._dirX - sin(angle) * self._dirY
        self._dirY = sin(angle) * olddirx + cos(angle) * self._dirY

        oldplaneX = self._planeX
        self._planeX = cos(angle) * self._planeX - sin(angle) * self._planeY
        self._planeY = sin(angle) * oldplaneX + cos(angle) * self._planeY

    def MoveTangent(self, magnitude : float):
        """
        moves the position forward by 'magnitude'. \n
        a positive 'magnitude' results in a movement forwards.\n
        a negative 'magnitude' results in a movement backwards.
        """
        self.posX += self._dirX * magnitude # posx += dirx
        self.posY += self._dirY * magnitude # posy += diry

    def MoveNormal(self, magnitude : float):
        """
        moves the position along the normal to the direction vector by 'magnitude'. \n
        a positive 'magnitude' results in a movement left.\n
        a negative 'magnitude' results in a movement right.
        """
        self.posX -= self._dirY * magnitude # posx -= diry
        self.posY += self._dirX * magnitude # posy += dirx