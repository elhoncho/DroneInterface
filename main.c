#include <stdio.h>
#include <wiringPiSPI.h>
#include <wiringPi.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdint.h>
#include <termios.h>
#include "wiringPi.h"
#include "AT86RF212B/Inc/MainController.h"
#include "AT86RF212B/Inc/AT86RF212B.h"

#define SPI_NSS_PIN 3
#define CLKM_PIN 0
#define IRQ_PIN 6
#define SLP_TR_PIN 5
#define RST_PIN 7
#define DIG2_PIN 2

int main(){
	AT86RF212B_Open();

	int flags = fcntl(STDIN_FILENO, F_GETFL, 0);
	fcntl(STDIN_FILENO, F_SETFL, flags | O_NONBLOCK);

	MainControllerOpen();

	while(1){
		MainControllerLoop();
	}
}
