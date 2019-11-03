import tkinter
from PIL import Image, ImageTk


def select_from_image(img):
    root = tkinter.Tk()
    root.wm_attributes("-topmost", True)
    root.state("icon")
    global from_x, from_y, is_select, captured
    from_x = 0
    from_y = 0
    is_select = False
    captured = False
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    top = tkinter.Toplevel(root, width=screen_width, height=screen_height)
    top.overrideredirect(True)
    canvas = tkinter.Canvas(top, bg="white", width=screen_width, height=screen_height)
    bg_img = ImageTk.PhotoImage(img)
    canvas.create_image(screen_width // 2, screen_height // 2, image=bg_img)

    def on_left_button_down(event):
        global from_x, from_y, is_select
        from_x = event.x
        from_y = event.y
        is_select = True

    canvas.bind("<Button-1>", on_left_button_down)

    def on_left_button_move(event):
        if not is_select:
            return
        global last_draw
        try:
            canvas.delete(last_draw)
        except:
            pass
        last_draw = canvas.create_rectangle(
            from_x, from_y, event.x, event.y, outline="red"
        )

    canvas.bind("<B1-Motion>", on_left_button_move)

    def on_left_button_up(event):
        global x_min, x_max, y_min, y_max, captured
        captured = True
        x_min, x_max = sorted([from_x, event.x])
        y_min, y_max = sorted([from_y, event.y])
        top.destroy()
        root.destroy()

    canvas.bind("<ButtonRelease-1>", on_left_button_up)

    def on_right_button_up(event):
        top.destroy()
        root.destroy()

    canvas.bind("<ButtonRelease-3>", on_right_button_up)
    canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    root.mainloop()
    if captured:
        return x_min, y_min, x_max, y_max
    else:
        return None
