#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <stdbool.h>

const char UwU_NAME[6][16] = {"PiUwUchu" , "CharUwUder", "EvUwU", "UwUduck", "MagiUwU", "KING OF UwU"};
const char *Tips[6][2] = {
	{"--Tips of the day--", "  Do you know, if you try harder, you maybe able to solve the challenge!"},
	{"Today is a good day for hacking!", ""},
	{"--Tips of the day--", "  Do you know, the king of UwU is neither a boy nor girl!"},
	{"--Tips of the day--", "  Do you know, the author of this challenge is really nice!"},
	{"Remember don't wrench the authors!", "All authors are nice guy!"},
	{"--Tips of the day--", "  Do you know, the most dangerous place is the safest place!"}
};
char TEAM[6][16] = {"FirebUwU", "None", "None", "None", "None", "None"};
int TEAM_SIZE = 1;
int MAX_TEAM_SIZE = 6;
int CHOSEN = 1;
char encountered[16];

char buffer1[80];
char buffer2[80];

// Function Prototypes
void print_team();
void edit_nickname();
void play();
void meun();
void print_ui(char*, bool);
void battle_ui1(char*);
void battle_ui2(char*, char*);
void battle_ui3(char*);
void text_box_ui(char*, char*);
void run_away();

void print_team() {
	puts("+-------------------------------------------------------------------------------+");
	for (int i = 0; i < MAX_TEAM_SIZE; i++) {
		printf("| [*] %d: %-70s |\n", i+1, TEAM[i]);
	}
	puts("+-------------------------------------------------------------------------------+");
}

void edit_nickname() {
	int index;
	puts("+---MAIN MENU----------------------------------------------------------UwU------+");
	printf("  Whose nickname do you want to edit? (Please enter an index)\n  ");
	scanf("%d", &index);
	getchar();
	if (index <= TEAM_SIZE) {
		print_ui("menu", true);
		print_team();
		puts("+---MAIN MENU----------------------------------------------------------UwU------+");
		printf("  Please get a new name to %s! What is its new nickname? \n  ", TEAM[index-1]);
		fgets(TEAM[index-1], 16, stdin);
		TEAM[index-1][strcspn(TEAM[index-1], "\n")] = 0;
	}
}

void play() {
	strcpy(encountered, UwU_NAME[rand() % 6]);
	print_ui("battle", true);
	printf("  1: Attack    2: UwUmon    3: UwUball    4. R̵͎̈ṵ̶͊n! \n  ");
	int option;
	scanf("%d", &option);
	getchar();
	switch (option) {
		case 1:
			// system("clear");
			print_ui("attack", false);
			break;
		case 2:
			// system("clear");
			battle_ui2(encountered, TEAM[CHOSEN-1]);
			print_team();
			puts("+----------------------------------------------------------------------UwU------+");
			printf("  Which one do you want to choose? (Please enter an index)\n  ");
			scanf("%d", &CHOSEN);
			if (CHOSEN > 6)
				CHOSEN = 1;

			// system("clear");
			run_away();
			sleep((rand() % 2) + 2);
			break;
		case 3:
			// system("clear");
			battle_ui2(encountered, TEAM[CHOSEN-1]);
			text_box_ui("Firebird used UwUball!", "");
			puts("+----------------------------------------------------------------------UwU------+");
			sleep((rand() % 2) + 1.5);
			if (rand() % 2) {
				if (TEAM_SIZE < 6) {
					// system("clear");
					battle_ui2(encountered, TEAM[CHOSEN-1]);
                    sprintf(buffer1, "Gotcha! %s was caught!", encountered);
					strcpy(buffer2, "");
                    text_box_ui(buffer1, buffer2);
					puts("+----------------------------------------------------------------------UwU------+");
					strcpy(TEAM[TEAM_SIZE], encountered);
					TEAM_SIZE++;
					sleep((rand() % 2) + 2);
				} else {
					// system("clear");
					battle_ui2(encountered, TEAM[CHOSEN-1]);
                    sprintf(buffer1, "Gotcha! %s was caught!", encountered);
                    sprintf(buffer2, "Your team is full! %s will be send to PC!", encountered);
                    text_box_ui(buffer1, buffer2);
					puts("+----------------------------------------------------------------------UwU------+");
					sleep((rand() % 2) + 2);
				}
			} else {
				// system("clear");
				battle_ui2(encountered, TEAM[CHOSEN-1]);
                sprintf(buffer1, "Oh no! %s has escaped!", encountered);
				strcpy(buffer2, "");
                text_box_ui(buffer1, buffer2);
				puts("+----------------------------------------------------------------------UwU------+");
				sleep((rand() % 2) + 2);

				// system("clear");
				run_away();
				sleep((rand() % 2) + 2);
			}
			break;

		default:
			// system("clear");
			battle_ui2(encountered, TEAM[CHOSEN-1]);
			text_box_ui("Ŷ̵̱o̵͓͋u̴̬̇ ̸͓̅c̶̪̒å̵̧n̶͍͌'̷͍͋t̶͕̿ ̷̩͛r̴̠͂u̴̺͝n̵̬̉", "");
			puts("+----------------------------------------------------------------------UwU------+");
			sleep((rand() % 2) + 2);

			// system("clear");
			run_away();
			sleep((rand() % 2) + 2);
	}
}

