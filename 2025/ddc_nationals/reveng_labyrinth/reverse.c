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