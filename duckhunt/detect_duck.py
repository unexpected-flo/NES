import numpy as np
import cv2

duck_templates = ["./diag_l.tif", "./diag_r.tif", "flat_l.tif", "flat_r.tif", "flat_l2.tif", "flat_r2.tif"]


def find_cursor_coords(image):
    """ Uses OpenCV template matching on the templates listed in duck templates and return the x,y coordinates
    of the center of the match in the image if found"""
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    for duck in duck_templates:
        template = cv2.imread(duck)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        threshold = 0.49
        res = np.where(result >= threshold)
        if len(res[0]) > 0:
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
            (startX, startY) = maxLoc
            endX = startX + template.shape[1]
            endY = startY + template.shape[0]

            found = True
            x_coords = int((startX + (endX-startX)/2))
            y_coords = int((startY + (endY-startY)/2))
            break
        else:
            found = False
            x_coords = -1
            y_coords = -1
    return found, x_coords, y_coords


if __name__ == '__main__':
    from grab_screen import get_game_window_location
    import mss
    window = get_game_window_location('Mesen - Duck Hunt (PC10)') # Change here to test on another window
    offset_border = 8  # offsets found empirically to remove space around the game image
    offset_top = 31
    window = (window[0] + offset_border, window[1] + offset_top, window[2] - offset_border, window[3] - offset_border)
    print(window)
    with mss.mss() as sct:
        while True:
            sct_img = np.asarray(sct.grab(window))
            found, x, y = find_cursor_coords(sct_img)
            if found:
                cv2.circle(sct_img, (x, y), 10, (57, 255, 20), -1)
            cv2.imshow("screen", sct_img)
            key = cv2.waitKey(1)
