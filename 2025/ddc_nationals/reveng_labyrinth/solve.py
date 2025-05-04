import angr
import claripy

def main():
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


    The correct path is at 0x12e5, the wrong path is at 0x1314
    """
    proj = angr.Project('./labyrinth', auto_load_libs=False)

    # Create a symbolic variable for the input, it is 16 integers which can be 1, 2 or 3
    input_size = 16
    # Create a list of symbolic variables for the input
    input_list = [claripy.BVS('input_%d' % i, 4) for i in range(input_size)]
    # Also needs newline
    input_str = claripy.Concat( *input_list, claripy.BVV(b'\n', 8))

    # Create a state for the program
    st = proj.factory.entry_state(args=['./labyrinth'], add_options=angr.options.unicorn, stdin=input_str)

    # Create a list of constraints for the input
    for i in input_list:
        # Each input must be between 1 and 3
        st.solver.add(i >= 1)
        st.solver.add(i <= 3)

    # Create a simulation manager
    sm = proj.factory.simulation_manager(st)

    # Explore the state until it finds a solution
    sol_bin = 0x12e5
    avoid_bin = 0x1314
    sm.explore(find=0x400000 + sol_bin, avoid=0x400000 + avoid_bin)

    if sm.found:
        # Get the first found state
        found_state = sm.found[0]
        # Get the input values
        input_values = found_state.solver.eval(input_list, cast_to=bytes)
        # Convert the input values to a string
        input_string = ''.join([str(i) for i in input_values])
        # Print the input values
        print("Input values:", input_string)
    else:
        # If no solution is found, return an error message
        return 'No solution found'

    

    

    

def test():
    assert main() == 'Math is hard!'

if __name__ == '__main__':
    print(main())