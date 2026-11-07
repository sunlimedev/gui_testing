# Client Web Connection Recovery Script


# ------------------ imports -------------------------------------------------------------------------------------------


import urllib3
import requests
import webbrowser

import tkinter as tk


# ------------------ constants -----------------------------------------------------------------------------------------


# internal address of server's tailscale network
TAILNET_ADDRESS = "100.107.220.110"

# background orange hex
BG_HEX_CODE = "#ffb86a"

# button orange hex
BTN_HEX_CODE = "#ea580c"

# button hover hex
BTN_HOVER_HEX_CODE = "#ca3500"


# ------------------ GUI functions -------------------------------------------------------------------------------------


# get the server's local network address via through tailnet
def locate_server(event=None):
    # create url for local address API call
    url = "https://" + TAILNET_ADDRESS + "/api/addr"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    request = requests.get(url, verify=False)
    data = request.json()
    local_address = data["address"]

    webbrowser.open(f"https://{local_address}")


# do not allow the window to be closed
def on_close():
    root.deiconify()
    bring_to_top()


# bring the window to top of desktop
def bring_to_top():
    root.attributes('-topmost', True)
    root.after(500, lambda: root.attributes('-topmost', False))


# recreate button design of web app
def draw_button(canvas, color, text):
    canvas.delete("all")
    width = 380
    height = 80
    radius = 15

    canvas.create_oval(0, 0, radius * 2, radius * 2, fill=color, outline="")
    canvas.create_oval(width - radius * 2, 0, width, radius * 2, fill=color, outline="")
    canvas.create_oval(0, height - radius * 2, radius * 2, height, fill=color, outline="")
    canvas.create_oval(width - radius * 2, height - radius * 2, width, height, fill=color, outline="")

    canvas.create_rectangle(radius, 0, width - radius, height, fill=color, outline="")
    canvas.create_rectangle(0, radius, width, height - radius, fill=color, outline="")

    canvas.create_text(width / 2, height / 2, text=text, font=("Helvetica", 20, "bold"), fill="white")


# create button with hover animation
def create_rounded_button(canvas, text, command):
    draw_button(canvas, BTN_HEX_CODE, text)

    canvas.bind("<Enter>", lambda e: draw_button(canvas, BTN_HOVER_HEX_CODE, text))
    canvas.bind("<Leave>", lambda e: draw_button(canvas, BTN_HEX_CODE, text))

    canvas.bind("<Button-1>", command)


# ------------------ script ----------------------------------------------------------------------------------------------


# build window object
root = tk.Tk()

# set window title
root.title("Erie Bike Co-op")

# set dimensions and background color
root.geometry("450x250")
root.configure(bg=BG_HEX_CODE)
frame = tk.Frame(root, bg=BG_HEX_CODE)
frame.pack(expand=True)

# create a space for a button to exist
btn_canvas = tk.Canvas(frame, width=380, height=80, bg=BG_HEX_CODE, highlightthickness=0)
btn_canvas.pack()

# draw the button and write some text
create_rounded_button(btn_canvas, "Click me to re-open the website", locate_server)

# reopen the window to top on close
root.protocol("WM_DELETE_WINDOW", on_close)
bring_to_top()

root.mainloop()
