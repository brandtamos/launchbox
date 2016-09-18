/*
Rocket Launch indicator
 */

#include <Servo.h>
#include <SoftwareSerial.h>
 

const int MINSERVOPOS = 60;
const int MAXSERVOPOS = 140;
const int SERVOPIN = 9;

Servo myservo;
//SoftwareSerial BT(10, 11);

int servopos = MINSERVOPOS;
String command;

int loopCount = 0;
void setup() {
  Serial.begin(9600);
  //init servo
  myservo.attach(SERVOPIN);
  setServoToStartPosition();
}

void loop() {
  /*if(Serial.available()){
    command = Serial.readString();
    Serial.println("got command:" + command);
  }*/

  if(Serial.available()){
    command = Serial.readString();
    Serial.println("got command: " + command);
  }
  if(command == "launch"){
    actuateServo();
    command = "";
  }

}
void setServoToStartPosition(){
  pinMode(SERVOPIN, OUTPUT);
  myservo.write(MINSERVOPOS);              // tell servo to go to position in variable 'pos'
  delay(200);                       // waits 15ms for the servo to reach the position
  pinMode(SERVOPIN, INPUT);
}

void actuateServo(){
  //activate servo pin
  pinMode(SERVOPIN, OUTPUT);
  for (servopos = MINSERVOPOS; servopos <= MAXSERVOPOS; servopos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(servopos);              // tell servo to go to position in variable 'pos'
    delay(25);                       // waits 15ms for the servo to reach the position
  }
  delay(2000);
  for (servopos = MAXSERVOPOS; servopos >= MINSERVOPOS; servopos -= 1) { // goes from 180 degrees to 0 degrees
    myservo.write(servopos);              // tell servo to go to position in variable 'pos'
    delay(25);                       // waits 15ms for the servo to reach the position
  }
  // this effectively turns the servo off to prevent servo buzzing
  pinMode(SERVOPIN, INPUT);
}

