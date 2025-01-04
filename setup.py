import pyautogui

USER_WIDTH, USER_HEIGHT = 0, 0
USER_WIDTH_MODIFIER, USER_HEIGHT_MODIFIER = 1, 1


def setup_res_modifier():
    # Full HD resolution for comparison
    FULL_HD_WIDTH = 1920
    FULL_HD_HEIGHT = 1080

    # Get the current screen resolution
    screen_width, screen_height = pyautogui.size()
    global USER_HEIGHT, USER_WIDTH, USER_WIDTH_MODIFIER, USER_HEIGHT_MODIFIER
    USER_WIDTH = pyautogui.size().width
    USER_HEIGHT = pyautogui.size().height

    # Calculate the modifiers
    USER_WIDTH_MODIFIER = screen_width / FULL_HD_WIDTH
    USER_HEIGHT_MODIFIER = screen_height / FULL_HD_HEIGHT
    print(f"Width Modifier: {USER_WIDTH_MODIFIER}, Height Modifier: {USER_HEIGHT_MODIFIER}")
