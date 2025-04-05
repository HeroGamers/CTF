
//  Microsoft (R) .NET Framework IL Disassembler.  Version 4.7.2558.0
//  Copyright (c) Microsoft Corporation.  All rights reserved.



// Metadata version: v4.0.30319
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 )                         // .z\V.4..
  .ver 4:0:0:0
}
.assembly extern System.Windows.Forms
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 )                         // .z\V.4..
  .ver 4:0:0:0
}
.assembly extern System
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 )                         // .z\V.4..
  .ver 4:0:0:0
}
.assembly extern System.Drawing
{
  .publickeytoken = (B0 3F 5F 7F 11 D5 0A 3A )                         // .?_....:
  .ver 4:0:0:0
}
.assembly StuckAt99
{
  .custom instance void [mscorlib]System.Runtime.CompilerServices.CompilationRelaxationsAttribute::.ctor(int32) = ( 01 00 08 00 00 00 00 00 ) 
  .custom instance void [mscorlib]System.Runtime.CompilerServices.RuntimeCompatibilityAttribute::.ctor() = ( 01 00 01 00 54 02 16 57 72 61 70 4E 6F 6E 45 78   // ....T..WrapNonEx
                                                                                                             63 65 70 74 69 6F 6E 54 68 72 6F 77 73 01 )       // ceptionThrows.

  // --- The following custom attribute is added automatically, do not uncomment -------
  //  .custom instance void [mscorlib]System.Diagnostics.DebuggableAttribute::.ctor(valuetype [mscorlib]System.Diagnostics.DebuggableAttribute/DebuggingModes) = ( 01 00 07 01 00 00 00 00 ) 

  .custom instance void [mscorlib]System.Reflection.AssemblyTitleAttribute::.ctor(string) = ( 01 00 09 53 74 75 63 6B 41 74 39 39 00 00 )       // ...StuckAt99..
  .custom instance void [mscorlib]System.Reflection.AssemblyDescriptionAttribute::.ctor(string) = ( 01 00 00 00 00 ) 
  .custom instance void [mscorlib]System.Reflection.AssemblyConfigurationAttribute::.ctor(string) = ( 01 00 00 00 00 ) 
  .custom instance void [mscorlib]System.Reflection.AssemblyCompanyAttribute::.ctor(string) = ( 01 00 00 00 00 ) 
  .custom instance void [mscorlib]System.Reflection.AssemblyProductAttribute::.ctor(string) = ( 01 00 09 53 74 75 63 6B 41 74 39 39 00 00 )       // ...StuckAt99..
  .custom instance void [mscorlib]System.Reflection.AssemblyCopyrightAttribute::.ctor(string) = ( 01 00 12 43 6F 70 79 72 69 67 68 74 20 C2 A9 20   // ...Copyright .. 
                                                                                                  20 32 30 32 34 00 00 )                            //  2024..
  .custom instance void [mscorlib]System.Reflection.AssemblyTrademarkAttribute::.ctor(string) = ( 01 00 00 00 00 ) 
  .custom instance void [mscorlib]System.Runtime.InteropServices.ComVisibleAttribute::.ctor(bool) = ( 01 00 00 00 00 ) 
  .custom instance void [mscorlib]System.Runtime.InteropServices.GuidAttribute::.ctor(string) = ( 01 00 24 61 62 35 66 38 38 38 32 2D 34 38 35 64   // ..$ab5f8882-485d
                                                                                                  2D 34 32 62 34 2D 62 32 62 66 2D 34 31 39 61 66   // -42b4-b2bf-419af
                                                                                                  32 32 35 30 34 35 30 00 00 )                      // 2250450..
  .custom instance void [mscorlib]System.Reflection.AssemblyFileVersionAttribute::.ctor(string) = ( 01 00 07 31 2E 30 2E 30 2E 30 00 00 )             // ...1.0.0.0..
  .custom instance void [mscorlib]System.Runtime.Versioning.TargetFrameworkAttribute::.ctor(string) = ( 01 00 1C 2E 4E 45 54 46 72 61 6D 65 77 6F 72 6B   // ....NETFramework
                                                                                                        2C 56 65 72 73 69 6F 6E 3D 76 34 2E 37 2E 32 01   // ,Version=v4.7.2.
                                                                                                        00 54 0E 14 46 72 61 6D 65 77 6F 72 6B 44 69 73   // .T..FrameworkDis
                                                                                                        70 6C 61 79 4E 61 6D 65 14 2E 4E 45 54 20 46 72   // playName..NET Fr
                                                                                                        61 6D 65 77 6F 72 6B 20 34 2E 37 2E 32 )          // amework 4.7.2
  .hash algorithm 0x00008004
  .ver 1:0:0:0
}
.mresource public StuckAt99.Form1.resources
{
  // Offset: 0x00000000 Length: 0x000012F4
  // WARNING: managed resource file StuckAt99.Form1.resources created
}
.mresource public StuckAt99.Properties.Resources.resources
{
  // Offset: 0x000012F8 Length: 0x0003D9C7
  // WARNING: managed resource file StuckAt99.Properties.Resources.resources created
}
.module StuckAt99.exe
// MVID: {861861EF-9788-4951-AD8F-38C1DE1B7373}
.imagebase 0x00400000
.file alignment 0x00000200
.stackreserve 0x00100000
.subsystem 0x0002       // WINDOWS_GUI
.corflags 0x00020003    //  ILONLY 32BITPREFERRED
// Image base: 0x0A240000


// =============== CLASS MEMBERS DECLARATION ===================

