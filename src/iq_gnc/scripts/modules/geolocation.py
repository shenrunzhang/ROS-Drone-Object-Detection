from math import *

def pixel_to_loc(px, py, drone_x, drone_y, drone_z, image_height, image_width, H_fov):
    """
    Returns real coordinates of a pixel in an aerial image.
    Assumes that px=0, py=0 at bottom left corner of image.

    Args:
        px (int): _description_
        py (int): _description_
        drone_x (float): _description_
        drone_y (float): _description_
        image_width (int): _description_
        image_height (int): _description_
        H_fov (float): _description_
    
    Returns:
        x_real, y_real: real coordinates of pixel
    """

    # Calculate vertical fov angle
    aspect_ratio = image_height / image_width
    V_fov = 2 * atan(tan(H_fov / 2) * aspect_ratio)

    # Get the angle dispacement from the image center in x and y directions
    horizontal_angle = (px - image_width / 2) * (H_fov / image_width)
    vertical_angle = (py - image_height / 2) * (V_fov / image_height)

    # Find dispacement from center in real world units in x and y directions
    delta_x = drone_z * tan(horizontal_angle)
    delta_y = drone_z * tan(vertical_angle)

    # Get real world coordinates of target
    x_real = drone_x + delta_x
    y_real = drone_y + delta_y

    return round(x_real, 2), round(y_real,2)