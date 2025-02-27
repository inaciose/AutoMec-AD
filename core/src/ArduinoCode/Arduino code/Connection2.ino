// Escrever no monitor serial o angulo das rodas (-30 até 30) junto da da percentagem de potencia do motor (0-100) como nos exemplos
// ex1:"-30000" ; ex2:"030100"
// PS: Colocar 3 caracteres para o angulo e 3 para a velocidade!!!


#if defined(ARDUINO) && ARDUINO >= 100  // ROS libraries
  #include "Arduino.h"
#else
  #include <WProgram.h>
#endif
#include <ros.h>
#include <std_msgs/Int16.h>
#include <std_msgs/String.h>

#include <Servo.h>

ros::NodeHandle  nh;                    // Creating a ROS node

String readString, servo1, servo2;
Servo myservo1;
Servo myservo2;

void servo_cb( const std_msgs::Int16 & cmd_msg){
  //servo.write(cmd_msg.data); //set servo angle, should be from 0-180  
  //digitalWrite(LED_BUILTIN, HIGH-digitalRead(LED_BUILTIN));  //toggle led  
  }



ros::Subscriber<std_msgs::Int16> sub("servo", servo_cb);  //Defining the subscriber

void setup() {
  nh.initNode();               // Initiating the node
  nh.subscribe(sub);           // Subscribing to the previously defined subscriber
  
  //Serial.begin(9600);
  myservo1.attach(7,-60,120);  //the pin for the servo control
  myservo2.attach(8,90,150);
  //myservo1.write(0);
  //myservo2.write(0);
  myservo1.writeMicroseconds(500);
  myservo1.writeMicroseconds(500);
  
  //Serial.println("servo-test-21"); // so I can keep track of what is loaded

  
}

void loop() {

  //while (Serial.available()) {
   // delay(1); 
   // if (Serial.available() >0) {
   //   char c = Serial.read();  //gets one byte from serial buffer
   //   readString += c; //makes the string readString

    nh.spinOnce();                      // Executes all ROS callbacks with a delay of one milisecond
    delay(1);
   
    }


if (readString.length() >0) {
      Serial.println(readString); //see what was received
     
      // expect a string like 07002100 containing the two servo positions     
      servo1 = readString.substring(0, 2); //get the first four characters
      servo2 = readString.substring(3, 5); //get the next four characters
     
      Serial.println(servo1);  //print to serial monitor to see results
      Serial.println(servo2);
     
      int n1; //declare as number 
      int n2;
     
      char carray1[6]; //magic needed to convert string to a number
      servo1.toCharArray(carray1, sizeof(carray1));
      n1 = atoi(carray1);
      n1=map(n1,0,100,-60,120);
     
      char carray2[6];
      servo2.toCharArray(carray2, sizeof(carray2));
      n2 = atoi(carray2);
      n2 = map(n2,0,100,90,150);
    
    Serial.println(n1);
    Serial.println(n2);
    myservo1.write(n1); //set servo position
    myservo2.write(n2);
    readString="";
  }
