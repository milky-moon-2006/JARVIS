import ctypes
import tkinter as tk
import math
import random
import time
import threading

# Make Windows report the real physical display size instead of a scaled
# logical size. This prevents the HUD from being smaller than the laptop screen.
if __import__("sys").platform.startswith("win"):
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# ============================================================
# JARVIS 1 — FULL SCREEN REACTOR HUD
# Designed to closely match the supplied JARVIS reference UI.
# Existing assistant controls are kept through:
#   set_command_handler(...)
#   set_mic_handler(...)
#   run_ui()
# ============================================================

BG = "#02060D"
GRID = "#061521"
CYAN = "#11DFFF"
CYAN2 = "#008DFF"
BLUE = "#1678FF"
WHITE = "#E8FBFF"
GREEN = "#00FF9D"
RED = "#FF315C"
MUTED = "#5B91A5"
PANEL = "#03111B"
BORDER = "#087A9E"

app = tk.Tk()
app.title("J.A.R.V.I.S — JARVIS 1")
app.configure(bg=BG)
app.config(cursor="arrow")

# TRUE BORDERLESS FULL SCREEN on Windows.
app.overrideredirect(True)
app.attributes("-topmost", True)

W = app.winfo_screenwidth()
H = app.winfo_screenheight()

app.geometry(f"{W}x{H}+0+0")
app.update_idletasks()

if __import__("sys").platform.startswith("win"):
    try:
        hwnd = app.winfo_id()
        HWND_TOPMOST = -1
        SWP_NOSIZE = 0x0001
        SWP_NOMOVE = 0x0002
        SWP_NOACTIVATE = 0x0010
        ctypes.windll.user32.SetWindowPos(
            hwnd, HWND_TOPMOST, 0, 0, W, H,
            SWP_NOSIZE | SWP_NOMOVE | SWP_NOACTIVATE
        )
    except Exception:
        pass

canvas = tk.Canvas(
    app,
    bg=BG,
    highlightthickness=0,
    bd=0,
)
canvas.pack(fill="both", expand=True)

command_handler = None
mic_handler = None

status = "● SYSTEMS ONLINE & OPTIMAL"
message = "HOW CAN I HELP YOU, SIR?"
angle = 0.0
pulse = 0.0

particles = [
    [random.randint(0, W), random.randint(0, H), random.choice([1, 1, 1, 2])]
    for _ in range(110)
]


def set_command_handler(handler):
    global command_handler
    command_handler = handler


def set_mic_handler(handler):
    global mic_handler
    mic_handler = handler
    
    # ============================================================
# QUICK ACCESS BUTTON CLICK
# ============================================================

def quick_access_click(event):

    x = event.x
    y = event.y

    # Quick Access panel
    rx1 = max(W - 335, int(W * 0.77))
    rx2 = W - 34

    panel_top = 315
    panel_bottom = 500

    # Click must be inside Quick Access panel
    if not (rx1 <= x <= rx2):
        return

    if not (panel_top <= y <= panel_bottom):
        return

    # Button area starts at y=359
    if y < 359:
        return

    cw = (rx2 - rx1) / 3
    ch = (panel_bottom - 359) / 2

    column = int((x - rx1) / cw)
    row = int((y - 359) / ch)

    if column < 0 or column > 2:
        return

    if row < 0 or row > 1:
        return

    commands = [
        [
            "open google",
            "open youtube",
            "open chatgpt"
        ],
        [
            "open calculator",
            "open camera",
            "open notepad"
        ]
    ]

    command = commands[row][column]

    print("QUICK ACCESS:", command)

    set_status("● THINKING")
    set_message(command.upper())

    if command_handler:

        threading.Thread(
            target=command_handler,
            args=(command,),
            daemon=True
        ).start()

    else:

        set_status("● SYSTEM ONLINE")
        set_message(
            "Command handler not connected."
        )


def set_status(value):
    global status
    status = str(value)


def set_message(value):
    global message
    message = str(value)


def text(x, y, value, size=10, fill=CYAN, anchor="center"):
    canvas.create_text(
        x, y,
        text=value,
        fill=fill,
        font=("Consolas", size, "bold"),
        anchor=anchor,
    )


