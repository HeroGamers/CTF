import z3

FLAG_LENGTH = 30

# 8-bit vector per flag char
flag = z3.BitVecs(" ".join(f"flag[{i}]" for i in range(FLAG_LENGTH)), 8)
solver = z3.Solver()

### ADD CONSTRAINTS HERE ###
solver.add(flag[0] ^ flag[5] == 28)

# Check constraints and extract result from model
if solver.check() == z3.sat:
    print("".join([chr(solver.model()[c].as_long()) for c in flag]))
else:
    print("Unsatisfiable")