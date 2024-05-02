undefined4 main(void) {
  int checkval;
  char *pcVar1;
  undefined4 uVar2;
  long in_FS_OFFSET;
  char pwd [264];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  __printf_chk(1,"Enter password: ");
  pcVar1 = fgets(pwd,0x100,stdin);
  if (pcVar1 == (char *)0x0) {
    uVar2 = 0xffffffff;
    puts("Error reading from stdin!");
  }
  else {
    sleep(1);
    checkval = check(pwd);
    if (checkval == 0) {
      puts("Permission granted.");
      uVar2 = 0;
    }
    else {
      uVar2 = 0;
      puts("Permission denied.");
    }
  }
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return uVar2;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}


byte check(char *pwd) {
  size_t pwd_len;
  ulong i;
  int pwd_mask_i;
  byte returnval;
  byte *pwd_char;
  
  pwd_len = strlen(pwd);
  if (pwd_len != 0) {
    i = 0;
    returnval = 0;
    do {
      pwd_mask_i = (int)i + (int)((i & 0xffffffff) / 0x1a) * -0x1a;
      pwd_char = (byte *)(pwd + i);
      i = i + 1;
      returnval = returnval | *pwd_char ^ (&pwd_mask)[pwd_mask_i] ^ (&pwd_mask)[0x33 - pwd_mask_i];
    } while (pwd_len != i);
                    /* needs to be equal to 0 */
    return returnval;
  }
  return 0;
}