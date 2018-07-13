#include <Servo.h>
Servo myservo1;  

int  serIn;             // var that will hold the bytes-in read from the serialBuffer
char serInString[100];  // array that will hold the different bytes  100=100characters;
                        // -> you must state how long the array will be else it won't work.
int  serInIndx  = 0;    // index of serInString[] in which to insert the next incoming byte
int  serOutIndx = 0;    // index of the outgoing serInString[] array;

Servo myServos[3];


#define arr_len( x )  ( sizeof( x ) / sizeof( *x ) )
 

void setup() {  
  // put your setup code here, to run once:
  
  int numServos = arr_len( myServos );  
  for(int i=0; i<numServos; i++)
  {
    myServos[i].attach(i+9);
  } 
  
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.println("Hello World");

  delay(500);
  readSerialString();

  processReceivedString();
}



//read a string from the serial and store it in an array
//this func uses globally set variable so it's not so reusable
//I need to find the right syntax to be able to pass to the function 2 parameters:
// the stringArray and (eventually) the index count
void readSerialString () {
    int sb;   
    if(Serial.available()) { 
       //Serial.print("reading Serial String: ");     //optional confirmation
       while (Serial.available()){ 
          sb = Serial.read();             
          serInString[serInIndx] = sb;
          serInIndx++;
          //serialWrite(sb);                        //optional confirmation
       }
       //Serial.println();
    }  
}

//print the string all in one time
//this func as well uses global variables
void processReceivedString() {
  if( serInIndx > 0) { 
    char* command = strtok(serInString, "&");
    while (command != 0)
    {
        // Split the command in two values
        char* separator = strchr(command, ':');
        if (separator != 0)
        {
            // Actually split the string in 2: replace ':' with 0
            *separator = 0;
            int servoId = atoi(command);
            ++separator;
            int position = atoi(separator);

            Serial.print("Servo: "); 
            Serial.print(servoId); 
            Serial.print("  Pos: "); 
            Serial.print(position); 
            Serial.println(""); 

            myServos[servoId].write(position);              
        }
        // Find the next command in input string
        command = strtok(0, "&");
    }
    
    //reset all the functions to be able to fill the string back with content
    serOutIndx = 0;
    serInIndx  = 0;
    Serial.println();
  }

}