.class public auto ansi beforefieldinit StuckAt99.Form1
       extends [System.Windows.Forms]System.Windows.Forms.Form
{
  .field private int32 progressValue
  .field private bool flagShown
  .field private class [System]System.ComponentModel.IContainer components
  .field private class [System.Windows.Forms]System.Windows.Forms.Button button1
  .field private class [System.Windows.Forms]System.Windows.Forms.ProgressBar progressBar1
  .method public hidebysig specialname rtspecialname 
          instance void  .ctor() cil managed
  {
    // Code size       37 (0x25)
    .maxstack  8
    IL_0000:  ldarg.0
    IL_0001:  ldc.i4.0
    IL_0002:  stfld      int32 StuckAt99.Form1::progressValue
    IL_0007:  ldarg.0
    IL_0008:  ldc.i4.0
    IL_0009:  stfld      bool StuckAt99.Form1::flagShown
    IL_000e:  ldarg.0
    IL_000f:  ldnull
    IL_0010:  stfld      class [System]System.ComponentModel.IContainer StuckAt99.Form1::components
    IL_0015:  ldarg.0
    IL_0016:  call       instance void [System.Windows.Forms]System.Windows.Forms.Form::.ctor()
    IL_001b:  nop
    IL_001c:  nop
    IL_001d:  ldarg.0
    IL_001e:  call       instance void StuckAt99.Form1::InitializeComponent()
    IL_0023:  nop
    IL_0024:  ret
  } // end of method Form1::.ctor

  .method private hidebysig instance void 
          button1_Click(object sender,
                        class [mscorlib]System.EventArgs e) cil managed
  {
    // Code size       121 (0x79)
    .maxstack  4
    .locals init (bool V_0,
             bool V_1)
    IL_0000:  nop
    IL_0001:  ldarg.0
    IL_0002:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_0007:  ldc.i4.0
    IL_0008:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_Enabled(bool)
    IL_000d:  nop
    IL_000e:  br.s       IL_006a

    IL_0010:  nop
    IL_0011:  ldc.i4.s   1
    IL_0013:  call       void [mscorlib]System.Threading.Thread::Sleep(int32)
    IL_0018:  nop
    IL_0019:  ldarg.0
    IL_001a:  ldarg.0
    IL_001b:  ldfld      int32 StuckAt99.Form1::progressValue
    IL_0020:  ldc.i4.5
    IL_0021:  add
    IL_0022:  stfld      int32 StuckAt99.Form1::progressValue
    IL_0027:  ldarg.0
    IL_0028:  ldfld      class [System.Windows.Forms]System.Windows.Forms.ProgressBar StuckAt99.Form1::progressBar1
    IL_002d:  ldarg.0
    IL_002e:  ldfld      int32 StuckAt99.Form1::progressValue
    IL_0033:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.ProgressBar::set_Value(int32)
    IL_0038:  nop
    IL_0039:  ldarg.0
    IL_003a:  ldfld      int32 StuckAt99.Form1::progressValue
    IL_003f:  ldc.i4.s   99
    IL_0041:  blt.s      IL_004e

    IL_0043:  ldarg.0
    IL_0044:  ldfld      bool StuckAt99.Form1::flagShown
    IL_0049:  ldc.i4.0
    IL_004a:  ceq
    IL_004c:  br.s       IL_004f

    IL_004e:  ldc.i4.0
    IL_004f:  stloc.0
    IL_0050:  ldloc.0
    IL_0051:  brfalse.s  IL_0069

    IL_0053:  nop
    IL_0054:  nop
    IL_0059:  ldarg.0
    IL_005e:  call       instance void StuckAt99.Form1::ShowFlag()
    IL_005f:  nop
    IL_0061:  nop
    IL_0066:  nop
    IL_0067:  nop

    IL_0069:  nop
    IL_006a:  ldarg.0
    IL_006b:  ldfld      int32 StuckAt99.Form1::progressValue
    IL_0070:  ldc.i4.s   100
    IL_0072:  clt
    IL_0074:  stloc.1
    IL_0075:  ldloc.1
    IL_0076:  brtrue.s   IL_0010

    IL_0078:  ret
  } // end of method Form1::button1_Click

  .method public hidebysig instance void 
          ShowFlag() cil managed
  {
    // Code size       63 (0x3f)
    .maxstack  4
    .locals init (bool V_0,
             string V_1)
    IL_0000:  nop
    IL_0001:  ldarg.0
    IL_0002:  ldfld      bool StuckAt99.Form1::flagShown
    IL_0007:  ldc.i4.0
    IL_0008:  ceq
    IL_000a:  stloc.0
    IL_000b:  ldloc.0
    IL_000c:  brfalse.s  IL_003e

    IL_000e:  nop
    IL_000f:  ldarg.0
    IL_0010:  call       instance string StuckAt99.Form1::GenerateFlag()
    IL_0015:  stloc.1
    IL_0016:  ldarg.0
    IL_0017:  ldc.i4.1
    IL_0018:  stfld      bool StuckAt99.Form1::flagShown
    IL_001d:  ldstr      "The flag has been copied into your clipboard\n"
    IL_0022:  ldloc.1
    IL_0023:  call       string [mscorlib]System.String::Concat(string,
                                                                string)
    IL_0028:  ldstr      "1337"
    IL_002d:  ldc.i4.0
    IL_002e:  ldc.i4.s   64
    IL_0030:  call       valuetype [System.Windows.Forms]System.Windows.Forms.DialogResult [System.Windows.Forms]System.Windows.Forms.MessageBox::Show(string,
                                                                                                                                                       string,
                                                                                                                                                       valuetype [System.Windows.Forms]System.Windows.Forms.MessageBoxButtons,
                                                                                                                                                       valuetype [System.Windows.Forms]System.Windows.Forms.MessageBoxIcon)
    IL_0035:  pop
    IL_0036:  ldloc.1
    IL_0037:  call       void [System.Windows.Forms]System.Windows.Forms.Clipboard::SetText(string)
    IL_003c:  nop
    IL_003d:  nop
    IL_003e:  ret
  } // end of method Form1::ShowFlag

  .method private hidebysig instance string 
          GenerateFlag() cil managed
  {
    // Code size       298 (0x12a)
    .maxstack  3
    .locals init (class [mscorlib]System.Text.StringBuilder V_0,
             string V_1)
    IL_0000:  nop
    IL_0001:  newobj     instance void [mscorlib]System.Text.StringBuilder::.ctor()
    IL_0006:  stloc.0
    IL_0007:  ldloc.0
    IL_0008:  ldarg.0
    IL_0009:  ldc.i4.0
    IL_000a:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_000f:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_0014:  pop
    IL_0015:  ldloc.0
    IL_0016:  ldarg.0
    IL_0017:  ldc.i4.0
    IL_0018:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_001d:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_0022:  pop
    IL_0023:  ldloc.0
    IL_0024:  ldarg.0
    IL_0025:  ldc.i4.1
    IL_0026:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_002b:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_0030:  pop
    IL_0031:  ldloc.0
    IL_0032:  ldarg.0
    IL_0033:  ldc.i4.2
    IL_0034:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_0039:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_003e:  pop
    IL_003f:  ldloc.0
    IL_0040:  ldarg.0
    IL_0041:  ldc.i4.s   31
    IL_0043:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_0048:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_004d:  pop
    IL_004e:  ldloc.0
    IL_004f:  ldarg.0
    IL_0050:  ldc.i4.s   32
    IL_0052:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_0057:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_005c:  pop
    IL_005d:  ldloc.0
    IL_005e:  ldarg.0
    IL_005f:  ldc.i4.s   33
    IL_0061:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_0066:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_006b:  pop
    IL_006c:  ldloc.0
    IL_006d:  ldarg.0
    IL_006e:  ldc.i4.s   34
    IL_0070:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_0075:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_007a:  pop
    IL_007b:  ldloc.0
    IL_007c:  ldarg.0
    IL_007d:  ldc.i4.s   41
    IL_007f:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_0084:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_0089:  pop
    IL_008a:  ldloc.0
    IL_008b:  ldarg.0
    IL_008c:  ldc.i4.s   41
    IL_008e:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_0093:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_0098:  pop
    IL_0099:  ldloc.0
    IL_009a:  ldarg.0
    IL_009b:  ldc.i4.s   42
    IL_009d:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_00a2:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_00a7:  pop
    IL_00a8:  ldloc.0
    IL_00a9:  ldarg.0
    IL_00aa:  ldc.i4.s   43
    IL_00ac:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_00b1:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_00b6:  pop
    IL_00b7:  ldloc.0
    IL_00b8:  ldarg.0
    IL_00b9:  ldc.i4.s   44
    IL_00bb:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_00c0:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_00c5:  pop
    IL_00c6:  ldloc.0
    IL_00c7:  ldarg.0
    IL_00c8:  ldc.i4.s   45
    IL_00ca:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_00cf:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_00d4:  pop
    IL_00d5:  ldloc.0
    IL_00d6:  ldarg.0
    IL_00d7:  ldc.i4.s   46
    IL_00d9:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_00de:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_00e3:  pop
    IL_00e4:  ldloc.0
    IL_00e5:  ldarg.0
    IL_00e6:  ldc.i4.s   47
    IL_00e8:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_00ed:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_00f2:  pop
    IL_00f3:  ldloc.0
    IL_00f4:  ldarg.0
    IL_00f5:  ldc.i4.s   48
    IL_00f7:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_00fc:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_0101:  pop
    IL_0102:  ldloc.0
    IL_0103:  ldarg.0
    IL_0104:  ldc.i4.s   49
    IL_0106:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_010b:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_0110:  pop
    IL_0111:  ldloc.0
    IL_0112:  ldarg.0
    IL_0113:  ldc.i4.3
    IL_0114:  call       instance char StuckAt99.Form1::GetCharacter(int32)
    IL_0119:  callvirt   instance class [mscorlib]System.Text.StringBuilder [mscorlib]System.Text.StringBuilder::Append(char)
    IL_011e:  pop
    IL_011f:  ldloc.0
    IL_0120:  callvirt   instance string [mscorlib]System.Object::ToString()
    IL_0125:  stloc.1
    IL_0126:  br.s       IL_0128

    IL_0128:  ldloc.1
    IL_0129:  ret
  } // end of method Form1::GenerateFlag

  .method private hidebysig instance void 
          progressBar1_Click_1(object sender,
                               class [mscorlib]System.EventArgs e) cil managed
  {
    // Code size       2 (0x2)
    .maxstack  8
    IL_0000:  nop
    IL_0001:  ret
  } // end of method Form1::progressBar1_Click_1

  .method private hidebysig instance char 
          GetCharacter(int32 index) cil managed
  {
    // Code size       28 (0x1c)
    .maxstack  3
    .locals init (char[] V_0,
             char V_1)
    IL_0000:  nop
    IL_0001:  ldc.i4.s   112
    IL_0003:  newarr     [mscorlib]System.Char
    IL_0008:  dup
    IL_0009:  ldtoken    field valuetype '<PrivateImplementationDetails>'/'__StaticArrayInitTypeSize=224' '<PrivateImplementationDetails>'::'4760AEBD12ED2244AE32873BBCE02C0ED076BD7C897D97AF58B7E666E4379BD1'
    IL_000e:  call       void [mscorlib]System.Runtime.CompilerServices.RuntimeHelpers::InitializeArray(class [mscorlib]System.Array,
                                                                                                        valuetype [mscorlib]System.RuntimeFieldHandle)
    IL_0013:  stloc.0
    IL_0014:  ldloc.0
    IL_0015:  ldarg.1
    IL_0016:  ldelem.u2
    IL_0017:  stloc.1
    IL_0018:  br.s       IL_001a

    IL_001a:  ldloc.1
    IL_001b:  ret
  } // end of method Form1::GetCharacter

  .method family hidebysig virtual instance void 
          Dispose(bool disposing) cil managed
  {
    // Code size       43 (0x2b)
    .maxstack  2
    .locals init (bool V_0)
    IL_0000:  nop
    IL_0001:  ldarg.1
    IL_0002:  brfalse.s  IL_000f

    IL_0004:  ldarg.0
    IL_0005:  ldfld      class [System]System.ComponentModel.IContainer StuckAt99.Form1::components
    IL_000a:  ldnull
    IL_000b:  cgt.un
    IL_000d:  br.s       IL_0010

    IL_000f:  ldc.i4.0
    IL_0010:  stloc.0
    IL_0011:  ldloc.0
    IL_0012:  brfalse.s  IL_0022

    IL_0014:  nop
    IL_0015:  ldarg.0
    IL_0016:  ldfld      class [System]System.ComponentModel.IContainer StuckAt99.Form1::components
    IL_001b:  callvirt   instance void [mscorlib]System.IDisposable::Dispose()
    IL_0020:  nop
    IL_0021:  nop
    IL_0022:  ldarg.0
    IL_0023:  ldarg.1
    IL_0024:  call       instance void [System.Windows.Forms]System.Windows.Forms.Form::Dispose(bool)
    IL_0029:  nop
    IL_002a:  ret
  } // end of method Form1::Dispose

  .method private hidebysig instance void 
          InitializeComponent() cil managed
  {
    // Code size       523 (0x20b)
    .maxstack  6
    .locals init (class [System]System.ComponentModel.ComponentResourceManager V_0)
    IL_0000:  nop
    IL_0001:  ldtoken    StuckAt99.Form1
    IL_0006:  call       class [mscorlib]System.Type [mscorlib]System.Type::GetTypeFromHandle(valuetype [mscorlib]System.RuntimeTypeHandle)
    IL_000b:  newobj     instance void [System]System.ComponentModel.ComponentResourceManager::.ctor(class [mscorlib]System.Type)
    IL_0010:  stloc.0
    IL_0011:  ldarg.0
    IL_0012:  newobj     instance void [System.Windows.Forms]System.Windows.Forms.Button::.ctor()
    IL_0017:  stfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_001c:  ldarg.0
    IL_001d:  newobj     instance void [System.Windows.Forms]System.Windows.Forms.ProgressBar::.ctor()
    IL_0022:  stfld      class [System.Windows.Forms]System.Windows.Forms.ProgressBar StuckAt99.Form1::progressBar1
    IL_0027:  ldarg.0
    IL_0028:  call       instance void [System.Windows.Forms]System.Windows.Forms.Control::SuspendLayout()
    IL_002d:  nop
    IL_002e:  ldarg.0
    IL_002f:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_0034:  call       valuetype [System.Drawing]System.Drawing.Color [System.Drawing]System.Drawing.SystemColors::get_ActiveBorder()
    IL_0039:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_BackColor(valuetype [System.Drawing]System.Drawing.Color)
    IL_003e:  nop
    IL_003f:  ldarg.0
    IL_0040:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_0045:  call       class [System.Windows.Forms]System.Windows.Forms.Cursor [System.Windows.Forms]System.Windows.Forms.Cursors::get_Hand()
    IL_004a:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_Cursor(class [System.Windows.Forms]System.Windows.Forms.Cursor)
    IL_004f:  nop
    IL_0050:  ldarg.0
    IL_0051:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_0056:  ldc.i4.1
    IL_0057:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.ButtonBase::set_FlatStyle(valuetype [System.Windows.Forms]System.Windows.Forms.FlatStyle)
    IL_005c:  nop
    IL_005d:  ldarg.0
    IL_005e:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_0063:  ldstr      "Microsoft Sans Serif"
    IL_0068:  ldc.r4     8.25
    IL_006d:  ldc.i4.0
    IL_006e:  ldc.i4.3
    IL_006f:  ldc.i4.0
    IL_0070:  newobj     instance void [System.Drawing]System.Drawing.Font::.ctor(string,
                                                                                  float32,
                                                                                  valuetype [System.Drawing]System.Drawing.FontStyle,
                                                                                  valuetype [System.Drawing]System.Drawing.GraphicsUnit,
                                                                                  uint8)
    IL_0075:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_Font(class [System.Drawing]System.Drawing.Font)
    IL_007a:  nop
    IL_007b:  ldarg.0
    IL_007c:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_0081:  call       valuetype [System.Drawing]System.Drawing.Color [System.Drawing]System.Drawing.SystemColors::get_ActiveCaptionText()
    IL_0086:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_ForeColor(valuetype [System.Drawing]System.Drawing.Color)
    IL_008b:  nop
    IL_008c:  ldarg.0
    IL_008d:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_0092:  ldc.i4     0x87
    IL_0097:  ldc.i4.s   121
    IL_0099:  newobj     instance void [System.Drawing]System.Drawing.Point::.ctor(int32,
                                                                                   int32)
    IL_009e:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_Location(valuetype [System.Drawing]System.Drawing.Point)
    IL_00a3:  nop
    IL_00a4:  ldarg.0
    IL_00a5:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_00aa:  ldstr      "button1"
    IL_00af:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_Name(string)
    IL_00b4:  nop
    IL_00b5:  ldarg.0
    IL_00b6:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_00bb:  ldc.i4.s   75
    IL_00bd:  ldc.i4.s   23
    IL_00bf:  newobj     instance void [System.Drawing]System.Drawing.Size::.ctor(int32,
                                                                                  int32)
    IL_00c4:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_Size(valuetype [System.Drawing]System.Drawing.Size)
    IL_00c9:  nop
    IL_00ca:  ldarg.0
    IL_00cb:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_00d0:  ldc.i4.0
    IL_00d1:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_TabIndex(int32)
    IL_00d6:  nop
    IL_00d7:  ldarg.0
    IL_00d8:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_00dd:  ldstr      "Get flag"
    IL_00e2:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_Text(string)
    IL_00e7:  nop
    IL_00e8:  ldarg.0
    IL_00e9:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_00ee:  ldc.i4.0
    IL_00ef:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.ButtonBase::set_UseVisualStyleBackColor(bool)
    IL_00f4:  nop
    IL_00f5:  ldarg.0
    IL_00f6:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_00fb:  ldarg.0
    IL_00fc:  ldftn      instance void StuckAt99.Form1::button1_Click(object,
                                                                      class [mscorlib]System.EventArgs)
    IL_0102:  newobj     instance void [mscorlib]System.EventHandler::.ctor(object,
                                                                            native int)
    IL_0107:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::add_Click(class [mscorlib]System.EventHandler)
    IL_010c:  nop
    IL_010d:  ldarg.0
    IL_010e:  ldfld      class [System.Windows.Forms]System.Windows.Forms.ProgressBar StuckAt99.Form1::progressBar1
    IL_0113:  ldc.i4     0xfc
    IL_0118:  ldc.i4.s   121
    IL_011a:  newobj     instance void [System.Drawing]System.Drawing.Point::.ctor(int32,
                                                                                   int32)
    IL_011f:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_Location(valuetype [System.Drawing]System.Drawing.Point)
    IL_0124:  nop
    IL_0125:  ldarg.0
    IL_0126:  ldfld      class [System.Windows.Forms]System.Windows.Forms.ProgressBar StuckAt99.Form1::progressBar1
    IL_012b:  ldstr      "progressBar1"
    IL_0130:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_Name(string)
    IL_0135:  nop
    IL_0136:  ldarg.0
    IL_0137:  ldfld      class [System.Windows.Forms]System.Windows.Forms.ProgressBar StuckAt99.Form1::progressBar1
    IL_013c:  ldc.i4     0x19e
    IL_0141:  ldc.i4.s   23
    IL_0143:  newobj     instance void [System.Drawing]System.Drawing.Size::.ctor(int32,
                                                                                  int32)
    IL_0148:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_Size(valuetype [System.Drawing]System.Drawing.Size)
    IL_014d:  nop
    IL_014e:  ldarg.0
    IL_014f:  ldfld      class [System.Windows.Forms]System.Windows.Forms.ProgressBar StuckAt99.Form1::progressBar1
    IL_0154:  ldc.i4.1
    IL_0155:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_TabIndex(int32)
    IL_015a:  nop
    IL_015b:  ldarg.0
    IL_015c:  ldfld      class [System.Windows.Forms]System.Windows.Forms.ProgressBar StuckAt99.Form1::progressBar1
    IL_0161:  ldarg.0
    IL_0162:  ldftn      instance void StuckAt99.Form1::progressBar1_Click_1(object,
                                                                             class [mscorlib]System.EventArgs)
    IL_0168:  newobj     instance void [mscorlib]System.EventHandler::.ctor(object,
                                                                            native int)
    IL_016d:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::add_Click(class [mscorlib]System.EventHandler)
    IL_0172:  nop
    IL_0173:  ldarg.0
    IL_0174:  ldc.r4     6.
    IL_0179:  ldc.r4     13.
    IL_017e:  newobj     instance void [System.Drawing]System.Drawing.SizeF::.ctor(float32,
                                                                                   float32)
    IL_0183:  call       instance void [System.Windows.Forms]System.Windows.Forms.ContainerControl::set_AutoScaleDimensions(valuetype [System.Drawing]System.Drawing.SizeF)
    IL_0188:  nop
    IL_0189:  ldarg.0
    IL_018a:  ldc.i4.1
    IL_018b:  call       instance void [System.Windows.Forms]System.Windows.Forms.ContainerControl::set_AutoScaleMode(valuetype [System.Windows.Forms]System.Windows.Forms.AutoScaleMode)
    IL_0190:  nop
    IL_0191:  ldarg.0
    IL_0192:  ldc.i4     0x2da
    IL_0197:  ldc.i4     0xf8
    IL_019c:  newobj     instance void [System.Drawing]System.Drawing.Size::.ctor(int32,
                                                                                  int32)
    IL_01a1:  call       instance void [System.Windows.Forms]System.Windows.Forms.Form::set_ClientSize(valuetype [System.Drawing]System.Drawing.Size)
    IL_01a6:  nop
    IL_01a7:  ldarg.0
    IL_01a8:  call       instance class [System.Windows.Forms]System.Windows.Forms.Control/ControlCollection [System.Windows.Forms]System.Windows.Forms.Control::get_Controls()
    IL_01ad:  ldarg.0
    IL_01ae:  ldfld      class [System.Windows.Forms]System.Windows.Forms.ProgressBar StuckAt99.Form1::progressBar1
    IL_01b3:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control/ControlCollection::Add(class [System.Windows.Forms]System.Windows.Forms.Control)
    IL_01b8:  nop
    IL_01b9:  ldarg.0
    IL_01ba:  call       instance class [System.Windows.Forms]System.Windows.Forms.Control/ControlCollection [System.Windows.Forms]System.Windows.Forms.Control::get_Controls()
    IL_01bf:  ldarg.0
    IL_01c0:  ldfld      class [System.Windows.Forms]System.Windows.Forms.Button StuckAt99.Form1::button1
    IL_01c5:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control/ControlCollection::Add(class [System.Windows.Forms]System.Windows.Forms.Control)
    IL_01ca:  nop
    IL_01cb:  ldarg.0
    IL_01cc:  ldc.i4.1
    IL_01cd:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_DoubleBuffered(bool)
    IL_01d2:  nop
    IL_01d3:  ldarg.0
    IL_01d4:  ldloc.0
    IL_01d5:  ldstr      "$this.Icon"
    IL_01da:  callvirt   instance object [mscorlib]System.Resources.ResourceManager::GetObject(string)
    IL_01df:  castclass  [System.Drawing]System.Drawing.Icon
    IL_01e4:  call       instance void [System.Windows.Forms]System.Windows.Forms.Form::set_Icon(class [System.Drawing]System.Drawing.Icon)
    IL_01e9:  nop
    IL_01ea:  ldarg.0
    IL_01eb:  ldstr      "Form1"
    IL_01f0:  call       instance void [System.Windows.Forms]System.Windows.Forms.Control::set_Name(string)
    IL_01f5:  nop
    IL_01f6:  ldarg.0
    IL_01f7:  ldstr      "StuckAt99"
    IL_01fc:  callvirt   instance void [System.Windows.Forms]System.Windows.Forms.Control::set_Text(string)
    IL_0201:  nop
    IL_0202:  ldarg.0
    IL_0203:  ldc.i4.0
    IL_0204:  call       instance void [System.Windows.Forms]System.Windows.Forms.Control::ResumeLayout(bool)
    IL_0209:  nop
    IL_020a:  ret
  } // end of method Form1::InitializeComponent

} // end of class StuckAt99.Form1

