import keyboard
import time
import capture
import screen
import pytesseract
import cv2
import translater
import pyperclip
import win32.win32api as win32api
import win32.lib.win32con as win32con
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"

previous_key_status = False
previous_text = pyperclip.paste()


def crop(img_array, box):
    return img_array[box[1] : box[3], box[0] : box[2]]


def show_translate_box(text, origin=None):
    global previous_text
    if origin == None:
        is_copy = win32api.MessageBox(0, text, "是否复制到剪贴板", win32con.MB_YESNO)
    else:
        is_copy = win32api.MessageBox(
            0, f"识别到的文本：\n{origin}\n\n翻译结果：\n{text}", "是否复制翻译结果", win32con.MB_YESNO
        )
    if is_copy == win32con.IDYES:
        pyperclip.copy(text)
        previous_text = text


def translate_screenshot(get_new_key):
    screen_array = screen.grab()
    rgb_screen_array = cv2.cvtColor(screen_array, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb_screen_array)
    region = capture.select_from_image(img)
    if region != None:
        width = region[2] - region[0]
        height = region[3] - region[1]
        rect_area = width * height
        half_rect_area = rect_area // 2
        img = crop(screen_array, region)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        retval, img_1 = cv2.threshold(img, 63, 255, cv2.THRESH_BINARY)
        retval, img_3 = cv2.threshold(img, 191, 255, cv2.THRESH_BINARY)
        count_1 = cv2.countNonZero(img_1)
        reverse_1 = False
        if count_1 < half_rect_area:
            reverse_1 = True
            count_1 = rect_area - count_1
        count_3 = cv2.countNonZero(img_3)
        reverse_3 = False
        if count_3 < half_rect_area:
            reverse_3 = True
            count_3 = rect_area - count_3
        if count_1 < count_3:
            img = img_1
            reverse = reverse_1
        else:
            img = img_3
            reverse = reverse_3
        if reverse:
            img = 255 - img
        text = pytesseract.image_to_string(img)
        result = translater.translate(text, get_new_key)
        show_translate_box(result, text)


refresh_key_time = 60.0
refresh_time_remain = refresh_key_time
get_new_key = False

print("复制需要翻译的文本，或者按Ctrl+>截屏并选取需要翻译的区域")
while True:
    time.sleep(0.01)
    if not get_new_key:
        refresh_time_remain -= 0.01
        if refresh_time_remain <= 0.0:
            get_new_key = True
    text = pyperclip.paste()
    if text != previous_text:
        previous_text = text
        result = translater.translate(text)
        show_translate_box(result)
        continue
    if not keyboard.check(keyboard.VK_CODE["."]):
        previous_key_status = False
        continue
    if previous_key_status:
        continue
    previous_key_status = True
    if not keyboard.check(keyboard.VK_CODE["left_control"]):
        continue
    translate_screenshot(get_new_key)
    if get_new_key:
        get_new_key = False
        refresh_time_remain = refresh_key_time
