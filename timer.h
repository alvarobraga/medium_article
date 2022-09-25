#ifndef TIMER_H_
#define TIMER_H_

#include "stm32f4xx.h" //This file is provided by ST and contains the definition of all registers in the STM32F4 family
#include "constants.h"

#define UIF (1U << 0) // Reference Manual page 295 - Mask to read timeout flag

void timer2_2000Hz_interrupt_init(void);

#endif /* TIMER_H_ */