def line(x1, y1, x2, y2, fill=CYAN, width=1):
    canvas.create_line(x1, y1, x2, y2, fill=fill, width=width)


def rect(x1, y1, x2, y2, fill=PANEL, outline=BORDER, width=1):
    canvas.create_rectangle(
        x1, y1, x2, y2,
        fill=fill,
        outline=outline,
        width=width,
    )


def clipped_panel(x1, y1, x2, y2, title):
    # Angular sci-fi panel frame.
    cut = 12

    pts = [
        x1 + cut, y1,
        x2 - cut, y1,
        x2, y1 + cut,
        x2, y2 - cut,
        x2 - cut, y2,
        x1 + cut, y2,
        x1, y2 - cut,
        x1, y1 + cut,
    ]

    canvas.create_polygon(
        pts,
        fill=PANEL,
        outline=BORDER,
        width=1,
    )

    text(x1 + 18, y1 + 22, title, 11, CYAN, "w")
    line(x1 + 18, y1 + 43, x2 - 18, y1 + 43, "#0B3B4D", 1)

    # Decorative slashes.
    for i in range(4):
        line(
            x2 - 62 + i * 9,
            y1 + 15,
            x2 - 53 + i * 9,
            y1 + 8,
            CYAN2,
            2,
        )


def draw_background():
    canvas.create_rectangle(0, 0, W, H, fill=BG, outline="")

    # Fine grid.
    grid = max(45, int(W / 36))
    for x in range(0, W, grid):
        line(x, 0, x, H, GRID, 1)

    for y in range(0, H, grid):
        line(0, y, W, y, GRID, 1)

    # Circuit-like horizontal traces.
    for y in (int(H * .08), int(H * .14), int(H * .86), int(H * .93)):
        line(0, y, int(W * .18), y, "#073248", 1)
        line(int(W * .82), y, W, y, "#073248", 1)

    # Tiny stars / data points.
    for p in particles:
        p[1] += p[2] * 0.22
        if p[1] > H:
            p[0] = random.randint(0, W)
            p[1] = 0

        canvas.create_oval(
            p[0] - p[2],
            p[1] - p[2],
            p[0] + p[2],
            p[1] + p[2],
            fill="#087FB1",
            outline="",
        )


def draw_header():
    text(46, 35, "JARVIS SYSTEMS", 18, CYAN, "w")
    text(46, 62, "JARVIS 1.0.0  //  LOCAL AI CORE", 9, MUTED, "w")

    # ONLINE indicator.
    text(300, 50, "ONLINE", 12, GREEN, "w")
    for i in range(4):
        line(370 + i * 12, 43, 378 + i * 12, 30, CYAN2, 3)

    # Center title.
    text(W / 2, 45, "J A R V I S", 38, WHITE)
    text(W / 2, 82, "I AM AT YOUR SERVICE, SIR.", 11, RED)

    # Time and system icons.
    now = time.localtime()
    clock = time.strftime("%H:%M:%S", now)
    date = time.strftime("%A, %d %B %Y", now)

    text(W - 48, 35, clock, 22, CYAN, "e")
    text(W - 48, 61, date.upper(), 9, MUTED, "e")

    text(W - 230, 37, "◉", 13, CYAN)
    text(W - 195, 37, "⌁", 15, CYAN)
    text(W - 155, 37, "▣ 100%", 10, CYAN)


def draw_status_panel(x1, y1, x2, y2):
    clipped_panel(x1, y1, x2, y2, "SYSTEM STATUS")

    rows = [
        ("CORE SYSTEM", "ONLINE"),
        ("AI ENGINE", "ONLINE"),
        ("VOICE MODULE", "READY"),
        ("VISION SYSTEM", "READY"),
        ("SECURITY PROTOCOL", "ACTIVE"),
    ]

    y = y1 + 75
    for label, value in rows:
        text(x1 + 28, y, label, 10, "#A9C9D4", "w")
        text(x2 - 28, y, value, 10, GREEN, "e")
        y += 34


