import serial
import time

arduino_port = 'COM4'  # Change this to your Arduino's COM port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # wait for Arduino to initialize

while True:
    command = input("Enter command (1 to turn on, 0 to turn off): ")
    ser.write(command.encode())
    time.sleep(1)  # adjust delay as needed
