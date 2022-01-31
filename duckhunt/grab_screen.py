import win32gui


def get_game_window_location(game_name):
    """Find the window named "game_name" and returns corresponding
     coordinates to draw a bounding box around that window"""

    toplist, winlist = [], []

    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)

    game = [(hwnd, title) for hwnd, title in winlist if title == game_name]
    hwnd = game[0][0]
    bbox = win32gui.GetWindowRect(hwnd)
    return bbox


if __name__ == "__main__":
    import numpy as np
    import mss
    import cv2
    window = get_game_window_location('Mesen - Duck Hunt (PC10)')  # Change here to test on another window
    with mss.mss() as sct:
        img = sct.grab(window)
        cv2.imshow("blectre", np.array(img))
        cv2.waitKey(0)
