int outPin = 13;
int inFiringPin = 2;
int inOverridePin = 3;
//int maxVal = 3100; 
//int minVal = 1100; 

boolean firing = false;
boolean overriding = false;
unsigned int pulseRep = 20000; //=20 ms

//test values for PWM ~ angle
//unsigned int fireAngle = 1000; //times in microseconds
//unsigned int nofireAngle = 18800;

//operational values for PWM ~ angle
unsigned int fireAngle = 2800; //times in microseconds
unsigned int nofireAngle = 2000;

unsigned long fireTime   =    4000000;
//unsigned long nofireTime =    2000000;
unsigned long overrideTime = 30000000;

unsigned long stateTime = 0;

void setup(){
  pinMode(outPin, OUTPUT);
  pinMode(inFiringPin, INPUT);
  digitalWrite(inFiringPin, HIGH);
  pinMode(inOverridePin, INPUT);
  digitalWrite(inOverridePin, HIGH);
}

void loop(){
  if ( firing ){
    pulseRep_us ( fireAngle );
  }
  else {
    pulseRep_us ( nofireAngle);
  }
  
  stateTime += pulseRep;

  if (digitalRead(inOverridePin) == HIGH ) {
    overriding = true;
    firing = false;
    stateTime = 0;
  }
  if (!overriding && digitalRead(inFiringPin) == HIGH ) {
     firing = true;
     stateTime = 0;
  }
  
  if ( overriding && (stateTime > overrideTime)){
    overriding = false;
    stateTime = 0;
  }
  if ( firing && (stateTime > fireTime) ){
    firing = false;
    stateTime = 0;
  }

}


void pulseRep_us ( unsigned int highT){
   digitalWrite(outPin, HIGH);
  delayMicroseconds( highT );
   digitalWrite(outPin, LOW);
  delayMicroseconds( pulseRep - highT );
}


