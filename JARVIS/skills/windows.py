import subprocess
APPS={"chrome":["cmd","/c","start","","chrome"],"edge":["cmd","/c","start","","msedge"],
"notepad":["notepad.exe"],"calculator":["calc.exe"],"calc":["calc.exe"],
"explorer":["explorer.exe"],"file explorer":["explorer.exe"],"vscode":["code"],"vs code":["code"]}
def open_app(name):
    cmd=APPS.get(name.lower())
    if not cmd: return False
    try: subprocess.Popen(cmd); return True
    except Exception as e: print("APP ERROR:",e); return False
def lock(): subprocess.run(["rundll32.exe","user32.dll","LockWorkStation"])
def shutdown(): subprocess.run(["shutdown","/s","/t","10"])
def restart(): subprocess.run(["shutdown","/r","/t","10"])
def cancel_shutdown(): subprocess.run(["shutdown","/a"])
