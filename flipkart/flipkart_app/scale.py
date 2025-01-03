import serial
import time
import logging
from serial.serialutil import SerialException


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class SerialReader:
    def __init__(self, port: str, baud_rate: int = 9600, timeout: int = 1):

        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial_connection = None

    def connect(self):
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=self.timeout
            )
            time.sleep(2) 
            logging.info(f"Connected to {self.port} at {self.baud_rate} baud.")
        except SerialException as e:
            logging.error(f"Failed to connect to {self.port}: {e}")
            raise

    def read_data(self):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                if self.serial_connection.in_waiting > 0:
                    data = self.serial_connection.readline().decode('utf-8').strip()
                    logging.info(f"Received data: {data}")
                    return data
            except SerialException as e:
                logging.error(f"Error reading data: {e}")
        else:
            logging.warning("Attempted to read data without an open serial connection.")

    def close(self):
        """Close the serial port connection."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            logging.info("Serial connection closed.")

def main():
    port = 'COM4' 
    baud_rate = 9600  

    reader = SerialReader(port=port, baud_rate=baud_rate)
    
    try:
        reader.connect()
        
        while True:
            data = reader.read_data()
            if data:
                logging.info(f"HI scale value: {data}")

    except KeyboardInterrupt:
        logging.info("Interrupted by user. Exiting...")

    except SerialException as e:
        logging.error(f"Serial communication error: {e}")

    finally:
        reader.close()

if __name__ == "__main__":
    main()