#include <stdio.h>
#include <stdlib.h>

struct gun_t {
  char name[32];
  int (*fun_ptr)(const char*);
};

void gunDefault(struct gun_t *gun) {
    system("clear");
    printf("\
                  \n\
 ,--^----------,--------,-----,-------^--, \n\
 | >%-9p< `--------'    %-9p   O\n\
 `+---------------------------^----------|\n\
   `\\_,-------, _________________________|\n\
     / XXXXXX /`|     /\n\
    / XXXXXX /  `\\   /\n\
   / XXXXXX /\\______(\n\
  / XXXXXX /\n\
 / XXXXXX /\n\
(________(\n\
 `------'\n\n", gun, &gun->fun_ptr);
}

void gunLoadMag(struct gun_t *gun, char* bullet) {
    system("clear");
    printf("\
 ,--^----------,--------,-----,-------^--, \n\
 | >%-9p< `--------'    %-9p   O\n\
 `+---------------------------^----------|\n\
   `\\_,-------, _________________________|\n\
     / XXXXXX /`|     /   __________ \n\
    / XXXXXX /  `\\   /   |%-10p|\n\
   / XXXXXX /\\______(    |%-10p|\n\
  / XXXXXX /             |%-10p|\n\
 / XXXXXX /              |%-10p|\n\
(________(               `----------'\n\n", gun, &gun->fun_ptr, bullet, bullet + 8, bullet + 12, bullet + 16);
}

void gunShoot(struct gun_t *gun) {
    system("clear");
    printf("\
                  \n\
 ,--^----------,........,-----,-------^--, \n\
 | >%-9p< `--------'    %-9p   Ø======+----------------+\n\
 `+---------------------------^----------|      |     BANG!      |\n\
   `\\_,-------, _________________________|      |  BANG! BANG!   |\n\
     / XXXXXX /`|     /                         |________________|\n\
    / XXXXXX /  `\\   /\n\
   / XXXXXX /\\______(\n\
  / XXXXXX /\n\
 / XXXXXX /\n\
(________(\n\
 `------'\n\n", gun, &gun->fun_ptr);
}

void gunTakeOutMag(struct gun_t *gun, char* bullet) {
    system("clear");
    printf("\
 ,--^----------,--------,-----,-------^--, \n\
 | >%-9p< `--------'    %-9p   O\n\
 `+---------------------------^----------|\n\
   `\\_,-------, _________________________|\n\
     / XXXXXX /`|     /   __________ \n\
    / XXXXXX /  `\\   /   |%-10p|\n\
   / XXXXXX /\\______(    |%-10p|\n\
  / XXXXXX /             |%-10p|\n\
 / XXXXXX /              |%-10p|\n\
(________(               `----------'\n\n", gun, &gun->fun_ptr, bullet, bullet + 8, bullet + 12, bullet + 16);
}