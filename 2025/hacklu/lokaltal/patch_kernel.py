from nyxstone import Nyxstone

patches = {}



syms = dict(
# a padding area after a function that is safe to overwrite
# we write the removed call to AlpcpReferenceBlob here
    code_cave = 0x1408b42d0,


# The unconditional jump that is used to jump from the end of the view construction block to the common "unlock blob and return" code path
# it is a small basic block that stores the view pointer to the "view out" pointer passed to the function
# in the case of the 11 24h2 / 11 25h2 kernel, this code is implemented as

# mov rax, [rbp+90h] ; load the saved argument
# xor ebx, ebx ; needed for later
# mov [rax], r14 ; store the view pointer, which is stored in r14 during most of the function
# jmp loc_alpc_unlock_and_return ; go to the common epilogue

# we patch the last jump to go to our code cave where we call the ALpcpReferenceBlob. This is roughly the same location
# where the call was in the unpatched windows version that is affected by the CVE
    insert_call_loc = 0x1408b40ba,

# The address of the epilogue basic block, i.e. the original jump target
    dest_after_patch = 0x1408B4177,


# location where AlpcpReferenceBlob is called in the non-vulnerable code, we have to patch this call
# to reintroduce the race condition
    remove_call_loc = 0x1408b3fb3,

# the function we need to call
    AlpcpReferenceBlob = 0x1408b4930
)

patches[syms['insert_call_loc']] = 'jmp code_cave'

patches[syms['code_cave']] = 'mov rcx, r14; call AlpcpReferenceBlob; jmp dest_after_patch'

patches[syms['remove_call_loc']] = b'\x90' * 5

ns = Nyxstone('amd64')


for addr,patch in patches.items():
    if isinstance(patch, bytes):
        patch_code = patch
    else:
        patch_code = bytes(ns.assemble(patches[addr], address=addr, labels=syms))

    print(f'patch @ {addr:#x} len {len(patch_code)}: {patch_code.hex(sep=' ')}')

print("Apply patches manually to the binary (e.g. with IDA)_and recalculate the checksum")