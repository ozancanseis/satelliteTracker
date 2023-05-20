#include <Servo.h>

Servo horizontalServo; 
Servo verticalServo;


const byte numChars = 64;
char receivedChars[numChars];

boolean newData = false;

int horizontal = 0; 
int vertical = 0;

void setup() {
  horizontalServo.attach(9);
  verticalServo.attach(10);

  Serial.begin(9600);

}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void loop() {
  recvWithStartEndMarkers();
  if (newData) {
    horizontal = atoi(&receivedChars[0]);
    newData = false;
    horizontalServo.write(horizontal);
  }

  recvWithStartEndMarkers();
  if (newData) {
    vertical = atoi(&receivedChars[0]);
    newData = false;
    verticalServo.write(vertical);
  }
}
