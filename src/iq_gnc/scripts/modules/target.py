import numpy as np
import copy

class Target:
    def __init__(self, image: np.ndarray, c_x: int, c_y: int, b_box: tuple, shape: str=None, color: str = None):
        """
        Initializer
        - "image" is the cv2 image of the target
        - c_x is the x-coordinate of the center of the target from the perspective the drone's camera
        - c_y is the y-coordinate of the center of the target from the perspective the drone's camera
        - Both c_x and c_y are integers as they are pixel coordinates
        - shape: shape of the target
        - color: color of the target
        """
        self._image = image
        self.b_box = b_box
        self._c_x = c_x
        self._c_y = c_y
        self._shape = shape
        self._color = color

    def get_image(self):
        return copy.deepcopy(self._image)

    def get_x(self):
        return int(self._c_x)

    def get_y(self):
        return int(self._c_y)

    def get_bbox(self):
        return tuple(self.b_box)
    
    def get_shape(self):
        return self._shape
        
    def get_color(self):
        return self._color

    def set_x(self, c_x):
        self._c_x = c_x

    def set_y(self, c_y):
        self._c_y = c_y

    def set_shape(self, shape):
        self._shape = shape
    
    def set_color(self, color):
        self._color = color
    

