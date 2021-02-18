from math import sqrt, sin, cos

class Vector:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    ### The usual vector operations ###

    def scale(self, scalar):
        return self.__mul__(scalar)

    def norm(self):
        return sqrt(self * self)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def normalize(self):
        if self.norm() != 0:
            return self / self.norm()
        else:
            return Vector(0, 0, 0)

    def rotate(self, theta):
        x = self.x * cos(theta) - self.y * sin(theta)
        y = self.x * sin(theta) + self.y * cos(theta)
        return Vector(x, y)

    ### The "magic functions" of the class ###

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector(x, y, z)

    def __neg__(self):
        x = - self.x
        y = - self.y
        z = - self.z
        return Vector(x, y, z)

    def __mul__(self, other):
        if type(self) == type(other):
            return self.dot(other)
        else:
            x = self.x * other
            y = self.y * other
            z = self.z * other
            return Vector(x, y, z)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        x = self.x / scalar
        y = self.y / scalar
        z = self.z / scalar
        return Vector(x, y, z)

    def __repr__(self):
        return 'Vector(%s, %s, %s)' % (str(self.x), str(self.y), str(self.z))

    def __len__(self):
        return 3

    def __getitem__(self, key):
        a = (self.x, self.y, self.z)
        return a[key]
