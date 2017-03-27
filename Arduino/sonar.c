/*code for the Arduino Uno
Written by Tom Bonar for testing
Sensors being used for this code are the MB10X0 from MaxBotix
All PW inputs are coded in this for simplicity.
Remove the comments to use the additional sensor inputs
*/

const int pwPin1 = 3, pwPin2 = 6, alertPin = 12;
long pulse1, sensor1;

void setup () {
  Serial.begin(9600);
  pinMode(pwPin1, INPUT);
  pinMode(pwPin2, INPUT);
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(alertPin, OUTPUT);

  pinMode(LED_BUILTIN, OUTPUT);
}

void read_sensor(){
  pulse1 = pulseIn(pwPin1, HIGH);
  pulse2 = pulseIn(pwPin2, HIGH);

  sensor1 = pulse1/147;
  sensor2 = pulse2/147;

}

//This section of code is if you want to print the range readings to your computer too remove this from the code put /* before the code section and */ after the code
void printall(){         
  Serial.print("S1");
  Serial.print(" ");
  Serial.print(sensor1);
  Serial.println(" ");
  if(sensor1 < 15 || sensor2 < 15){
    digitalWrite(LED_BUILTIN, HIGH); 
    digitalWrite(alertPin, HIGH); 

  }else{
    digitalWrite(LED_BUILTIN, LOW);   // turn the LED on (HIGH is the voltage level)
    digitalWrite(alertPin, HIGH); 
    
  }
}

void loop () {
  read_sensor();
  printall();
  delay(50); // This delay time changes by 50 for every sensor in the chain.  For 5 sensors this will be 250
}

