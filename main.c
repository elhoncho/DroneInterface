#include <stdio.h>
#include <wiringPiSPI.h>
#include <wiringPi.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdint.h>
#include <termios.h>
#include "wiringPi.h"
#include "MainController.h"

#define SPI_NSS_PIN 3
#define CLKM_PIN 0
#define IRQ_PIN 6
#define SLP_TR_PIN 5
#define RST_PIN 7
#define DIG2_PIN 2

int main(){
//	struct termios term, term_orig;

	AT86RF212B_Open();

//	//Set the STDIN to canonical mode so that one char can be read with read without needing a new line
//	if(tcgetattr(0, &term_orig)) {
//		printf("tcgetattr failed\n");
//		return -1;
//	}
//
//	term = term_orig;
//
//	term.c_lflag &= ~ICANON;
//	term.c_lflag &= ~ECHO;
//	term.c_cc[VMIN] = 0;
//	term.c_cc[VTIME] = 0;
//
//	if (tcsetattr(0, TCSANOW, &term)) {
//		printf("tcsetattr failed\n");
//		return -1;
//	}

	int flags = fcntl(STDIN_FILENO, F_GETFL, 0);
	fcntl(STDIN_FILENO, F_SETFL, flags | O_NONBLOCK);

	MainControllerOpen();

	while(1){
		MainControllerLoop();
	}
}
