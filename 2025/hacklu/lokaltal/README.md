In this challenge, you will need to exploit CVE-2023-21688, a use-after-free vulnerability in the `AlpcpCreateView` function.

### Kernel patch setup
We forward-ported the vulnerability to the most recent release version of Windows 11 25H2 with a binary patch to `ntoskrnl.exe`. The patch is provided together with this README in the challenge attachment:
- A copy of the patched `ntoskrnl.exe` binary. If you want to compare with the unpatched one, you can check the build number in the PE file and download the corresponding build from [Winbindex](https://winbindex.m417z.com/)
- A python script that assembles our patches and writes the patch bytes and addresses onto the console (hex-formatted). There is no fully automated patch procedure, the original binary was patched using IDA.

In addition, you can download the full remote setup [here](https://lokaltal-cdn.flu.xxx/lokaltal-615aa87aba93afc64507bb9cc418f29f.zip). The archive is around 17GB in size and contains the fully configured Win11 25H2 VM with a start script for `qemu-kvm`. Our remote setup works using docker (so there is a dockerfile that starts the VM script); it is recommended to run the command from the dockerfile directly to make interfacing with the VM easier. If you want to build / use your own 11 25H2 VM (not recommended), consider the `vm_setup.md` file, which contains a writeup of the steps that were taken to set up the challenge VM.

As the VM image is somewhat large (~27GB), you should download the `ntoskrnl.exe` binary first and examine it in a reverse engineering tool with PDB support (IDA pro is recommended, others should work), so that you can analyze the bug and think about an exploit before downloading the larger image.

### DSE / PatchGuard disablement
Windows normally has countermeasures in place to prevent modifications to the kernel:
- `PatchGuard` will check integrity of the system at runtime with non-deterministic patterns, and may cause the system to bugcheck if the kernel is modified
- The windows bootloader `winload.efi` verifies the Authenticode signature and refuses the boot if it is wrong

For the challenge, we circumvent both measures using [EfiGuard](https://github.com/Mattiwatti/EfiGuard), a UEFI DXE driver that hooks into the windows boot process. The provided VM is already set up to boot with EfiGuard. When you boot your VM locally with the display attached, you should see a few green log messages during windows bootup. If you encounter any of the following issues, it indicates that EfiGuard is not loaded correctly
- The VM shows a blue recovery message (not a bugcheck) indicating that ntoskrnl.exe is corrupt
- The VM boots into the "automatic repair" mode

In this case, check that the EFIGuard drive is set up as your boot device, in particular if you imported the VM into another hypervisor that is not qemu-kvm. If you cannot resolve your issue, please open a ticket, getting PatchGuard / DSE disabled is not part of the challenge :)

### Challenge environment
When you submit your exploit to the VM, it will be executed in a lesser privileged app container (LPAC) sandbox. The LPAC runner is installed as a service in the challenge VM that you can download, the source code and release binary is provided [on github](https://github.com/SeTcbPrivilege/sandbox-ctf-launcher/releases/tag/hacklu) as well for better debugging.

The flag is passed into the VM as a raw disk, which is only readable by administrators. You can use the following code to read it, assuming you have privileges:
```c
#include <iostream>
#include <Windows.h>

// requires settings c++20 in your project settings
#include <format>
int main()
{
    HANDLE hFile = CreateFile(L"\\\\?\\PhysicalDrive2", GENERIC_READ, 0, nullptr, OPEN_EXISTING, 0, nullptr);

    if (hFile == 0 || hFile == INVALID_HANDLE_VALUE) {
        std::cout << std::format("Could not open file, GLE {:x}", GetLastError());
    }
    char buf[512] = {};
    DWORD bytesRead;
    ReadFile(hFile, buf, sizeof(buf), &bytesRead, nullptr);

	// flag is ASCII
    std::cout << buf;
    
}
```

The read size (and offset) have to be a multiple of 512, otherwise the read will fail. 

### Debugging your exploit
At some point, you will almost definitely want to debug your VM with the WinDbg kernel debugger, which also needs to run under Windows. If you are running windows on your host system, you will most likely want to import your VM into another hypervisor software (I used VMWare, but anything should work in theory). 
- You need to convert the disk images. The main disk is qcow2, while the additional EfiGuard bootdisk is a raw disk image. Use `qemu-img` and/or the tools provided by your hypervisor
- Pay attention to the order of the disks. The setup expects the following. If you change the order, you may need to change your flag read command
	- EfiGuard ESP disk set up as disk 0 and boot device
	- Windows main disk as disk 1
	- Flag disk as disk 2

If you can get your debugger and the debugged VM into the same network, Network kernel debugging (KDNET) is the recommended option. On the debugee VM, issue the following commands
- `bcdedit /debug on`
- `bcdedit /dbgsettings net hostip:<DEBUGGER_IP> port:50000`
- Take note of the resulting debug key. This has to be entered in the debugger. The debugee will connect via UDP to the host VM

You _need_ a DHCP server to assign an IP to the debugee VM. Most hypervisors have an internal one that should hand out reasonably stable leases. There is a `nodhcp` flag in the net debug settings, but you should not use it. Windows will disregard your static IP configuration and just configure an APIPA ip 
