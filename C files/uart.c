#include "uart.h"

#define GPIOAEN (1U << 0)  // Enable clock to GPIOA
#define UART2EN (1U << 17) /*Reference Manual, page 118 - Mask to enable clock \
                             to the USART2 module*/
#define SYS_FREQ 16000000  // Default system clock speed
#define APB1_CLK SYS_FREQ
#define UART_BAUDRATE 115200
#define TE (1U << 3)  /*Reference Manual, page 552 - Mask to enable transmitter*/
#define UE (1U << 13) /*Reference Manual, page 551 - Mask to enable USART*/
#define TXE (1U << 7) /*Reference Manual, page 548 - Mask to check if Transmit Data register \
                        is empty*/

static void uart_set_baudrate(USART_TypeDef *USARTx, uint32_t PeriphClk, uint32_t BaudRate);
static uint16_t compute_uart_baudrate(uint32_t PeriphClk, uint32_t BaudRate);

int stdout_putchar(int ch)
{
    uart2_write(ch);
    return ch;
}

void uart2_tx_init(void)
{
    /*********** Configure UART2 GPIO pin *************/
    /*Enable clock access to GPIOA*/
    RCC->AHB1ENR |= GPIOAEN;

    /*Set PA2 mode to alternate function mode - set bit 4 to 0 and bit 5 to 1*/
    GPIOA->MODER &= ~(1U << 4);
    GPIOA->MODER |= (1U << 5);

    /*Set PA2 alternate function type to UART_TX (AF07) - the AFR member of the structure GPIOA
     is an array of size two. The index 0 is to configure AFRL and the index 1 is to configure
     AFRH*/
    GPIOA->AFR[0] |= (1U << 8);
    GPIOA->AFR[0] |= (1U << 9);
    GPIOA->AFR[0] |= (1U << 10);
    GPIOA->AFR[0] &= ~(1U << 11);

    /*********** Configure UART2 module *************/
    /*Enable clock access to UART2*/
    RCC->APB1ENR |= UART2EN;

    /*Configure baudrate*/
    uart_set_baudrate(USART2, APB1_CLK, UART_BAUDRATE);

    /*Configure transfer direction*/
    USART2->CR1 = TE; // By making "equals to", all bits of the register are set to 0 apart from bit 3

    /*Enable UART2 module*/
    USART2->CR1 |= UE;
}

void uart2_write(int ch)
{
    /*Make sure the transmit data register is empty*/
    while (!(USART2->SR & TXE))
        ;

    /*Write to transmit data register*/
    USART2->DR = (ch & 0xFF); // The AND with 0xFF is to transmit 8 bits
}

static void uart_set_baudrate(USART_TypeDef *USARTx, uint32_t PeriphClk, uint32_t BaudRate)
{
    USARTx->BRR = compute_uart_baudrate(PeriphClk, BaudRate); // BRR: baud rate register - Reference Manual pg. 550
}

static uint16_t compute_uart_baudrate(uint32_t PeriphClk, uint32_t BaudRate)
{
    return ((PeriphClk + (BaudRate / 2U)) / BaudRate);
}
