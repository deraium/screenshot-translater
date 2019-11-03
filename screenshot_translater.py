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


def translate_screenshot():
    screen_array = screen.grab()
    rgb_screen_array = cv2.cvtColor(screen_array, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb_screen_array)
    region = capture.select_from_image(img)
    if region != None:
        img_array = crop(screen_array, region)
        text = pytesseract.image_to_string(img_array)
        result = translater.translate(text)
        show_translate_box(result, text)

print('复制需要翻译的文本，或者按Ctrl+>截屏并选取需要翻译的区域')
while True:
    time.sleep(0.01)
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
    translate_screenshot()
