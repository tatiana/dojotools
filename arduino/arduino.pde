#define PIN_RED 4
#define PIN_GREEN 2
#define DELAY_TIME 700

void setup(){
    Serial.begin(9600);
    pinMode(PIN_RED, OUTPUT);
    pinMode(PIN_GREEN, OUTPUT);
    digitalWrite(PIN_RED, HIGH);
    digitalWrite(PIN_GREEN, LOW);
}

void turnOffAll(){
    digitalWrite(PIN_GREEN, LOW);
    digitalWrite(PIN_RED, LOW);
}
 
void blinkPin(int pin){
    for (int i = 0; i < 3; i++){
        delay(DELAY_TIME);
        digitalWrite(pin, HIGH);
        delay(DELAY_TIME);
        digitalWrite(pin, LOW);
    }
}


boolean pinIsOn(int pin){
    return digitalRead(pin) == HIGH;
} 
  
void loop(){
    if (Serial.available()){
        char option = Serial.read();
        int pinOn;
        int pinOff;
        boolean shouldBlink = false;
        Serial.begin(9600);
        
        Serial.print(option);
        if (option == 'R'){
            pinOff = PIN_GREEN;
            pinOn = PIN_RED;
        }
        else if (option == 'G'){
            pinOn = PIN_GREEN;
            pinOff = PIN_RED;
        }
        digitalWrite(pinOff, LOW); 
        digitalWrite(pinOn, HIGH);
        
        
    }
}