.class private abstract auto ansi sealed beforefieldinit StuckAt99.Program
       extends [mscorlib]System.Object
{
  .method private hidebysig static void  Main() cil managed
  {
    .entrypoint
    .custom instance void [mscorlib]System.STAThreadAttribute::.ctor() = ( 01 00 00 00 ) 
    // Code size       26 (0x1a)
    .maxstack  8
    IL_0000:  nop
    IL_0001:  call       void [System.Windows.Forms]System.Windows.Forms.Application::EnableVisualStyles()
    IL_0006:  nop
    IL_0007:  ldc.i4.0
    IL_0008:  call       void [System.Windows.Forms]System.Windows.Forms.Application::SetCompatibleTextRenderingDefault(bool)
    IL_000d:  nop
    IL_000e:  newobj     instance void StuckAt99.Form1::.ctor()
    IL_0013:  call       void [System.Windows.Forms]System.Windows.Forms.Application::Run(class [System.Windows.Forms]System.Windows.Forms.Form)
    IL_0018:  nop
    IL_0019:  ret
  } // end of method Program::Main

} // end of class StuckAt99.Program

.class private auto ansi beforefieldinit StuckAt99.Properties.Resources
       extends [mscorlib]System.Object
{
  .custom instance void [System]System.CodeDom.Compiler.GeneratedCodeAttribute::.ctor(string,
                                                                                      string) = ( 01 00 33 53 79 73 74 65 6D 2E 52 65 73 6F 75 72   // ..3System.Resour
                                                                                                  63 65 73 2E 54 6F 6F 6C 73 2E 53 74 72 6F 6E 67   // ces.Tools.Strong
                                                                                                  6C 79 54 79 70 65 64 52 65 73 6F 75 72 63 65 42   // lyTypedResourceB
                                                                                                  75 69 6C 64 65 72 08 31 37 2E 30 2E 30 2E 30 00   // uilder.17.0.0.0.
                                                                                                  00 ) 
  .custom instance void [mscorlib]System.Diagnostics.DebuggerNonUserCodeAttribute::.ctor() = ( 01 00 00 00 ) 
  .custom instance void [mscorlib]System.Runtime.CompilerServices.CompilerGeneratedAttribute::.ctor() = ( 01 00 00 00 ) 
  .field private static class [mscorlib]System.Resources.ResourceManager resourceMan
  .field private static class [mscorlib]System.Globalization.CultureInfo resourceCulture
  .method assembly hidebysig specialname rtspecialname 
          instance void  .ctor() cil managed
  {
    // Code size       9 (0x9)
    .maxstack  8
    IL_0000:  ldarg.0
    IL_0001:  call       instance void [mscorlib]System.Object::.ctor()
    IL_0006:  nop
    IL_0007:  nop
    IL_0008:  ret
  } // end of method Resources::.ctor

  .method assembly hidebysig specialname static 
          class [mscorlib]System.Resources.ResourceManager 
          get_ResourceManager() cil managed
  {
    // Code size       57 (0x39)
    .maxstack  2
    .locals init (bool V_0,
             class [mscorlib]System.Resources.ResourceManager V_1,
             class [mscorlib]System.Resources.ResourceManager V_2)
    IL_0000:  nop
    IL_0001:  ldsfld     class [mscorlib]System.Resources.ResourceManager StuckAt99.Properties.Resources::resourceMan
    IL_0006:  ldnull
    IL_0007:  ceq
    IL_0009:  stloc.0
    IL_000a:  ldloc.0
    IL_000b:  brfalse.s  IL_002f

    IL_000d:  nop
    IL_000e:  ldstr      "StuckAt99.Properties.Resources"
    IL_0013:  ldtoken    StuckAt99.Properties.Resources
    IL_0018:  call       class [mscorlib]System.Type [mscorlib]System.Type::GetTypeFromHandle(valuetype [mscorlib]System.RuntimeTypeHandle)
    IL_001d:  callvirt   instance class [mscorlib]System.Reflection.Assembly [mscorlib]System.Type::get_Assembly()
    IL_0022:  newobj     instance void [mscorlib]System.Resources.ResourceManager::.ctor(string,
                                                                                         class [mscorlib]System.Reflection.Assembly)
    IL_0027:  stloc.1
    IL_0028:  ldloc.1
    IL_0029:  stsfld     class [mscorlib]System.Resources.ResourceManager StuckAt99.Properties.Resources::resourceMan
    IL_002e:  nop
    IL_002f:  ldsfld     class [mscorlib]System.Resources.ResourceManager StuckAt99.Properties.Resources::resourceMan
    IL_0034:  stloc.2
    IL_0035:  br.s       IL_0037

    IL_0037:  ldloc.2
    IL_0038:  ret
  } // end of method Resources::get_ResourceManager

  .method assembly hidebysig specialname static 
          class [mscorlib]System.Globalization.CultureInfo 
          get_Culture() cil managed
  {
    // Code size       11 (0xb)
    .maxstack  1
    .locals init (class [mscorlib]System.Globalization.CultureInfo V_0)
    IL_0000:  nop
    IL_0001:  ldsfld     class [mscorlib]System.Globalization.CultureInfo StuckAt99.Properties.Resources::resourceCulture
    IL_0006:  stloc.0
    IL_0007:  br.s       IL_0009

    IL_0009:  ldloc.0
    IL_000a:  ret
  } // end of method Resources::get_Culture

  .method assembly hidebysig specialname static 
          void  set_Culture(class [mscorlib]System.Globalization.CultureInfo 'value') cil managed
  {
    // Code size       8 (0x8)
    .maxstack  8
    IL_0000:  nop
    IL_0001:  ldarg.0
    IL_0002:  stsfld     class [mscorlib]System.Globalization.CultureInfo StuckAt99.Properties.Resources::resourceCulture
    IL_0007:  ret
  } // end of method Resources::set_Culture

  .method assembly hidebysig specialname static 
          class [System.Drawing]System.Drawing.Bitmap 
          get_output_onlinegiftools() cil managed
  {
    // Code size       33 (0x21)
    .maxstack  3
    .locals init (object V_0,
             class [System.Drawing]System.Drawing.Bitmap V_1)
    IL_0000:  nop
    IL_0001:  call       class [mscorlib]System.Resources.ResourceManager StuckAt99.Properties.Resources::get_ResourceManager()
    IL_0006:  ldstr      "output-onlinegiftools"
    IL_000b:  ldsfld     class [mscorlib]System.Globalization.CultureInfo StuckAt99.Properties.Resources::resourceCulture
    IL_0010:  callvirt   instance object [mscorlib]System.Resources.ResourceManager::GetObject(string,
                                                                                               class [mscorlib]System.Globalization.CultureInfo)
    IL_0015:  stloc.0
    IL_0016:  ldloc.0
    IL_0017:  castclass  [System.Drawing]System.Drawing.Bitmap
    IL_001c:  stloc.1
    IL_001d:  br.s       IL_001f

    IL_001f:  ldloc.1
    IL_0020:  ret
  } // end of method Resources::get_output_onlinegiftools

  .property class [mscorlib]System.Resources.ResourceManager
          ResourceManager()
  {
    .custom instance void [System]System.ComponentModel.EditorBrowsableAttribute::.ctor(valuetype [System]System.ComponentModel.EditorBrowsableState) = ( 01 00 02 00 00 00 00 00 ) 
    .get class [mscorlib]System.Resources.ResourceManager StuckAt99.Properties.Resources::get_ResourceManager()
  } // end of property Resources::ResourceManager
  .property class [mscorlib]System.Globalization.CultureInfo
          Culture()
  {
    .custom instance void [System]System.ComponentModel.EditorBrowsableAttribute::.ctor(valuetype [System]System.ComponentModel.EditorBrowsableState) = ( 01 00 02 00 00 00 00 00 ) 
    .get class [mscorlib]System.Globalization.CultureInfo StuckAt99.Properties.Resources::get_Culture()
    .set void StuckAt99.Properties.Resources::set_Culture(class [mscorlib]System.Globalization.CultureInfo)
  } // end of property Resources::Culture
  .property class [System.Drawing]System.Drawing.Bitmap
          output_onlinegiftools()
  {
    .get class [System.Drawing]System.Drawing.Bitmap StuckAt99.Properties.Resources::get_output_onlinegiftools()
  } // end of property Resources::output_onlinegiftools
} // end of class StuckAt99.Properties.Resources

