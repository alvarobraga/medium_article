#include "timer.h"

#define EN (1U << 0)  // Reference Manual page 118 - Mask to enable clock to Timer 2
#define CEN (1U << 0) // Reference Manual page 287 - Mask to enable Timer 2

/*Timer Interruption*/
#define UIE (1U << 0) /* Reference Manul page 293 - Mask to read Update Interrupt (UIE) of \
								the TIM2_DIER (Interrupt Enable Register)*/

#define PSC_VALUE(N) (int)16000000 / (1000 * N)

void timer2_1000hz_interrupt_init(void)
{
	/*Enable clock access to timer2*/
	RCC->APB1ENR |= EN;

	/*Configure timer to sample at 500Hz*/
	/*Set prescaler value*/
	TIM2->PSC = (PSC_VALUE((SAMPLING_SIZE)) - 1); // PSC_VALUE((SAMPLING_SIZE)) = 8 --->
												  //  therefore 16,000,000 / 8 = 2,000,000

	/*Set auto-reload value*/
	TIM2->ARR = (1000 - 1); // 2,000,000 / 1,000 = 2000Hz --> 2000 samples/second

	/*Clear counter*/
	TIM2->CNT = 0;

	/*Enable timer*/
	TIM2->CR1 |= CEN;

	/*Enable Timer interrupt*/
	TIM2->DIER |= UIE;

	/*Enable Timer interrupt in NVIC - Nested Vector Interrup Controller*/
	NVIC_EnableIRQ(TIM2_IRQn);
}