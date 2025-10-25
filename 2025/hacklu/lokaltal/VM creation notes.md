## VM setup steps
Since the VM was set up manually, it is recommended to use the provided VM image to avoid any deviations in the setup.
If you want to set up your own VM, or just understand the components of the given setup, these are the steps that were taken to set up the VM in order

1. During windows setup, the "vm_run_manual.sh" script is used, which provides virtual CDROM drives containing the Windows 11 25H2 installer ISO and the VirtIO drivers
   which were obtained from the [lastest nightly release](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/latest-virtio/virtio-win.iso), at the time the release was `virtio-win-0.1.285.iso`
2. Immediately upon reaching the windows setup environment (the screen asking you for your language and locale), the following registry values are added under `HKEY_LOCAL_MACHINE\SYSTEM\Setup\LabConfig` to bypass the Win11 system requirements,
   i.e. minimal CPU / RAM / Disk requirements and TPM. The challenge application still runs reliably with the given resources
   - `BypassSecureBootCheck`
   - `BypassTpmCheck`
   - `BypassRAMCheck`
   - `BypassCpuCheck`
   - `BypassDiskCheck`
   - `BypassStorageCheck`

   To add the entries, press `Shift+F10` to open a `cmd.exe` window and enter the `regedit` command to open the registry editor
3. The Windows 10 Pro SKU is selected during setup, this should not make a major difference
4. In the disk selection screen, no disk will be available by default with the provided qemu launch arguments (as a virtio disk is chosen as the boot device)
   press the "Search for driver" link at the bottom, then browse to `D:\viostor\win11\amd64` to install the Virtio controller driver. The VirtIO disk should become visible.
   
5. Once you get into the OOBE screen (the prompt "Is this the right country or region"), we skip the OOBE by enabling the administrator account. To do so,
   open `cmd.exe` again by pressing `SHIFT+F10` and run
   `net user administrator password`: Set the password `password` for the administrator user. (Note: the password for the challenge VM admin is set to a secure one later)
   `net user administrator /active:yes`: Allow the administrator to log on to the system
   In addition, we remove some registry keys to prevent the OOBE from starting
   - Under `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\OOBE`, remove `DefaultAccountAction`,`DefaultAccountSAMName`,`DefaultAccountSID`,`LaunchUserOOBE`
   - Under `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon`, remove `AutoAdminLogon`, `AutoLogonSID`,`DefaultDomainName`,`DefaultUserName`
   - Type `shutdown /l` to log out of the OOBE 

   You will see the default logon screen. Log in as the administrator using the just set password. Windows will set up the user profile (showing the "We are getting things ready for you") and then show a final prompt regarding advertisement / data collection
   preferences (which you can all deny), the OOBE should close after that and drop you to the Win11 desktop. The OOBE user `defaultuser0` is not needed anymore and can be deleted,
   e.g. by opening the Computer Management MMC console `compmgmt.msc` and deleting the user from the "System Tools -> Local Users and Groups" menu
   
6. [Optional, if you want spice display] We install all of the VirtIO guest tools by running the executable installer `virtio-win-gt-x64` from the provided disk.

7. Install [defendnot](https://dnot.sh) from the github repository to disable the Windows defender

8. Install [EfiGuard] as loader. I added a separate EFI partition as a raw block device to the VM and set it as first boot index. You should see the EfiGuard patch messages in green during the windows boot process
   installing it as a driver works as well (using the "boot maintenance menu" in the UEFI graphical setup, we can add drivers from EFI-accessible filesystems), but there seems to be a bug where custom DXE drivers
   are not loaded after config changes (e.g. if the display device is changed), even though they are still listed on the menu. Therefore, if you make changes, you lose EfiGuard and will get a recovery "blue screen"
   message indicating that ntoskrnl.exe is corrupted on boot.

9. Install all available windows updates to ensure that we have the latest windows kernel. During the CTF, the VM will not be setup with internet access, so there will be no unexpected updates

10. Download the [latest MSVC Redistributable (2015-2022)](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist). This is required for the exploit sandbox launcher, and most likely also by your exploit.
    Note: I installed the release version only - if you get an error for some MSVC DLL files missing, your program might be compiled in debug mode and tries to load the debug DLLs (suffixed with "d") - compile in release mode.

11. Run `compact.exe /compactos:never` to uncompress OS binaries. This will be needed to mount the OS disk with the linux NTFS driver to replace the NT OS kernel.

12. Turn off fast startup: Enter `control` in the Win+r run menu to bring up the old control panel, go to "Hardware and sound" then to the "Choose what the power button does" link in the power options category. Click the link with the shield icon to unlock all options, then uncheck the fast startup checkbox
    If fast startup is enabled, windows will hibernate, leaving the filesystem in an unclean state that is not safe for external mounting.

13. Shut down the virtual machine properly, then use `guestmount` to mount the main partition to an empty folder. For me, the command is `guestmount -a disk.qcow2 -m /dev/sda3 --rw vm_mount`, but your partition number may be different depending on your setup.
    Note that `/dev/sdaX` will not refer to a real linux device, it is just a pseudo-identifier for the guestmounted disk. Also, at least my version of libguestfs did not explicitly warn me that the filesystem was unclean, but silently mounted the disk as read-only instead.
    If you have troubles with `libguestfs`, `qemu-nbd` is another option that exposes the qcow image as a virtual block device to your kernel, so you can use the default implementation of ntfs-3g.
    
14. Patch the NT OS kernel
    - run the provided script to assemble the patches. The addresses that have to be patched will be printed along with the hex patches. You can use IDA to apply the patches to the NT OS kernel file
    - Use a tool to correct the checksum of the NT OS kernel image. Otherwise, the VM will boot into automatic repair
    - Replace the kernel on the mounted disk, unmount and boot into windows again

15. Completely disable the windows firewall by going into the "Windows defender firewall with advanced security" MMC console. Then, click on the "Windows defender firewall property" link (you have to be in the root view).
    In the property popup, set "firewall state" to "Off" in all three profile tabs (Domain, Private, Public)
    
16. Install the [SandboxCtfLauncher](https://github.com/SeTcbPrivilege/sandbox-ctf-launcher) using [srvany-ng](https://github.com/birkett/srvany-ng)
    - Download the latest executable build of the SandboxCtfLauncher. Place both `SandboxCtfLauncher.exe` and `srvany-ng.exe` under `C:` (other directories will also be fine if you adjust paths)
    - create the service as `sc create "SandboxCtfLauncher" start= auto binPath= "C:\srvany-ng.exe"`
    - Create the following values under the `HKLM\SYSTEM\CurrentControlSet\Services\SandboxCtfLauncher\Parameters`
      - `Application`: `C:\SandboxCtfLauncher.exe`
      - `RestartOnExit`: 1 (DWORD)
      
17. [Optional], disable prefetcher by setting `EnablePrefetcher` to 0 in `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters`.
    Also, delete everything from `C:\Windows\Prefetch`. this is just so that I don't accidentally leave my exploit on the VM
    
18. [Optional] Use the Omnissa (previously VMWare) OS optimization tool

