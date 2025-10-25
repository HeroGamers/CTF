from pwn import *

# XOR Starter
str = "label"

new_str = xor(str.encode(), 13)
print("crypto{" + new_str.decode() + "}")

# XOR Properties

KEY1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
KEY2_xor_KEY1 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
KEY2_xor_KEY3 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
FLAG_xor_KEY1_xor_KEY3_xor_KEY2 = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

KEY1_bytes = bytes.fromhex(KEY1)
KEY2_xor_KEY1_bytes = bytes.fromhex(KEY2_xor_KEY1)
KEY2_xor_KEY3_bytes = bytes.fromhex(KEY2_xor_KEY3)
FLAG_xor_KEY1_xor_KEY3_xor_KEY2_bytes = bytes.fromhex(FLAG_xor_KEY1_xor_KEY3_xor_KEY2)

KEY2_bytes = xor(KEY2_xor_KEY1_bytes, KEY1_bytes)
KEY3_bytes = xor(KEY2_xor_KEY3_bytes, KEY2_bytes)

FLAG_xor_KEY1_xor_KEY3_bytes = xor(FLAG_xor_KEY1_xor_KEY3_xor_KEY2_bytes, KEY2_bytes)
FLAG_xor_KEY1_bytes = xor(FLAG_xor_KEY1_xor_KEY3_bytes, KEY3_bytes)
FLAG_bytes = xor(FLAG_xor_KEY1_bytes, KEY1_bytes)
FLAG = FLAG_bytes.decode()
print(FLAG) # crypto{x0r_i5_ass0c1at1v3}

# Favourite byte

## https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')XOR_Brute_Force(1,100,0,'Standard',false,true,false,'crypto%7B')&input=NzM2MjY5NjA2NDdmNmIyMDY4MjEyMDRmMjEyNTRmN2Q2OTRmNzYyNDY2MjA2NTYyMjEyNzIzNGY3MjY5Mjc3NTZk

## key = 10
## crypto{0x10_15_my_f4v0ur173_by7e}

# You either know, XOR you don't

## 0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104

## https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')XOR(%7B'option':'UTF8','string':'crypto%7B'%7D,'Standard',false)&input=MGUwYjIxM2YyNjA0MWU0ODBiMjYyMTdmMjczNDJlMTc1ZDBlMDcwYTNjNWIxMDNlMjUyNjIxN2YyNzM0MmUxNzVkMGUwNzdlMjYzNDUxMTUwMTA0&oeol=VT

## https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')XOR(%7B'option':'UTF8','string':'myXORkey'%7D,'Standard',false)&input=MGUwYjIxM2YyNjA0MWU0ODBiMjYyMTdmMjczNDJlMTc1ZDBlMDcwYTNjNWIxMDNlMjUyNjIxN2YyNzM0MmUxNzVkMGUwNzdlMjYzNDUxMTUwMTA0&oeol=VT

## myXORkey

## crypto{1f_y0u_Kn0w_En0uGH_y0u_Kn0w_1t_4ll}