
void main(undefined4 param_1,undefined4 param_2,uint **param_3)

{
  uint extraout_r1;
  uint extraout_r1_00;
  uint extraout_r1_01;
  uint extraout_r1_02;
  uint extraout_r1_03;
  uint extraout_r1_04;
  uint extraout_r1_05;
  uint extraout_r1_06;
  uint extraout_r1_07;
  uint uVar1;
  uint uVar2;
  uint uVar3;
  undefined *puVar4;
  undefined4 uVar5;
  int iVar6;
  undefined4 uVar7;
  undefined4 *puVar8;
  int iVar9;
  byte *pbVar10;
  byte *pbVar11;
  undefined8 uVar12;
  ulonglong uVar13;
  uint local_2c0;
  uint local_2bc;
  int local_27c;
  uint local_228;
  uint local_224;
  uint *login_success_str;
  uint *now_access_fuln_func_str;
  uint *chall_done_str;
  uint *local_pico_str;
  uint local_188;
  ushort local_184;
  byte local_168 [319];
  undefined1 uStack_29;
  
  FUN_10004a54();
  FUN_100016b4(2000);
  FUN_1000197c(0x40034000,0x1c200);
  FUN_10000aac(0,2);
  FUN_10000aac(1,2);
  FUN_10000334();
  login_success_str = (uint *)0x1000816c;
  now_access_fuln_func_str = (uint *)0x10008188;
  chall_done_str = (uint *)0x10008250;
  local_pico_str = (uint *)0x10008278;
LAB_100004c6:
  uVar3 = 0x696d6461;
LAB_100004cc:
  FUN_100016b4(2000);
  read_message_print(&DAT_10008104,extraout_r1,param_3,uVar3);
  print_message((uint *)"Welcome to the i have fun challenge");
  print_message((uint *)"Please enter your credentials:\n");
  puVar4 = &DAT_20001498;
  iVar9 = 0;
  FUN_100075fc(&DAT_20001bc4);
  read_message_print((byte *)"Username: ",extraout_r1_00,param_3,puVar4);
  puVar4 = &DAT_20001498;
  FUN_100075fc(&DAT_20001bc4);
LAB_10000500:
  uVar3 = FUN_10004a5c();
  uVar1 = extraout_r1_01;
  do {
    if ((uVar3 == 10) || (uVar3 == 0xd)) {
LAB_10000548:
      uVar5 = 0;
      *(undefined1 *)((int)&local_188 + iVar9) = 0;
      FUN_10004adc(10);
      read_message_print((byte *)"Password: ",extraout_r1_02,param_3,uVar5);
      puVar4 = &DAT_20001498;
      iVar9 = 0;
      FUN_100075fc(&DAT_20001bc4);
      break;
    }
    if ((uVar3 != 8) && (uVar3 != 0x7f)) {
      puVar4 = (undefined *)(uVar3 - 0x20);
      if (puVar4 < (undefined *)0x5f) {
        param_3 = &login_success_str;
        *(char *)((int)&local_188 + iVar9) = (char)uVar3;
        FUN_10004adc(uVar3);
        puVar4 = &DAT_20001498;
        iVar9 = iVar9 + 1;
        FUN_100075fc(&DAT_20001bc4);
        if (iVar9 == 0x1f) {
          iVar9 = 0x1f;
          goto LAB_10000548;
        }
      }
      goto LAB_10000500;
    }
    if (iVar9 < 1) goto LAB_10000500;
    read_message_print(&DAT_10008028,uVar1,param_3,puVar4);
    puVar4 = &DAT_20001498;
    iVar9 = iVar9 + -1;
    FUN_100075fc(&DAT_20001bc4);
    uVar3 = FUN_10004a5c();
    uVar1 = extraout_r1_05;
  } while( true );
LAB_10000572:
  uVar3 = FUN_10004a5c();
  uVar1 = extraout_r1_03;
  do {
    if ((uVar3 == 10) || (uVar3 == 0xd)) {
LAB_100005b6:
      local_168[iVar9] = 0;
      FUN_10004adc(10);
      uVar3 = local_188;
      if ((local_188 == 0x696d6461) && (uVar3 = (uint)local_184, uVar3 == 0x6e)) {
        local_2c0 = (uint)local_168[0];
        if (local_2c0 == 0) {
          param_3 = (uint **)0x0;
          uVar3 = 0;
          read_message_print((byte *)
                             "Debug: password=\'%s\' -> number=%llu -> encrypted=%llu (expected=%llu )\n"
                             ,(uint)local_168,0,0);
        }
        else {
          uVar3 = (uint)local_168[1];
          local_2bc = 0;
          if (uVar3 != 0) {
            uVar1 = local_2c0 * 0x100;
            local_2c0 = uVar1 + uVar3;
            local_2bc = (uint)CARRY4(uVar1,uVar3);
            uVar3 = (uint)local_168[2];
            if (uVar3 != 0) {
              uVar1 = local_2c0 * 0x100;
              local_2c0 = uVar3 + uVar1;
              local_2bc = local_2bc * 0x100 + (uint)CARRY4(uVar3,uVar1);
              uVar3 = (uint)local_168[3];
              if (uVar3 != 0) {
                uVar1 = local_2c0 >> 0x18;
                uVar2 = local_2c0 * 0x100;
                local_2c0 = uVar3 + uVar2;
                local_2bc = (local_2bc * 0x100 | uVar1) + (uint)CARRY4(uVar3,uVar2);
                uVar3 = (uint)local_168[4];
                if (uVar3 != 0) {
                  uVar1 = local_2c0 >> 0x18;
                  uVar2 = local_2c0 * 0x100;
                  local_2c0 = uVar3 + uVar2;
                  local_2bc = (local_2bc * 0x100 | uVar1) + (uint)CARRY4(uVar3,uVar2);
                  uVar3 = (uint)local_168[5];
                  if (uVar3 != 0) {
                    uVar1 = local_2c0 >> 0x18;
                    uVar2 = local_2c0 * 0x100;
                    local_2c0 = uVar3 + uVar2;
                    local_2bc = (local_2bc * 0x100 | uVar1) + (uint)CARRY4(uVar3,uVar2);
                    uVar3 = (uint)local_168[6];
                    if (uVar3 != 0) {
                      uVar1 = local_2c0 >> 0x18;
                      uVar2 = local_2c0 * 0x100;
                      local_2c0 = uVar3 + uVar2;
                      local_2bc = (local_2bc * 0x100 | uVar1) + (uint)CARRY4(uVar3,uVar2);
                      uVar3 = (uint)local_168[7];
                      if (uVar3 != 0) {
                        uVar1 = local_2c0 >> 0x18;
                        uVar2 = local_2c0 * 0x100;
                        local_2c0 = uVar3 + uVar2;
                        local_2bc = (local_2bc * 0x100 | uVar1) + (uint)CARRY4(uVar3,uVar2);
                      }
                    }
                  }
                }
              }
            }
          }
          uVar3 = 0;
          param_3 = (uint **)0x3e8;
          FUN_10002110(local_2c0,local_2bc,1000,0);
          iVar9 = 0;
          uVar1 = 0x143;
          FUN_10002110((uint)param_3,uVar3,0x143,0);
          uVar12 = FUN_10002cdc(uVar1,iVar9,uVar1,iVar9);
          iVar6 = 0;
          uVar2 = 0x143;
          FUN_10002110((uint)uVar12,(uint)((ulonglong)uVar12 >> 0x20),0x143,0);
          uVar12 = FUN_10002cdc(uVar2,iVar6,uVar2,iVar6);
          iVar6 = 0;
          uVar2 = 0x143;
          FUN_10002110((uint)uVar12,(uint)((ulonglong)uVar12 >> 0x20),0x143,0);
          uVar12 = FUN_10002cdc(uVar2,iVar6,uVar1,iVar9);
          iVar6 = 0;
          iVar9 = 0x143;
          FUN_10002110((uint)uVar12,(uint)((ulonglong)uVar12 >> 0x20),0x143,0);
          read_message_print((byte *)
                             "Debug: password=\'%s\' -> number=%llu -> encrypted=%llu (expected=%llu )\n"
                             ,(uint)local_168,param_3,uVar3);
          if ((iVar9 == 0x7b) && (iVar6 == 0)) {
            print_message(login_success_str);
            print_message(now_access_fuln_func_str);
            read_message_print((byte *)"RSA parameters visible: n=%llu, e=%llu\n",extraout_r1_06,
                               0x143,0);
            local_228 = (uint)local_168[0];
            if (local_228 == 0) {
              local_228 = 0;
              local_224 = 0;
            }
            else {
              uVar3 = (uint)local_168[1];
              if (uVar3 == 0) {
                local_224 = 0;
              }
              else {
                uVar1 = local_228 * 0x100;
                local_228 = uVar1 + uVar3;
                local_224 = (uint)CARRY4(uVar1,uVar3);
                uVar3 = (uint)local_168[2];
                if (uVar3 != 0) {
                  uVar1 = local_228 * 0x100;
                  local_228 = uVar3 + uVar1;
                  local_224 = local_224 * 0x100 + (uint)CARRY4(uVar3,uVar1);
                  uVar3 = (uint)local_168[3];
                  if (uVar3 != 0) {
                    uVar1 = local_228 >> 0x18;
                    uVar2 = local_228 * 0x100;
                    local_228 = uVar3 + uVar2;
                    local_224 = (local_224 * 0x100 | uVar1) + (uint)CARRY4(uVar3,uVar2);
                    uVar3 = (uint)local_168[4];
                    if (uVar3 != 0) {
                      uVar1 = local_228 >> 0x18;
                      uVar2 = local_228 * 0x100;
                      local_228 = uVar3 + uVar2;
                      local_224 = (local_224 * 0x100 | uVar1) + (uint)CARRY4(uVar3,uVar2);
                      uVar3 = (uint)local_168[5];
                      if (uVar3 != 0) {
                        uVar1 = local_228 >> 0x18;
                        uVar2 = local_228 * 0x100;
                        local_228 = uVar3 + uVar2;
                        local_224 = (local_224 * 0x100 | uVar1) + (uint)CARRY4(uVar3,uVar2);
                        uVar3 = (uint)local_168[6];
                        if (uVar3 != 0) {
                          uVar1 = local_228 >> 0x18;
                          uVar2 = local_228 * 0x100;
                          local_228 = uVar3 + uVar2;
                          local_224 = (local_224 * 0x100 | uVar1) + (uint)CARRY4(uVar3,uVar2);
                          uVar3 = (uint)local_168[7];
                          if (uVar3 != 0) {
                            uVar1 = local_228 >> 0x18;
                            uVar2 = local_228 * 0x100;
                            local_228 = uVar3 + uVar2;
                            local_224 = (local_224 * 0x100 | uVar1) + (uint)CARRY4(uVar3,uVar2);
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
            uVar2 = 0;
            uVar3 = 1000;
            FUN_10002110(local_228,local_224,1000,0);
            uVar1 = 0x143;
            iVar9 = 0;
            FUN_10002110(uVar3,uVar2,0x143,0);
            uVar12 = FUN_10002cdc(uVar1,iVar9,uVar1,iVar9);
            iVar6 = 0;
            uVar3 = 0x143;
            FUN_10002110((uint)uVar12,(uint)((ulonglong)uVar12 >> 0x20),0x143,0);
            uVar12 = FUN_10002cdc(uVar3,iVar6,uVar3,iVar6);
            iVar6 = 0;
            uVar3 = 0x143;
            FUN_10002110((uint)uVar12,(uint)((ulonglong)uVar12 >> 0x20),0x143,0);
            uVar12 = FUN_10002cdc(uVar3,iVar6,uVar1,iVar9);
            uVar7 = 0;
            uVar5 = 0x143;
            uVar13 = FUN_10002110((uint)uVar12,(uint)((ulonglong)uVar12 >> 0x20),0x143,0);
            read_message_print((byte *)"Your encrypted input was: %llu\n",(uint)(uVar13 >> 0x20),
                               uVar5,uVar7);
            read_message_print((byte *)"Enter input for processing: ",extraout_r1_07,uVar5,uVar7);
            local_27c = 0;
            FUN_100075fc(&DAT_20001bc4);
            pbVar11 = local_168 + 0x40;
            pbVar10 = pbVar11;
            break;
          }
        }
      }
      print_message((uint *)"\n*** Invalid credentials. Try again. ***");
      goto LAB_100004cc;
    }
    if ((uVar3 != 8) && (uVar3 != 0x7f)) {
      puVar4 = (undefined *)(uVar3 - 0x20);
      if (puVar4 < (undefined *)0x5f) {
        param_3 = &login_success_str;
        local_168[iVar9] = (byte)uVar3;
        FUN_10004adc(uVar3);
        puVar4 = &DAT_20001498;
        iVar9 = iVar9 + 1;
        FUN_100075fc(&DAT_20001bc4);
        if (iVar9 == 0x3f) {
          iVar9 = 0x3f;
          goto LAB_100005b6;
        }
      }
      goto LAB_10000572;
    }
    if (iVar9 < 1) goto LAB_10000572;
    read_message_print(&DAT_10008028,uVar1,param_3,puVar4);
    puVar4 = &DAT_20001498;
    iVar9 = iVar9 + -1;
    FUN_100075fc(&DAT_20001bc4);
    uVar3 = FUN_10004a5c();
    uVar1 = extraout_r1_04;
  } while( true );
  while( true ) {
    local_27c = local_27c + 1;
    *pbVar10 = (byte)uVar3;
    pbVar10 = pbVar10 + 1;
    if (local_27c == 0xff) break;
    uVar3 = FUN_10004a5c();
    if ((uVar3 + 1 < 0xf) && ((0x4801U >> (uVar3 + 1 & 0xff) & 1) != 0)) {
      local_168[local_27c + 0x40] = 0;
      if (local_27c != 0) goto LAB_10000a0a;
      goto LAB_10000a42;
    }
  }
  uStack_29 = 0;
LAB_10000a0a:
  uVar5 = 0x10;
  puVar8 = &DAT_20001494;
  do {
    read_message_print((byte *)"%02x ",(uint)*pbVar11,uVar5,puVar8);
    if (pbVar11 == local_168 + local_27c + 0x3f) break;
    pbVar11 = pbVar11 + 1;
  } while (local_168 + 0x50 != pbVar11);
LAB_10000a42:
  FUN_10004adc(10);
  get_flag(local_168 + 0x40,local_27c);
  if (RET_STATUS != 0) {
    print_message(chall_done_str);
    print_message(local_pico_str);
  }
  param_3 = (uint **)0x0;
  RET_STATUS = 0;
  FUN_100016b4(100);
  goto LAB_100004c6;
}


void get_flag(byte *param_1,int param_2)

{
  uint uVar1;
  uint uVar2;
  uint extraout_r1;
  int iVar3;
  undefined4 uVar4;
  undefined4 *puVar5;
  byte *pbVar6;
  byte *pbVar7;
  undefined1 auStack_3c [32];
  uint local_1c;
  
  uVar4 = 0xdeadbeef;
  local_1c = 0xdeadbeef;
  iVar3 = param_2;
  thunk_EXT_FUN_0000434c(auStack_3c,param_1);
  uVar1 = local_1c;
  read_message_print((byte *)"Processing input: ",extraout_r1,iVar3,uVar4);
  if (0 < param_2) {
    pbVar7 = param_1 + 0x20;
    pbVar6 = param_1 + param_2 + -1;
    do {
      uVar2 = (uint)*param_1;
      if (0x5e < uVar2 - 0x20) {
        uVar2 = 0x2e;
      }
      FUN_10004adc(uVar2);
    } while ((param_1 != pbVar6) && (param_1 = param_1 + 1, param_1 != pbVar7));
  }
  FUN_10004adc(10);
  uVar4 = 0xdeadbeef;
  if (uVar1 == 0xdeadbeef) {
    print_message((uint *)"Buffer processed safely.");
  }
  else {
    print_message((uint *)"*** STACK SMASHING DETECTED! ***");
    read_message_print((byte *)"Canary was overwritten: 0x%08x\n",uVar1,iVar3,uVar4);
    if (uVar1 == 0xcafebabe) {
      uVar4 = 1;
      puVar5 = &RET_STATUS;
      RET_STATUS = 1;
      print_message((uint *)"*** EXPLOIT SUCCESSFUL! ***");
      print_message((uint *)"Flag found!");
      read_message_print((byte *)"Flag: %s\n",0x20000f98,uVar4,puVar5);
    }
    else {
      print_message((uint *)"Try again with the correct canary value!");
    }
  }
  return;
}