void meun() {
	bool print_team_flag = false;
	while (1) {
		print_ui("menu", true);
		if (print_team_flag) {
			print_team();
		} else {
			int random_number = (rand() % 6);
			strcpy(buffer1, Tips[random_number][0]);
			strcpy(buffer2, Tips[random_number][1]);
			text_box_ui(buffer1, buffer2);
		}
		print_team_flag = false;
		puts("+---MAIN MENU----------------------------------------------------------UwU------+");
		printf("  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ");
		int option;
		scanf("%d", &option); getchar();
		switch (option) {
			case 1:
				play();
				break;
			case 2:
				print_team_flag = true;
				break;
			case 3:
				print_ui("menu", true);
				print_team();
				edit_nickname();
				break;
			case 0:
				exit(0);
		}
	}
}

int main() {
	srand(time(NULL));
	setvbuf(stdin,NULL,2,0);
	setvbuf(stdout,NULL,2,0);
	setvbuf(stderr,NULL,2,0);
	print_ui("start", true);
	getchar();
	meun();
	return 0;
}

void print_ui(char option[16], bool clear) {
	if (clear) {
		// system("clear");
	}
	if (strcmp(option, "start") == 0) {
        puts("+-------------------------------------------------------------------------------+");
        puts("|                                                                               |");
        puts("|   ________                                _____   ____ ___          ____ ___  |");
        puts("|  /  _____/_____    _____   ____     _____/ ____\\ |    |   \\__  _  _|    |   \\ |");
        puts("| /   \\  ___\\__  \\  /     \\_/ __ \\   /  _ \\   __\\  |    |   /\\ \\/ \\/ /    |   / |");
        puts("| \\    \\_\\  \\/ __ \\|  Y Y  \\  ___/  (  <_> )  |    |    |  /  \\     /|    |  /  |");
        puts("|  \\______  (____  /__|_|  /\\___  >  \\____/|__|    |______/    \\/\\_/ |______/   |");
        puts("|          \\/     \\/      \\/     \\/                                             |");
        puts("|                                                                               |");
        puts("|                                                                               |");
        puts("|                                                                               |");
        puts("|                                                                               |");
        puts("|                                                                               |");
        puts("|                                                                               |");
        puts("|                                                                               |");
        puts("+-------------------------------------------------------------------------------+");
        puts("+----------------------------------------------------------------------UwU------+");
        puts("Press any key to continue...");
    } else if (strcmp(option, "menu") == 0) {
        puts("+-------------------------------------------------------------------------------+");
        puts("|                                                         v        _(    )      |");
        puts("|                                                       v         (___(__)      |");
        puts("|                                                    v v                        |");
        puts("|        _ ^ _                                         v                        |");
        puts("|       '_\\V/ `                                v  v                             |");
        puts("|       ' oX`                                        v                          |");
        puts("|          X                                            v                       |");
        puts("|          X                                                                    |");
        puts("|          X                   +                                  .             |");
        puts("|          X     UwU           A_                                 |\\            |");
        puts("|          X.a#######a.       /\\-\\                                |_\\           |");
        puts("|       .aa##############a   _||\"|_                              __|__          |");
        puts("|    .a############################aa.                           \\   /          |");
        puts("|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|");
        puts("+-------------------------------------------------------------------------------+");
    } else if (strcmp(option, "battle") == 0) {
			battle_ui1(encountered);
            sprintf(buffer1, "Wlid %s appeared!", encountered);
            strcpy(buffer2, "");
            text_box_ui(buffer1, buffer2);
			puts("+----------------------------------------------------------------------UwU------+");
			sleep((rand() % 2) + 2);
			// system("clear");

			battle_ui1(encountered);
            sprintf(buffer1, "Go! %s!", TEAM[CHOSEN-1]);
            strcpy(buffer2, "");
            text_box_ui(buffer1, buffer2);
			puts("+----------------------------------------------------------------------UwU------+");
			sleep((rand() % 2) + 2);
			// system("clear");

			battle_ui2(encountered, TEAM[CHOSEN-1]);
            sprintf(buffer1, "What will %s do?", TEAM[CHOSEN-1]);
            strcpy(buffer2, "");
            text_box_ui(buffer1, buffer2);
			puts("+----------------------------------------------------------------------UwU------+");
    } else if (strcmp(option, "attack") == 0) {
			battle_ui2(encountered, TEAM[CHOSEN-1]);
            sprintf(buffer1, "%s used Try Harder!", TEAM[CHOSEN-1]);
            strcpy(buffer2, "");
            text_box_ui(buffer1, buffer2);
			puts("+----------------------------------------------------------------------UwU------+");
			sleep((rand() % 2) + 2);
			// system("clear");

			battle_ui2(encountered, TEAM[CHOSEN-1]);
			text_box_ui("But it failed!", "");
			puts("+----------------------------------------------------------------------UwU------+");
			sleep((rand() % 2) + 2);
			// system("clear");

			run_away();
			sleep((rand() % 2) + 2);
    }
}

