
volatile boolean flag=0;
int lightPin=7;   //for digitalRead



void setup()
{
  // put your setup code here, to run once:
  pinMode(7, INPUT);     
  Serial.begin(115200);


  //******************************************
  #define portOfPin(P)\
  (((P)>=0&&(P)<8)?&PORTD:(((P)>7&&(P)<14)?&PORTB:&PORTC))
  #define ddrOfPin(P)\
  (((P)>=0&&(P)<8)?&DDRD:(((P)>7&&(P)<14)?&DDRB:&DDRC))
  #define pinOfPin(P)\
  (((P)>=0&&(P)<8)?&PIND:(((P)>7&&(P)<14)?&PINB:&PINC))
  #define pinIndex(P)((uint8_t)(P>13?P-14:P&7))
  #define pinMask(P)((uint8_t)(1<<pinIndex(P)))

  #define pinAsInput(P) *(ddrOfPin(P))&=~pinMask(P)
  #define pinAsInputPullUp(P) *(ddrOfPin(P))&=~pinMask(P);digitalHigh(P)
  #define pinAsOutput(P) *(ddrOfPin(P))|=pinMask(P)
  #define digitalLow(P) *(portOfPin(P))&=~pinMask(P)
  #define digitalHigh(P) *(portOfPin(P))|=pinMask(P)
  #define isHigh(P)((*(pinOfPin(P))& pinMask(P))>0)
  #define isLow(P)((*(pinOfPin(P))& pinMask(P))==0)
  #define digitalState(P)((uint8_t)isHigh(P))

  //******************************************

  

}

void loop() 
{
  // put your main code here, to run repeatedly:

  unsigned int data;
 
  while(1)
  { 
      data = digitalState(lightPin);
      Serial.print(data);
      delay(25);  
    
  }
  

}

