
ulong decode_recipe(char *param_1)

{
  bool bVar1;
  int iVar2;
  size_t sVar3;
  char *__dest;
  code *pcVar4;
  undefined7 extraout_var;
  undefined **ppuVar5;
  char local_1f [7];
  
  if (param_1 == (char *)0x0) {
    return 0;
  }
  sVar3 = strlen(param_1);
  builtin_strncpy(local_1f,"DREAM{",7);
  if ((((6 < sVar3) && (iVar2 = strncmp(param_1,local_1f,6), iVar2 == 0)) &&
      (param_1[sVar3 - 1] == '}')) && (__dest = (char *)malloc(sVar3 - 6), __dest != (char *)0x0)) {
    memcpy(__dest,param_1 + 6,sVar3 - 7);
    ppuVar5 = &PTR_FUN_00103dc0;
    __dest[sVar3 - 7] = '\0';
    pcVar4 = FUN_001012c0;
    while (iVar2 = (*pcVar4)(__dest), iVar2 != 0) {
      pcVar4 = (code *)ppuVar5[1];
      ppuVar5 = ppuVar5 + 1;
      if (pcVar4 == (code *)0x0) {
        bVar1 = FUN_00101550(__dest);
        free(__dest);
        return CONCAT71(extraout_var,bVar1) & 0xffffffff;
      }
    }
    free(__dest);
  }
  return 0;
}


bool FUN_001012c0(byte *param_1)

{
  byte bVar1;
  __int32_t **pp_Var2;
  byte *pbVar3;
  int iVar4;
  byte local_2e [14];
  
  bVar1 = *param_1;
  local_2e[0] = 0x70;
  local_2e[1] = 0x33;
  local_2e[2] = 0x61;
  local_2e[3] = 0x72;
  local_2e[4] = 0x73;
  local_2e[5] = 0;
  if (bVar1 == 0) {
    return false;
  }
  pbVar3 = param_1 + 1;
  iVar4 = 0;
  do {
    if (iVar4 != 5) {
      while( true ) {
        pp_Var2 = __ctype_tolower_loc();
        if ((*pp_Var2)[bVar1] == (uint)local_2e[iVar4]) break;
        bVar1 = *pbVar3;
        pbVar3 = pbVar3 + 1;
        if (bVar1 == 0) goto LAB_00101334;
      }
      iVar4 = iVar4 + 1;
    }
    bVar1 = *pbVar3;
    pbVar3 = pbVar3 + 1;
  } while (bVar1 != 0);
LAB_00101334:
  return iVar4 == 5;
}


undefined8 try_decode(void)

{
  char *__ptr;
  ulong uVar1;
  
  FUN_00101430();
  puts(&DAT_00102080);
  puts("The recipe is locked away... can you decode it?");
  __ptr = enter_key();
  uVar1 = decode_recipe(__ptr);
  if ((int)uVar1 == 0) {
    puts(&DAT_001020f0);
    wrong();
  }
  else {
    FUN_00101800(__ptr);
  }
  free(__ptr);
  return 0;
}



char * enter_key(void)

{
  char *__s;
  char *pcVar1;
  size_t sVar2;
  
  __s = (char *)malloc(0x100);
  if (__s == (char *)0x0) {
    fwrite("Memory allocation failed!\n",1,0x1a,stderr);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  printf("Enter the secret recipe key: ");
  fflush(stdout);
  pcVar1 = fgets(__s,0x100,stdin);
  if (pcVar1 == (char *)0x0) {
    free(__s);
    __s = (char *)0x0;
  }
  else {
    sVar2 = strlen(__s);
    if ((sVar2 != 0) && (__s[sVar2 - 1] == '\n')) {
      __s[sVar2 - 1] = '\0';
      return __s;
    }
  }
  return __s;
}