void battle_ui1(char encounter[16]) {
	puts("+-------------------------------------------------------------------------------+");
	printf("| %-15s |                                                             |\n", encounter);
	puts("| Lvl: 1000       |                                              ,,,            |");
	puts("| HP: 100000      |                                             (UwU)           |");
	puts("|-----------------+                                     ----oOO--( )--OOo----   |");
	puts("|                                                                / \\            |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                             +-----------------|");
	puts("|                                                             |                 |");
	puts("|                                                             |                 |");
	puts("|                                                             |                 |");
	puts("+-------------------------------------------------------------------------------+");
}

void battle_ui2(char encounter[16], char team[16]) {
	puts("+-------------------------------------------------------------------------------+");
	printf("| %-15s |                                                             |\n", encounter);
	puts("| Lvl: 1000       |                                              ,,,            |");
	puts("| HP: 100000      |                                             (UwU)           |");
	puts("|-----------------+                                     ----oOO--( )--OOo----   |");
	puts("|                                                                / \\            |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|   +-------+                                                                   |");
	puts("|   | o   o |                                                 +-----------------|");
	printf("|   |  www  |                                                 | %-15s |\n", team);
	puts("|   +-------+                                                 | Lvl: 1          |");
	puts("|                                                             | HP: 10          |");
	puts("+-------------------------------------------------------------------------------+");
}

void battle_ui3(char team[16]) {
	puts("+-------------------------------------------------------------------------------+");
	puts("|                 |                                                             |");
	puts("|                 |                                                             |");
	puts("|                 |                                                             |");
	puts("|-----------------+                                                             |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|   +-------+                                                                   |");
	puts("|   | o   o |                                                 +-----------------|");
	printf("|   |  www  |                                                 | %-15s |\n", team);
	puts("|   +-------+                                                 | Lvl: 1          |");
	puts("|                                                             | HP: 10          |");
	puts("+-------------------------------------------------------------------------------+");
}

void text_box_ui(char text1[77], char text2[77]) {
	puts("+-------------------------------------------------------------------------------+");
	printf("| %-77s |\n", text1);
	printf("| %-77s |\n", text2);
	puts("+-------------------------------------------------------------------------------+");
}

void run_away() {
	battle_ui3(TEAM[CHOSEN-1]);
    sprintf(buffer1, "%s ran away!", encountered);
    strcpy(buffer2, "");
    text_box_ui(buffer1, buffer2);
	puts("+----------------------------------------------------------------------UwU------+");
}

// This function is used to make sure the binary 
// work the same as the binary with "system(clear);"
void debug() {
	system("");
}