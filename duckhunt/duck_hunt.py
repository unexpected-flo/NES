import cv2
import mss
import numpy as np
import sys
import time
import win32api, win32con
from pynput.keyboard import Key

from detect_duck import find_cursor_coords
from grab_screen import get_game_window_location
from keyboard_logger import Keylogger


def play_duck_hunt(window_name):
    window = get_game_window_location(window_name)
    offset_border = 8  # Determined empirically to crop the game image a bit more closely
    offset_top = 31
    window = (window[0] + offset_border, window[1] + offset_top, window[2] - offset_border, window[3] - offset_border)

    logger = Keylogger()

    with mss.mss() as sct:
        while logger.pressed_key is not Key.esc:
            sct_img = np.asarray(sct.grab(window))
            found, x, y = find_cursor_coords(sct_img)
            if found:
                cv2.circle(sct_img, (x, y), 25, (57, 255, 20), -1)
                # Draws a green circle centered on where the program is targeting

                win32api.SetCursorPos((x + window[0], y + window[1]))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                time.sleep(0.02)  # Necessary for the emulator to register the click
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

                print(x, y, window[0], window[1])
            cv2.imshow("screen", sct_img)
            key = cv2.waitKey(1)  # Refresh the agent display


if __name__ == "__main__":
    play_duck_hunt(sys.argv[1])
