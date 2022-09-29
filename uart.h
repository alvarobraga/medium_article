#ifndef UART_H_
#define UART_H_

#include <stdio.h>
#include <stdint.h>
#include "stm32f4xx.h"

void uart2_tx_init(void);
void uart2_write(int ch);

#endif /* UART_H_ */
