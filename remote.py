import subprocess
import tkinter as tk
import socket
import netifaces
import threading

ADB_DEVICE = None


def get_local_network():
    gws = netifaces.gateways()
    default = gws['default'][netifaces.AF_INET][1]
    addrs = netifaces.ifaddresses(default)
    ip = addrs[netifaces.AF_INET][0]['addr']
    return ".".join(ip.split(".")[:3])


def scan_network():
    network = get_local_network()
    status.config(text="Scanning...")

    for i in range(1,255):
        ip = f"{network}.{i}"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            result = s.connect_ex((ip,5555))
            if result == 0:
                devices_list.insert(tk.END, ip)
            s.close()
        except:
            pass

    status.config(text="Scan finished")


def connect_selected():
    global ADB_DEVICE
    selection = devices_list.get(devices_list.curselection())
    subprocess.run(["adb","connect",selection])
    ADB_DEVICE = selection
    status.config(text=f"Connected : {selection}")


def key(code):
    if ADB_DEVICE:
        subprocess.Popen([
            "adb","-s",ADB_DEVICE,"shell","input","keyevent",str(code)
        ])


def send_text():
    if ADB_DEVICE:
        text = text_entry.get().replace(" ","%s")
        subprocess.Popen([
            "adb","-s",ADB_DEVICE,"shell","input","text",text
        ])


def launch(pkg):
    subprocess.Popen([
        "adb","-s",ADB_DEVICE,"shell","monkey","-p",pkg,"1"
    ])


def wake():
    key(26)


# Interface

root = tk.Tk()
root.title("FireStick Remote")

top = tk.Frame(root)
top.pack()

scan_btn = tk.Button(top,text="Scan FireStick",command=lambda:threading.Thread(target=scan_network).start())
scan_btn.pack()

devices_list = tk.Listbox(root,width=30)
devices_list.pack()

connect_btn = tk.Button(root,text="Connect",command=connect_selected)
connect_btn.pack()

status = tk.Label(root,text="Disconnected")
status.pack()


# TELECOMMANDE

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Button(frame,text="⬆",width=5,height=2,command=lambda:key(19)).grid(row=0,column=1)

tk.Button(frame,text="⬅",width=5,height=2,command=lambda:key(21)).grid(row=1,column=0)
tk.Button(frame,text="OK",width=5,height=2,command=lambda:key(66)).grid(row=1,column=1)
tk.Button(frame,text="➡",width=5,height=2,command=lambda:key(22)).grid(row=1,column=2)

tk.Button(frame,text="⬇",width=5,height=2,command=lambda:key(20)).grid(row=2,column=1)


nav = tk.Frame(root)
nav.pack()

tk.Button(nav,text="Home",command=lambda:key(3)).pack(side="left")
tk.Button(nav,text="Back",command=lambda:key(4)).pack(side="left")
tk.Button(nav,text="Wake",command=wake).pack(side="left")


apps = tk.Frame(root)
apps.pack(pady=10)

tk.Button(apps,text="Netflix",command=lambda:launch("com.netflix.ninja")).pack(side="left")
tk.Button(apps,text="Prime",command=lambda:launch("com.amazon.amazonvideo.livingroom")).pack(side="left")
tk.Button(apps,text="YouTube",command=lambda:launch("com.google.android.youtube.tv")).pack(side="left")
tk.Button(apps,text="Disney+",command=lambda:launch("com.disney.disneyplus")).pack(side="left")


text_frame = tk.Frame(root)
text_frame.pack()

text_entry = tk.Entry(text_frame)
text_entry.pack(side="left")

tk.Button(text_frame,text="Send",command=send_text).pack(side="left")


root.mainloop()