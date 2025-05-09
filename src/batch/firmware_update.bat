@echo off
set fastboot=%~dp0fastboot.exe
set bl2=%~dp0SDK1.2.0\signed_4k_bl2_1520_0.bin
set bl31=%~dp0SDK1.2.0\signed_bl31.bin
set bl33=%~dp0SDK1.2.0\signed_u-boot_spinand0_boot.bin
%fastboot% --page-size 512 boot %bl2%
timeout /t 1 /nobreak >nul
%fastboot% --page-size 512 boot %bl31%
timeout /t 1 /nobreak >nul
%fastboot% --page-size 512 boot %bl33%
timeout /t 4 /nobreak >nul
%fastboot% --page-size 512 boot %~dp0script.img
%fastboot% erase blx
%fastboot% flash blx %~dp0SDK1.2.0\signed_4k_blx_1520_0.bin
%fastboot% erase env
%fastboot% flash env %~dp0SDK1.2.0\uboot-evm_spinand_boot_uart0.env
%fastboot% erase u-boot
%fastboot% flash u-boot %~dp0SDK1.2.0\signed_u-boot_spinand0_boot.bin
%fastboot% erase dtb
%fastboot% flash dtb %~dp0SDK1.2.0\leipzig-evm-multi-sensor.dtb
%fastboot% erase kernel
%fastboot% flash kernel %~dp0SDK1.2.0\Image
%fastboot% erase rootfs
%fastboot% flash rootfs %~dp0SDK1.2.0\rootfs.squashfs
%fastboot% erase ubifs
%fastboot% flash ubifs %~dp0SDK1.2.0\sdk1.2.0-imx678-os08a10.ubifs
%fastboot% reboot
