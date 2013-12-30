/***************************************************************
 * BE système autonome           							   *
 * Created by Joao VASCONCELOS	 							   *
 * Date: 12/12/2013				 							   *
 *								 							   *
 * File: Init_System.c			 							   *
 * Description: This file contains all system configurations   *
 ***************************************************************/


/***************************************************************
 *
 * INCLUDE FILES
 *
 ***************************************************************/
#include <Init_System.h>

/***************************************************************
 *
 * FUNCTIONS
 *
 ***************************************************************/

void init_System(void)
{
	// Config for system clock (8MHz by internal clock)
	OSCTUNE = 0x00;//0xC0;
	OSCCON = 0x77; 		  // Use internal clock as clock system

	// Enable periodic interruption timeout + enable maskable interrupt 
	T0CON = 0xD8;          //timeout 8bits (8M/4*256 = 7812.5Hz)
	INTCONbits.TMR0IE = 1;
	INTCONbits.GIEH = 1;
	
	// Config Input pins for all IR sensors
	TRISBbits.TRISB7 = 1;
	TRISBbits.TRISB6 = 1;
	TRISBbits.TRISB5 = 1;

	// Config Input pin for ultrason sensor
	TRISBbits.TRISB4 = 1;

	// Config for Serial comm
	// Ports for development board ICD2 leds for tests
	TRISBbits.TRISB0 = 0;
	PORTB = 0;

	// Config for serial communication
	// Ports for USART/UART/serial communication
	TRISCbits.TRISC7 = 0; // RX
	TRISCbits.TRISC6 = 1; // TX	

	// Baudrate config
	BAUDCONbits.BRG16 = 0;	// 8-bit baudrate generator
	BAUDCONbits.ABDEN = 0;	// Disable auto-baud detect
	SPBRG = 0x33;			// 9600 bauds (ERROR = 0.16%)

	// RX register control
	RCSTAbits.SPEN = 1;		// Enable TX and RX as serial port pins
	RCSTAbits.CREN = 0;		// Disable receiver	

	// TX register control
	TXSTAbits.TX9 = 0;		// 8 bits transmission
	TXSTAbits.SYNC = 0;		// Asyschronous mode
	TXSTAbits.BRGH = 1;		// High speed
	TXSTAbits.TXEN = 1; 	// TX enable
}