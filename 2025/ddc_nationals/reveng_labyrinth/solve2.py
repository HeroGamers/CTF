
"""
undefined8 main(void)

{
  int correct;
  char flag [16];
  undefined local_98;
  undefined try_hash [44];
  int number;
  int number_thing [19];
  int i;
  
  puts("Welcome to the Labyrinth!");
  puts(
      "Make your way through the labyrinth by choosing one of the three paths (1, 2, or 3) at each c hoice."
      );
  for (i = 0; i < 16; i = i + 1) {
    printf("Choice %d - Enter a number between 1 and 3: ",(ulong)(i + 1));
    __isoc99_scanf(&DAT_001020bd,&number);
    if ((number < 1) || (3 < number)) {
      puts("Invalid choice! Please choose 1, 2, or 3.");
      i = i + -1;
    }
    else {
      number_thing[i] = number;
      flag[i] = (char)number + '0';
    }
  }
  local_98 = 0;
  compute_sha256(number_thing,0x40,try_hash);
  correct = memcmp(try_hash,correct_hash,0x20);
  if (correct == 0) {
    puts("Congratulations! You\'ve escaped the labyrinth.");
    printf("DDC{%s}\n",flag);
  }
  else {
    puts("You ended up at a blind path! Try again...");
  }
  return 0;
}
"""

import z3

correct_hash = b'\xed\x7e\xdd\x1f\xe0\x12\xc1\xd2\xd8\xe5\x5d\xca\xcc\x9f\x56\x80\x96\xea\x31\xaa\x2c\xf9\x1c\x5b\xc1\xd7\x2e\x3b\x08\x6f\x06\x2d'

hash_to_hex = lambda x: ''.join(['%02x' % b for b in x]) # ed7edd1fe012c1d2d8e55dcacc9f568096ea31aa2cf91c5bc1d72e3b086f062d
print(hash_to_hex(correct_hash))

# Setup the Z3 solver

s = z3.Solver()

# Create a list of symbolic variables for the input
input_size = 16
input_list = [z3.BitVec('input_%d' % i, 4) for i in range(input_size)]
# Create a list of constraints for the input
for i in range(input_size):
    # Each input must be between 1 and 3
    s.add(z3.Or(input_list[i] == 1, input_list[i] == 2, input_list[i] == 3))

# Create a list of constraints for the hash
# The hash is computed by the function compute_sha256(number_thing,0x40,try_hash)
# The input is passed to the function as a list of integers
# The hash is compared to the correct hash
# The hash is 32 bytes long, so we need to create a list of 32 bytes

hash_size = 32
hash_list = [z3.BitVec('hash_%d' % i, 8) for i in range(hash_size)]

# Setup constraints for the hash
for i in range(hash_size):
    # The hash is computed by the function compute_sha256(number_thing,0x40,try_hash)
    # The input is passed to the function as a list of integers
    # The hash is compared to the correct hash
    s.add(hash_list[i] == correct_hash[i])

# Make the input match the hash
