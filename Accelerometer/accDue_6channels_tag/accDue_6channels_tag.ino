/*
 * Hyoyeon Lee 2016.07.15
 * [Reference] code : http://forum.arduino.cc/index.php?topic=137635.5;wap2
 *             atmel: http://www.atmel.com/Images/Atmel-11057-32-bit-Cortex-M3-Microcontroller-SAM3X-SAM3A_Datasheet.pdf
 * [HardWare ] arduino board : Due (ATMEL : SAM3X8E, MainClock=84[MHz])
 *             accelerometer : ADXL001-500z (bw=22[kHz]) on A0~A6
 * [Summary  ] Enable A0(ch7) to A5(ch2) (ADC_CHER:  B11111000) 
 *             Set sps=50[kHz]                (ADC_MR  : prescale=7)
 *             Data with a tag of channel name(ADC_EMR :      tag=1)
 *             Fill the Buffer (uint16_t) with data (4bits(tag)+12bits(data)) 
 *             [(ch2)data (ch3)data...(ch7)data][(ch2)data (ch3)data...(ch7)data]...
 *             Write data to the serial port.
 */
#undef HID_ENABLED

volatile int          n,obufn; //index
   const int channels   =   6; //acc1(x1,y1,z1),acc2(x2,y2,z2)
   const int M = 256*channels; //Size of Buffer (col)
   const int N =   4*channels; //Size of Buffer (row)
    uint16_t     Buffer[N][M];
         
void ADC_Handler() {

    int f = ADC->ADC_ISR;  //Interrupt Status
    if (f & (1 << 27)) {  
                    n =         (n + 1) & 3 ;
        ADC->ADC_RNPR = (uint32_t)Buffer[n] ;
        ADC->ADC_RNCR =                   M ;
    }
    
}

void setup() {

    SerialUSB.begin(0);
    while (!SerialUSB);
    
//--------[Turn On] ADC-clock and Interrupt-----------//
    
    pmc_enable_periph_clk(ID_ADC);
    adc_init(ADC, SystemCoreClock, ADC_FREQ_MAX, ADC_STARTUP_FAST);
    NVIC_EnableIRQ(ADC_IRQn);   

  
//--------[Set ADC] Mode Reg. and Channel-------------//
      
    ADC->ADC_MR     =            503842432 ;//Mode          : Set variables here!!
    ADC->ADC_CHER   =                  252 ;//CHannel Enable: A0~A5(=CH7~CH2)
    ADC->ADC_IDR    =           ~(1 << 27) ;//Interrupt Disable
    ADC->ADC_IER    =             1 << 27  ;//Interrupt Enable
    ADC->ADC_EMR   |=             1 << 24  ;//(Tag)Append channel number
    
//--------[Get Data]Fill the Buffer-------------------//
  
    ADC->ADC_RPR    = (uint32_t) Buffer[0] ;//Receive Pointer
    ADC->ADC_RCR    =                    M ;//Receive Count
    ADC->ADC_RNPR   = (uint32_t) Buffer[1] ;//Next
    ADC->ADC_RNCR   =                    M ;//Next
        n = obufn   =                    1 ;
          
//--------[ADC START]---------------------------------//
  
    ADC->ADC_PTCR   =                    1 ;//Transfer Ctrl
    ADC->ADC_CR     =                    2 ;//Control       : Begin ADC!!!

}

void loop() {
  
  while (n == obufn);
  SerialUSB.write((uint8_t *)Buffer[obufn], 2*M);
  obufn = (obufn + 1) & 3 ;
  
}