def draw_voice_panel(x1, y1, x2, y2):
    clipped_panel(x1, y1, x2, y2, "VOICE RECOGNITION")

    base_y = y1 + 105
    bars = 48
    span = (x2 - x1 - 45) / (bars - 1)

    for i in range(bars):
        wave = (
            abs(math.sin(i * 0.65 + angle * 0.05))
            * (12 + 20 * abs(math.sin(i * 0.27 + angle * 0.02)))
        )
        xx = x1 + 22 + i * span
        line(xx, base_y - wave, xx, base_y + wave, CYAN, 2)

    text(x1 + 20, y2 - 28, "● LISTENING / READY", 10, GREEN, "w")


def draw_time_panel(x1, y1, x2, y2):
    clipped_panel(x1, y1, x2, y2, "CURRENT TIME")

    now = time.localtime()
    clock = time.strftime("%H:%M:%S", now)
    date = time.strftime("%A, %d %B %Y", now)

    # Clock circle.
    cx = x1 + 48
    cy = y1 + 98
    r = 25
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=CYAN, width=2)

    for i in range(12):
        a = math.radians(i * 30 - 90)
        x_a = cx + math.cos(a) * 20
        y_a = cy + math.sin(a) * 20
        x_b = cx + math.cos(a) * 24
        y_b = cy + math.sin(a) * 24
        line(x_a, y_a, x_b, y_b, CYAN, 1)

    now_seconds = time.localtime().tm_sec
    a = math.radians(now_seconds * 6 - 90)
    line(cx, cy, cx + math.cos(a) * 17, cy + math.sin(a) * 17, CYAN, 2)

    text(x1 + 88, y1 + 87, clock, 28, CYAN, "w")
    text(x1 + 88, y1 + 117, date, 10, WHITE, "w")


def draw_diagnostics(x1, y1, x2, y2):
    clipped_panel(x1, y1, x2, y2, "DIAGNOSTICS")

    rows = [
        ("OLLAMA", "LOCAL"),
        ("PYTHON", "ACTIVE"),
        ("NETWORK", "READY"),
        ("AUDIO", "READY"),
        ("STATUS", "STABLE"),
    ]

    y = y1 + 75
    for label, value in rows:
        text(x1 + 28, y, label, 10, "#A9C9D4", "w")
        text(x2 - 28, y, value, 10, GREEN, "e")
        y += 34


def draw_quick_access(x1, y1, x2, y2):
    clipped_panel(x1, y1, x2, y2, "QUICK ACCESS")

    items = [
        ("G", "GOOGLE"),
        ("▶", "YOUTUBE"),
        ("◉", "CHATGPT"),
        ("▦", "CALCULATOR"),
        ("◉", "CAMERA"),
        ("▤", "NOTEPAD"),
    ]

    width = (x2 - x1) / 3
    top = y1 + 88

    for i, (icon, label) in enumerate(items):
        col = i % 3
        row = i // 3

        cx = x1 + width * col + width / 2
        cy = top + row * 76

        text(cx, cy, icon, 23, CYAN2)
        text(cx, cy + 29, label, 8, WHITE)


def draw_shortcuts(x1, y1, x2, y2):
    clipped_panel(x1, y1, x2, y2, "SHORTCUT COMMANDS")

    left = [
        ("◉", "OPEN CHROME"),
        ("⌕", "SEARCH GOOGLE"),
        ("▶", "SEARCH YOUTUBE"),
        ("▤", "OPEN NOTEPAD"),
        ("▦", "OPEN CALCULATOR"),
    ]

    right = [
        ("♙", "LOCK LAPTOP"),
        ("◉", "SHUTDOWN"),
        ("↻", "RESTART"),
        ("◉", "OPEN CAMERA"),
        ("●", "SEND WHATSAPP"),
    ]

    y = y1 + 70

    for icon, label in left:
        text(x1 + 22, y, icon, 13, CYAN, "w")
        text(x1 + 48, y, label, 9, "#D4EAF0", "w")
        y += 30

    y = y1 + 70

    for icon, label in right:
        color = RED if label == "SHUTDOWN" else CYAN
        text(x1 + (x2-x1)/2 + 10, y, icon, 13, color, "w")
        text(x1 + (x2-x1)/2 + 36, y, label, 9, "#D4EAF0", "w")
        y += 30


