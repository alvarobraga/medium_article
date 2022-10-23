#ifndef TIMER_H_
#define TIMER_H_

#include "stm32f4xx.h"

#define SAMPLING_SIZE 2000

//#define SAMPLING_SIZE		1000
#define UIF (1U << 0) // Reference Manual page 295 - Mask to read timeout flag

// void timer2_1hz_init(void);
void timer2_1000hz_interrupt_init(void);

#endif /* TIMER_H_ */
