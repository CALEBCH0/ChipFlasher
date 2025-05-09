# ChipFlasher
ChipFlasher is a Windows tool that automatically updates the firmware on one or more embedded devices connected via USB. 
It uses the fastboot protocol to flash the follwing key firmware components:
Bootloader (BL2, BL31, U-Boot)
Device Tree (DTB)
Kernel (Image)
Root filesystem
Flash environment config
UBIFS image

This tool ensures your device is brought to a known, working firmware state using a reliable, guided process.

# Requirements
Windows 10 or later
USB connection to one or more devices that support fastboot
Devices must be powered on and in fastboot mode
Do not disconnect the device during update

# How to build
Make sure you have pyinstaller. If not, run `pip install pyinstaller`
To build .exe file, click build.bat or locate it and type `./build.bat` in terminal

# How to use
1. Connect your device(s) via USB and ensure they are in fastboot mode.
2. Run ChipFlasher.exe (double-click).
3. A window will open and show connected fastboot devices.
4. Select one or more devices from the list.
5. Click "Flash Firmware".
6. Watch the status updates and progress bar.

Once complete, the device will reboot automatically.

All code written by Caleb Cho. This tool is provided for internal use only. Do not redistribute without permission.
