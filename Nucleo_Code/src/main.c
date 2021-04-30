/**
  ******************************************************************************
  * @file    main.c
  * @author  Zachary Ellis
  * @version V1.0
  * @date    4/09/21
  * @brief   Battery Test Rig software test on nucleo dev board
  ******************************************************************************
*/


#include "stm32l4xx.h"
//#include "stm32l4xx_nucleo_32.h"
#include <stdio.h> // for printf()

int simple_putchar(int arg){
	while(!(USART1->ISR & USART_ISR_TXE)) ;
	USART1->TDR = arg;
	return arg;
}


int better_putchar(int arg){
	while(!(USART1->ISR & USART_ISR_TXE)) ;
	if(arg == '\n'){
		USART1->TDR = '\r';
	}
	while(!(USART1->ISR & USART_ISR_TXE)) ;
	USART1->TDR = arg;
	return arg;
}

int __io_putchar(int ch) {
	return simple_putchar(ch);
}

struct ADC_Samples_t{
	int discharge_curr;
	int charge_curr;
	int dut_volt;
};

void init_ADC(void) {
	RCC->AHB2ENR |= RCC_AHB2ENR_GPIOAEN;
	GPIOA->MODER |= GPIO_MODER_MODER0 | GPIO_MODER_MODER1; //Enable PA0, PA1 for ADC
	RCC->AHB2ENR |= RCC_AHB2ENR_GPIOBEN;
	GPIOB->MODER |= GPIO_MODER_MODER0;
	RCC->AHB2ENR |= RCC_AHB2ENR_ADCEN; //Enable PB0 for ADC (not exposed on dev board but I don't care)
	ADC1->SQR1 |= ADC_SQR1_L_0 | ADC_SQR1_L_1; //three channels in sequence
	ADC1->SQR1 |= ADC_SQR1_SQ1_0 | ADC_SQR1_SQ1_2; //ADC1_IN5
	ADC1->SQR1 |= ADC_SQR1_SQ2_1 | ADC_SQR1_SQ2_2; //ADC1_IN6
	ADC1->SQR1 |= ADC_SQR1_SQ3_0 | ADC_SQR1_SQ3_1 | ADC_SQR1_SQ3_2 | ADC_SQR1_SQ3_3; //ADC1_IN15
	ADC1->CR &= ~ADC_CR_DEEPPWD;        //exit ADC deep power down state
	ADC1->CR |= ADC_CR_ADVREGEN;        //enable the ADC voltage regulator
	while(!(ADC1->CR & ADC_CR_ADVREGEN)); //wait for the voltage regulator to be ready
	ADC1->CR |= ADC_CR_ADCAL;             //perform ADC calibration
	while(ADC1->CR & ADC_CR_ADCAL);       //wait for calibration to be complete
	ADC1->CR |= ADC_CR_ADEN;            //enable ADC
	while(!(ADC1->ISR & ADC_ISR_ADRDY));//wait for ADC to be ready
}

struct ADC_Samples_t get_ADC_samples(void){
	volatile struct ADC_Samples_t samples; //don't know if volatile is needed here but we are writing the struct in a weird way
	samples.charge_curr = 0x69;
	samples.discharge_curr = 0x69;
	samples.dut_volt = 0x69;
	int* place;
	place = (void*)&samples;  //address to store sample
	while(!(ADC1->ISR & ADC_ISR_ADRDY)); //wait for ADC to be ready
	ADC1->CR |= ADC_CR_ADSTART;          //start conversion
	for(int i=0; i < sizeof(samples) / sizeof(int); i++){
		while(!(ADC1->ISR & ADC_ISR_EOC));
		*place = ADC1->DR; //store sample in the value at the address
		place ++; //increment the address
	}
	ADC1->CR |= ADC_CR_ADSTP; //stop any ongoing conversions. probably don't need this but whatevs
	while(ADC1->CR & ADC_CR_ADSTART); //make sure things actually stop
	return samples;
}

void init_UART(){
	RCC->AHB2ENR |= RCC_AHB2ENR_GPIOAEN;
	GPIOA->MODER &= ~GPIO_MODER_MODER9 & ~GPIO_MODER_MODER10;
	GPIOA->MODER |= GPIO_MODER_MODER9_1 | GPIO_MODER_MODER10_1;
	GPIOA->AFR[1] &= ~GPIO_AFRH_AFSEL9 & ~GPIO_AFRH_AFSEL10;
	GPIOA->AFR[1] |= (7 << GPIO_AFRH_AFSEL9_Pos) | (7 << GPIO_AFRH_AFSEL10_Pos);

	RCC->CR = 0;
	RCC->CR |= 0xA << RCC_CR_MSIRANGE_Pos;
	RCC->CR |= RCC_CR_MSION | RCC_CR_MSIRDY | RCC_CR_MSIPLLEN | RCC_CR_MSIRGSEL;

	RCC->APB2ENR |= RCC_APB2ENR_USART1EN;
	USART1->CR1 &= ~USART_CR1_UE;
	USART1->CR1 &= ~USART_CR1_M & ~(1<<28);
	USART1->CR2 &= ~USART_CR2_STOP;
	USART1->CR1 &= ~USART_CR1_PS;
	USART1->CR1 &= ~USART_CR1_OVER8;
	USART1->BRR = 0x116;
	USART1->CR1 |= USART_CR1_TE | USART_CR1_RE;
	USART1->CR1 |= USART_CR1_UE;
	while(!(USART1->ISR & (USART_ISR_TEACK | USART_ISR_REACK))) ;
}

void setup_tim6(){
	RCC->APB1ENR1 |= RCC_APB1ENR1_TIM6EN;
	TIM6->PSC = 24000-1;
	TIM6->ARR = 200-1;
	TIM6->DIER |= TIM_DIER_UIE;
	NVIC->ISER[1] |= 1 << (TIM6_IRQn - 32);
	//TIM6->CR1 |= TIM_CR1_ARPE;
	TIM6->CR1 |= TIM_CR1_CEN;
}

void TIM6_IRQHandler(){
	TIM6->SR &= ~TIM_SR_UIF;

	struct ADC_Samples_t samples;
	samples = get_ADC_samples();
	char buffer[10];
	sprintf(buffer, "\r%04d", samples.charge_curr);
	printf(buffer);
}

int main(void)
{
	setbuf(stdin,0);
	setbuf(stdout,0);
	//init_DAC(); No DAC on dev board version chip. DAC is easy to use however
	init_ADC();
	init_UART();
	setup_tim6();

}