.class private auto ansi sealed beforefieldinit StuckAt99.Properties.Settings
       extends [System]System.Configuration.ApplicationSettingsBase
{
  .custom instance void [mscorlib]System.Runtime.CompilerServices.CompilerGeneratedAttribute::.ctor() = ( 01 00 00 00 ) 
  .custom instance void [System]System.CodeDom.Compiler.GeneratedCodeAttribute::.ctor(string,
                                                                                      string) = ( 01 00 4B 4D 69 63 72 6F 73 6F 66 74 2E 56 69 73   // ..KMicrosoft.Vis
                                                                                                  75 61 6C 53 74 75 64 69 6F 2E 45 64 69 74 6F 72   // ualStudio.Editor
                                                                                                  73 2E 53 65 74 74 69 6E 67 73 44 65 73 69 67 6E   // s.SettingsDesign
                                                                                                  65 72 2E 53 65 74 74 69 6E 67 73 53 69 6E 67 6C   // er.SettingsSingl
                                                                                                  65 46 69 6C 65 47 65 6E 65 72 61 74 6F 72 08 31   // eFileGenerator.1
                                                                                                  31 2E 30 2E 30 2E 30 00 00 )                      // 1.0.0.0..
  .field private static class StuckAt99.Properties.Settings defaultInstance
  .method public hidebysig specialname static 
          class StuckAt99.Properties.Settings 
          get_Default() cil managed
  {
    // Code size       11 (0xb)
    .maxstack  1
    .locals init (class StuckAt99.Properties.Settings V_0)
    IL_0000:  nop
    IL_0001:  ldsfld     class StuckAt99.Properties.Settings StuckAt99.Properties.Settings::defaultInstance
    IL_0006:  stloc.0
    IL_0007:  br.s       IL_0009

    IL_0009:  ldloc.0
    IL_000a:  ret
  } // end of method Settings::get_Default

  .method public hidebysig specialname rtspecialname 
          instance void  .ctor() cil managed
  {
    // Code size       8 (0x8)
    .maxstack  8
    IL_0000:  ldarg.0
    IL_0001:  call       instance void [System]System.Configuration.ApplicationSettingsBase::.ctor()
    IL_0006:  nop
    IL_0007:  ret
  } // end of method Settings::.ctor

  .method private hidebysig specialname rtspecialname static 
          void  .cctor() cil managed
  {
    // Code size       21 (0x15)
    .maxstack  8
    IL_0000:  newobj     instance void StuckAt99.Properties.Settings::.ctor()
    IL_0005:  call       class [System]System.Configuration.SettingsBase [System]System.Configuration.SettingsBase::Synchronized(class [System]System.Configuration.SettingsBase)
    IL_000a:  castclass  StuckAt99.Properties.Settings
    IL_000f:  stsfld     class StuckAt99.Properties.Settings StuckAt99.Properties.Settings::defaultInstance
    IL_0014:  ret
  } // end of method Settings::.cctor

  .property class StuckAt99.Properties.Settings
          Default()
  {
    .get class StuckAt99.Properties.Settings StuckAt99.Properties.Settings::get_Default()
  } // end of property Settings::Default
} // end of class StuckAt99.Properties.Settings

