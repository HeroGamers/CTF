#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <stdio.h>

#include "gun_t.h"

int my_aim(const char* str) {
    puts(str);
    return 0;
}

struct gun_t *gun;
char *bullet;

int main()
{
  char line[128];
  gunDefault(gun);

  char* command1 = "init";
  char* command2 = "load";
  char* command3 = "reload";
  char* command4 = "shoot";

  while(1) {
    printf("\033[1m %s [gun name] \033[0m take out mag \033[1m %s <ammo> \033[0m load mag with ammo \033[1m %s \033[0m load and reset \033[1m %s \033[0m aim and shoot\n\n", command1, command2, command3, command4);

    if(fgets(line, sizeof(line), stdin) == NULL) break;
    
    // init: take out mag and give gun a name
    if(strncmp(line, command1, sizeof(command1)) == 0) {
      gun = malloc(sizeof(struct gun_t));
      gun->fun_ptr = my_aim;
      if(strlen(line + sizeof(command1)) < 32) {
        strcpy(gun->name, line + sizeof(command1));
      }
      gunTakeOutMag(gun, bullet);
      puts("Mag out..");
    }

    // load: load mag with ammo
    if(strncmp(line, command2, sizeof(command3)) == 0) {
      if (gun) {
        bullet = strdup(line + sizeof(command3) - 1);
        gunLoadMag(gun, bullet);
        puts("Mag loaded..");
      } else {
        puts("Please take magasin out first!\n");
      }
    }

    // reload: load and reset
    if(strncmp(line, command3, sizeof(command2)) == 0) {
      free(gun);
      gunDefault(gun);
      puts("Gun reset..");
    }

    // shoot: aim and shoot
    if(strncmp(line, command4, sizeof(command4)) == 0) {
      if (gun && bullet) {
        gunShoot(gun);
        (*gun->fun_ptr)("cat flag.txt");
      } else {
        puts("Please load gun..");
      }
    }
  }
}