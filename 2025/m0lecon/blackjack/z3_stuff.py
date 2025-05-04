import z3

solver = z3.Solver()

# 4 symbolic bytes for player_choice (each is an 8-bit ASCII character)
c0, c1, c2, c3 = z3.BitVecs("c0 c1 c2 c3", 8)

# Ensure all input characters are valid ASCII (printable)
for c in [c0, c1, c2, c3]:
    solver.add(c >= 32, c <= 126)  # Space (32) to tilde (126)

# Convert to a 32-bit integer representation (explicit BitVec conversion)
player_choice = z3.Concat(c0, c1, c2, c3)  # 32-bit

# Define the function computation (simplified model)
S1, S2, S3, S4 = z3.BitVecs("S1 S2 S3 S4", 32)

# Explicitly cast `player_choice` to 32-bit to match operands
computed_result = (S1 + S2 + S3 + S4) ^ player_choice

# The return value must be 'p', 's', 'h', or 'd'
allowed_outputs = [ord('p'), ord('s'), ord('h'), ord('d')]
solver.add(z3.Or([computed_result == a for a in allowed_outputs]))

# Find all valid 4-character player_choice values
print("Valid player_choice inputs:")
while solver.check() == z3.sat:
    model = solver.model()
    value = [chr(model[c].as_long()) for c in [c0, c1, c2, c3]]
    print("".join(value))
    # Exclude this solution to find more
    solver.add(z3.Or([c0 != model[c0], c1 != model[c1], c2 != model[c2], c3 != model[c3]]))

print("Done")