def draw_reactor():
    cx = W / 2
    cy = H * 0.46

    # Outer rings.
    rings = [
        (245, "#07344A", 1),
        (225, "#07506B", 2),
        (205, "#0086B8", 2),
        (185, CYAN2, 2),
        (165, CYAN, 2),
        (142, "#44EEFF", 2),
        (118, CYAN, 2),
        (94, "#A5F8FF", 2),
    ]

    for r, color, width in rings:
        canvas.create_oval(
            cx-r, cy-r,
            cx+r, cy+r,
            outline=color,
            width=width,
        )

    # Rotating arcs.
    canvas.create_arc(
        cx-225, cy-225, cx+225, cy+225,
        start=angle,
        extent=70,
        outline=CYAN,
        width=7,
    )

    canvas.create_arc(
        cx-225, cy-225, cx+225, cy+225,
        start=angle + 145,
        extent=90,
        outline=BLUE,
        width=4,
    )

    canvas.create_arc(
        cx-225, cy-225, cx+225, cy+225,
        start=angle + 275,
        extent=42,
        outline=RED,
        width=4,
    )

    canvas.create_arc(
        cx-165, cy-165, cx+165, cy+165,
        start=-angle * 1.5,
        extent=105,
        outline=CYAN,
        width=7,
    )

    canvas.create_arc(
        cx-165, cy-165, cx+165, cy+165,
        start=-angle * 1.5 + 180,
        extent=95,
        outline=BLUE,
        width=4,
    )

    # Radial targeting lines.
    for i in range(12):
        a = math.radians(angle + i * 30)
        r1 = 180
        r2 = 210 if i % 2 == 0 else 195

        line(
            cx + math.cos(a) * r1,
            cy + math.sin(a) * r1,
            cx + math.cos(a) * r2,
            cy + math.sin(a) * r2,
            CYAN2,
            1,
        )

    # Tick marks.
    for i in range(48):
        a = math.radians(i * 7.5)
        r1 = 230
        r2 = 238 if i % 3 == 0 else 234

        line(
            cx + math.cos(a) * r1,
            cy + math.sin(a) * r1,
            cx + math.cos(a) * r2,
            cy + math.sin(a) * r2,
            CYAN,
            2,
        )

    # Reactor glow layers.
    glow = 65 + int(math.sin(time.time() * 5) * 5)

    for r, color, width in [
        (glow + 28, "#075A78", 2),
        (glow + 18, CYAN2, 3),
        (glow + 8, CYAN, 4),
    ]:
        canvas.create_oval(
            cx-r, cy-r,
            cx+r, cy+r,
            outline=color,
            width=width,
        )

    # Bright core.
    canvas.create_oval(
        cx-45, cy-45,
        cx+45, cy+45,
        fill="#087DA4",
        outline=WHITE,
        width=2,
    )

    # Triangular reactor symbol.
    points = []
    for deg in (-90, 30, 150):
        a = math.radians(deg)
        points.extend([
            cx + math.cos(a) * 31,
            cy + math.sin(a) * 31,
        ])

    canvas.create_polygon(
        points,
        fill="#16EFFF",
        outline=WHITE,
        width=2,
    )

    canvas.create_oval(
        cx-10, cy-10,
        cx+10, cy+10,
        fill=WHITE,
        outline="",
    )

    text(cx, cy + 82, "ARC REACTOR", 11, CYAN)
    text(cx, cy + 102, "CORE POWER: 100%", 9, WHITE)


def draw_bottom():
    # Status label.
    text(W / 2, H - 154, status, 14, GREEN)

    # Command bar.
    x1 = W * .27
    x2 = W * .73
    y1 = H - 120
    y2 = H - 54

    clipped_panel(x1, y1, x2, y2, "")

    # Entry background is positioned above the canvas.
    text(
        x1 + 24,
        y1 + 33,
        message,
        14,
        CYAN,
        "w",
    )

    # Footer.
    text(
        46,
        H - 22,
        "JARVIS 1.0.0",
        9,
        CYAN,
        "w",
    )

    text(
        46,
        H - 7,
        "ALL SYSTEMS OPERATIONAL",
        8,
        MUTED,
        "w",
    )

    text(
        W - 46,
        H - 22,
        "CONNECTED & SECURE  //  ESC: EXIT",
        8,
        MUTED,
        "e",
    )


# ------------------------------------------------------------
# REAL INPUT CONTROLS
# ------------------------------------------------------------

input_frame = tk.Frame(
    app,
    bg="#020912",
    highlightbackground=CYAN2,
    highlightthickness=1,
)

