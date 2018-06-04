class Wspolrzedne:
    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y

    def set_xy(self, x, y):
        self.__x = x
        self.__y = y

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_xy(self):
        return self.__x, self.__y

    def equal(self, other):
        if self.__x == other.__x:
            if self.__y == other.__y:
                return True
        return False

    def __repr__(self):
        return 'Punkt({0}, {1})'.format(self.__x, self.__y)

    def __eq__(self, other):
        if isinstance(other, Wspolrzedne):
            if self.__x == other.__x:
                if self.__y == other.__y:
                    return True
        return False

    def __ne__(self, other):
        if isinstance(other, Wspolrzedne):
            if self.__x == other.__x:
                if self.__y == other.__y:
                    return True
        return False
