# All code written by Caleb Cho. This tool is provided for internal use only. Do not redistribute without permission.

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
import os, sys, subprocess

""" Get absolute path to resource, works for dev and for PyInstaller .exe """
def resource_path(relative_path):
    try:
        # PyInstaller _MEIPASS temp path
        base_path = sys._MEIPASS
    except AttributeError:
        # Dev mode: relative to current file
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, *relative_path.split('/'))

FASTBOOT = resource_path("tools/fastboot.exe")

if not os.path.exists(FASTBOOT):
    messagebox.showerror("Missing fastboot.exe", f"Expected at: {FASTBOOT}")
    sys.exit(1)

FIRMWARE = {
    "bl2": resource_path("SDK1.2.0/signed_4k_bl2_1520_0.bin"),
    "bl31": resource_path("SDK1.2.0/signed_bl31.bin"),
    "bl33": resource_path("SDK1.2.0/signed_u-boot_spinand0_boot.bin"),
    "blx": resource_path("SDK1.2.0/signed_4k_blx_1520_0.bin"),
    "env": resource_path("SDK1.2.0/uboot-evm_spinand_boot_uart0.env"),
    "dtb": resource_path("SDK1.2.0/leipzig-evm-multi-sensor.dtb"),
    "kernel": resource_path("SDK1.2.0/Image"),
    "rootfs": resource_path("SDK1.2.0/rootfs.squashfs"),
    "ubifs": resource_path("SDK1.2.0/sdk1.2.0-imx678-os08a10.ubifs"),
    "script": resource_path("script.img"),
}

def get_fastboot_devices():
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        result = subprocess.run(
            [FASTBOOT, 'devices'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            startupinfo=si,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )

        devices = [line.split()[0] for line in result.stdout.strip().splitlines() if line.strip()]
        return devices
    except Exception as e:
        messagebox.showerror("Fastboot Error", f"Error running fastboot: {e}")
        return []

    #TODO: remove later: test devices
    return ["TEST123456", "MOCK987654"]

def flash_device(serial):
    # TODO: remove later: test flash
    if serial.startswith("TEST") or serial.startswith("MOCK"):
        print(f"(Mock) Simulated flashing of device: {serial}")
        return
    
    def fb(args):
        cmd = [FASTBOOT, "-s", serial] + args
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, timeout=15)

    try:
        fb(['--page-size', '512', 'boot', FIRMWARE['bl2']])
        fb(['--page-size', '512', 'boot', FIRMWARE['bl31']])
        fb(['--page-size', '512', 'boot', FIRMWARE['bl33']])
        fb(['--page-size', '512', 'boot', FIRMWARE['script']])

        fb(['erase', 'blx'])
        fb(['flash', 'blx', FIRMWARE['blx']])
        fb(['erase', 'env'])
        fb(['flash', 'env', FIRMWARE['env']])
        fb(['erase', 'u-boot'])
        fb(['flash', 'u-boot', FIRMWARE['bl33']])
        fb(['erase', 'dtb'])
        fb(['flash', 'dtb', FIRMWARE['dtb']])
        fb(['erase', 'kernel'])
        fb(['flash', 'kernel', FIRMWARE['kernel']])
        fb(['erase', 'rootfs'])
        fb(['flash', 'rootfs', FIRMWARE['rootfs']])
        fb(['erase', 'ubifs'])
        fb(['flash', 'ubifs', FIRMWARE['ubifs']])

        fb(['reboot'])

        messagebox.showinfo("Success", f"Flashed {serial} successfully.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Flashing Failed", f"Error flashing {serial}. Check device and logs.")

def center_window(win, width=400, height=400):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def run_gui():
    root = tk.Tk()
    root.title("ChipFlasher")
    center_window(root)

    status_var = tk.StringVar(value="Status: connect a device to update")
    progress = ttk.Progressbar(root, length=300, mode='determinate')
    checked_devices = {}

    # Load checkbox images
    checkbox_on = PhotoImage(file=resource_path("assets/checkbox_on.png"))
    checkbox_off = PhotoImage(file=resource_path("assets/checkbox_off.png"))


    # Treeview with custom style
    style = ttk.Style()
    style = ttk.Style()
    style.configure("Treeview", rowheight=24)

    # Remove left indent by customizing layout
    style.layout("Treeview.Item", [
        ("Treeitem.padding", {
            "sticky": "nswe",
            "children": [
                ("Treeitem.image", {"side": "left", "sticky": ""}),
                ("Treeitem.text", {"side": "left", "sticky": ""})
            ]
        })
    ])

    # Treeview with checkboxes
    device_tree = ttk.Treeview(root, show="tree", selectmode="none", height=10)
    device_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def toggle_check(event):
        item_id = device_tree.identify_row(event.y)
        if not item_id:
            return
        dev_id = device_tree.item(item_id, 'text')
        checked = not checked_devices.get(dev_id, False)
        checked_devices[dev_id] = checked
        device_tree.item(item_id, image=checkbox_on if checked else checkbox_off)

    device_tree.bind("<Button-1>", toggle_check)

    # Status label
    tk.Label(root, textvariable=status_var, anchor='w').pack(fill=tk.X, padx=10)
    progress.pack(pady=5)

    def load_devices():
        device_tree.delete(*device_tree.get_children())
        checked_devices.clear()
        progress['value'] = 0
        devices = get_fastboot_devices()
        if not devices:
            status_var.set("Status: connect a device to update")
        else:
            for dev in devices:
                checked_devices[dev] = False
                device_tree.insert('', 'end', text='   ' + dev, image=checkbox_off)
            status_var.set("Status: select a device to update")

    def flash_device(dev):
        print(f"(Mock) Flashing {dev}")
        # Simulate flashing with print and success
        return True

    def on_flash():
        selected = [d for d, checked in checked_devices.items() if checked]
        if not selected:
            messagebox.showinfo("No Devices", "Please check at least one device.")
            return

        total = len(selected)
        progress['maximum'] = total
        progress['value'] = 0

        for i, dev in enumerate(selected, start=1):
            status_var.set(f"Status: updating firmware on {dev}...")
            root.update_idletasks()
            try:
                flash_device(dev)
                status_var.set(f"Status: successfully updated {dev}")
            except Exception as e:
                status_var.set(f"Status: failed to flash {dev}")
                messagebox.showerror("Flash Failed", str(e))
            progress['value'] = i
            root.update_idletasks()

        status_var.set("Status: update complete")

        #TODO: optional timed progress reset
        # root.after(1000, lambda: progress.config(value=0))

    # Buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="🔁 Refresh Devices", command=load_devices).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="🚀 Flash Firmware", command=lambda: threading.Thread(target=on_flash, daemon=True).start()).pack(side=tk.LEFT, padx=5)

    import threading
    load_devices()
    root.mainloop()

if __name__ == "__main__":
    run_gui()