entry = tk.Entry(
    input_frame,
    bg="#020912",
    fg=WHITE,
    insertbackground=CYAN,
    relief="flat",
    font=("Consolas", 14, "bold"),
)

entry.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10,
    pady=8,
    ipady=8,
)


def submit_command(event=None):
    command = entry.get().strip()

    if not command:
        return "break"

    entry.delete(0, "end")

    set_status("● PROCESSING COMMAND")
    set_message(command)

    if command_handler:
        threading.Thread(
            target=command_handler,
            args=(command,),
            daemon=True,
        ).start()

    return "break"


entry.bind("<Return>", submit_command)


mic_button = tk.Button(
    input_frame,
    text="🎤  SPEAK",
    bg="#075A78",
    fg=WHITE,
    activebackground="#008CFF",
    activeforeground=WHITE,
    relief="flat",
    borderwidth=0,
    font=("Consolas", 12, "bold"),
    padx=22,
    pady=10,
    command=lambda: start_microphone(),
)

mic_button.pack(
    side="right",
    padx=7,
    pady=7,
)


def start_microphone():
    if not mic_handler:
        set_message("Microphone handler is not connected.")
        return

    mic_button.config(
        state="disabled",
        text="● LISTENING",
    )

    set_status("● LISTENING")

    threading.Thread(
        target=run_microphone,
        daemon=True,
    ).start()


def run_microphone():
    try:
        mic_handler()

    except Exception as exc:
        print("MIC ERROR:", exc)
        set_message("Microphone error. Check your microphone.")

    finally:
        try:
            app.after(
                0,
                lambda: mic_button.config(
                    state="normal",
                    text="🎤  SPEAK",
                ),
            )

            app.after(
                0,
                lambda: set_status("● SYSTEMS ONLINE & OPTIMAL"),
            )

        except tk.TclError:
            pass


input_frame.place(
    relx=0.5,
    rely=0.90,
    relwidth=0.47,
    anchor="center",
)


# ------------------------------------------------------------
# ANIMATION
# ------------------------------------------------------------

def draw():
    global angle, pulse

    canvas.delete("all")

    draw_background()
    draw_header()

    # Responsive side panel sizes.
    left_x1 = 32
    left_x2 = int(W * 0.25)

    right_x1 = int(W * 0.75)
    right_x2 = W - 32

    top_y = int(H * 0.13)

    draw_status_panel(
        left_x1,
        top_y,
        left_x2,
        int(H * 0.36),
    )

    draw_voice_panel(
        left_x1,
        int(H * 0.39),
        left_x2,
        int(H * 0.62),
    )

    draw_time_panel(
        left_x1,
        int(H * 0.65),
        left_x2,
        int(H * 0.87),
    )

    draw_diagnostics(
        right_x1,
        top_y,
        right_x2,
        int(H * 0.36),
    )

    draw_quick_access(
        right_x1,
        int(H * 0.39),
        right_x2,
        int(H * 0.62),
    )

    draw_shortcuts(
        right_x1,
        int(H * 0.65),
        right_x2,
        int(H * 0.92),
    )

    draw_reactor()
    draw_bottom()

    angle = (angle + 1.6) % 360
    pulse += 0.05

    app.after(30, draw)


# ------------------------------------------------------------
# FULL SCREEN KEYS
# ------------------------------------------------------------

def toggle_fullscreen(event=None):
    global W, H
    W = app.winfo_screenwidth()
    H = app.winfo_screenheight()
    app.overrideredirect(True)
    app.attributes("-topmost", True)
    app.geometry(f"{W}x{H}+0+0")
    app.update_idletasks()


def refresh_display(event=None):
    global W, H
    W = app.winfo_screenwidth()
    H = app.winfo_screenheight()
    app.geometry(f"{W}x{H}+0+0")
    app.update_idletasks()


def exit_jarvis(event=None):
    app.destroy()


app.bind("<F11>", toggle_fullscreen)
app.bind("<F12>", refresh_display)
app.bind("<Escape>", exit_jarvis)

entry.focus_set()


def run_ui():
    app.bind(
        "<Button-1>",
        quick_access_click
    )

    draw()

    app.mainloop()


if __name__ == "__main__":
    run_ui()