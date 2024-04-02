const int ledPin = 11; // LED connected to digital pin 13

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud
  pinMode(ledPin, OUTPUT); // Set the LED pin as an output
}

void loop() {
  if (Serial.available() > 0) { // If data is available to read
    char receivedChar = Serial.read(); // Read the incoming byte
    if (receivedChar == '1') {
      digitalWrite(ledPin, HIGH); // Turn on the LED
      Serial.println("LED ON");
    } else if (receivedChar == '0') {
      digitalWrite(ledPin, LOW); // Turn off the LED
      Serial.println("LED OFF");
    }
  }
}
