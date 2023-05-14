import cv2


def get_image_dimensions(image_path):
    # read image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
 
    # height, width
    height = img.shape[0]
    width = img.shape[1]

    
    return (height, width)
