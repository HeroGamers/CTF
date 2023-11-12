# Challenge 13 Attendance

WEB attendance: flag{g00d_5tud3nt_att3nd_cl455}
breakpoints go brrrr

# Homework 3-B

.htaccess add-type PHP to .hth files
flag{wHy_U_w0nt_5t0p_upl04d1n9_phP_f1l3s?}


# Homework 3-A
Ghidra Reverse


f = b'\x01\x01\x02\x03\x05\x08\x0d\x15\x22\x37\x59\x90\xe9\x79\x62\xdb\x3d\x18\x55\x6d\xc2\x2f\xf1\x20\x11\x31\x42\x73\xb5\x00\x00\x00\x55\x38\x5b\x31\xb1\x8e\xb3\xed\x8b\x1d\xaf\x50\x6e\xb6\x25\x6a\xf6\x79\xec\x4e\x6f\x1b\x2a\x6e\xe4\x74\x08\xbf\x8d'
data = b'\x55\x38\x5b\x31\xb1\x8e\xb3\xed\x8b\x1d\xaf\x50\x6e\xb6\x25\x6a\xf6\x79\xec\x4e\x6f\x1b\x2a\x6e\xe4\x74\x08\xbf\x8d'

undefined8 main(void)

{
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  
  for (local_c = 2; local_c < 0x1d; local_c = local_c + 1) {
    (&f)[local_c] = (&f)[local_c + -1] + (&f)[local_c + -2];
  }
  for (local_10 = 0; local_10 < 0x1d; local_10 = local_10 + 1) {
    __isoc99_scanf("%c",s + local_10);
    s[local_10] = s[local_10] + (&f)[local_10];
  }
  local_14 = 0;
  for (local_18 = 0; local_18 < 0x1d; local_18 = local_18 + 1) {
    s[local_18] = s[local_18] ^ s[(local_18 + 0x1c) % 0x1d];
    if (s[local_18] == data[local_18]) {
      local_14 = local_14 + 1;
    }
  }
  if (local_14 == 0x1d) {
    puts(":D");
  }
  else {
    puts(":(");
  }
  return 0;
}