.class private auto ansi sealed '<PrivateImplementationDetails>'
       extends [mscorlib]System.Object
{
  .custom instance void [mscorlib]System.Runtime.CompilerServices.CompilerGeneratedAttribute::.ctor() = ( 01 00 00 00 ) 
  .class explicit ansi sealed nested assembly '__StaticArrayInitTypeSize=224'
         extends [mscorlib]System.ValueType
  {
    .pack 1
    .size 224
  } // end of class '__StaticArrayInitTypeSize=224'

  .field static assembly initonly valuetype '<PrivateImplementationDetails>'/'__StaticArrayInitTypeSize=224' '4760AEBD12ED2244AE32873BBCE02C0ED076BD7C897D97AF58B7E666E4379BD1' at I_00042988
} // end of class '<PrivateImplementationDetails>'


// =============================================================

.data cil I_00042988 = bytearray (
                 44 00 43 00 7B 00 7D 00 59 00 62 00 39 00 5F 00  // D.C.{.}.Y.b.9._.
                 48 00 6A 00 58 00 34 00 4C 00 66 00 32 00 75 00  // H.j.X.4.L.f.2.u.
                 56 00 7A 00 73 00 4D 00 4B 00 44 00 50 00 74 00  // V.z.s.M.K.D.P.t.
                 6E 00 46 00 31 00 30 00 72 00 61 00 7A 00 66 00  // n.F.1.0.r.a.z.f.
                 31 00 6E 00 65 00 6C 00 48 00 41 00 53 00 69 00  // 1.n.e.l.H.A.S.i.
                 74 00 5F 00 6D 00 34 00 6E 00 75 00 61 00 6C 00  // t._.m.4.n.u.a.l.
                 6C 00 79 00 47 00 6F 00 64 00 62 00 6C 00 65 00  // l.y.G.o.d.b.l.e.
                 43 00 36 00 70 00 59 00 64 00 49 00 77 00 71 00  // C.6.p.Y.d.I.w.q.
                 62 00 4D 00 6E 00 4A 00 33 00 7A 00 58 00 73 00  // b.M.n.J.3.z.X.s.
                 46 00 72 00 74 00 43 00 67 00 51 00 31 00 4C 00  // F.r.t.C.g.Q.1.L.
                 38 00 4E 00 65 00 5F 00 75 00 54 00 73 00 30 00  // 8.N.e._.u.T.s.0.
                 79 00 6B 00 66 00 50 00 68 00 56 00 63 00 57 00  // y.k.f.P.h.V.c.W.
                 6A 00 32 00 6C 00 42 00 37 00 72 00 4F 00 58 00  // j.2.l.B.7.r.O.X.
                 65 00 39 00 53 00 61 00 4D 00 54 00 6E 00 21 00) // e.9.S.a.M.T.n.!.
// *********** DISASSEMBLY COMPLETE ***********************
// WARNING: Created Win32 resource file F:\Coding\projects\git\Mig\CTF\2025\ddc_regionals\binary_StuckAt99\bn_StuckAt99\StuckAt99.res
