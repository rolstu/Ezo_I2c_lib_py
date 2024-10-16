import smbus2
import time

class EzoBoard:
    # Define error codes as class constants
    SUCCESS = 1
    FAIL = 2
    NOT_READY = 254
    NO_DATA = 255
    NOT_READ_CMD = 3

    def __init__(self, address, name=None, bus=1):
        """
        Initialize the EzoBoard object.

        :param address: I2C address of the device
        :param name: Optional name for the device
        :param bus: I2C bus number (default is bus 1)
        """
        self.i2c_address = address
        self.name = name
        self.bus = smbus2.SMBus(bus)  # Use smbus2 to communicate via I2C
        self.issued_read = False
        self.reading = 0.0
        self.error = EzoBoard.SUCCESS
        self.bufferlen = 32  # Default buffer length

    def get_name(self):
        """
        Get the name of the EzoBoard object.

        :return: Name of the device
        """
        return self.name

    def set_name(self, name):
        """
        Set the name of the EzoBoard object.

        :param name: New name to set
        """
        self.name = name

    def get_address(self):
        """
        Get the I2C address of the EzoBoard.

        :return: I2C address of the device
        """
        return self.i2c_address

    def set_address(self, address):
        """
        Set the I2C address of the EzoBoard.

        :param address: New I2C address to set
        """
        self.i2c_address = address

    def send_cmd(self, command):
        """
        Send a command to the EzoBoard over I2C.

        :param command: Command to send as a string
        """
        try:
            self.bus.write_i2c_block_data(self.i2c_address, 0, list(command.encode('utf-8')))
            self.issued_read = False
        except OSError:
            self.error = EzoBoard.FAIL

    def send_read_cmd(self):
        """
        Send the 'r' command to the EzoBoard to request a reading.
        """
        self.send_cmd('r')
        self.issued_read = True

    def send_cmd_with_num(self, cmd, num, decimal_amount=3):
        """
        Send a command with a number appended to it.

        :param cmd: Command as a string
        :param num: Number to append
        :param decimal_amount: Number of decimal places to include
        """
        temp = f"{cmd}{num:.{decimal_amount}f}"
        self.send_cmd(temp)

    def send_read_with_temp_comp(self, temperature):
        """
        Send a temperature compensated read command.

        :param temperature: Temperature value to send
        """
        self.send_cmd_with_num('rt,', temperature, 3)
        self.issued_read = True

    def receive_read_cmd(self):
        """
        Receive the read response from the EzoBoard.

        :return: Error code
        """
        sensor_data = [0] * self.bufferlen
        self.error = self.receive_cmd(sensor_data, self.bufferlen)

        if self.error == EzoBoard.SUCCESS:
            if not self.issued_read:
                self.error = EzoBoard.NOT_READ_CMD
            else:
                self.reading = float(''.join(map(chr, sensor_data)).strip('\x00'))

        return self.error

    def is_read_poll(self):
        """
        Check if the board is waiting for a read response.

        :return: True if a read response is expected, False otherwise
        """
        return self.issued_read

    def get_last_received_reading(self):
        """
        Get the last reading received from the EzoBoard.

        :return: The last reading as a float
        """
        return self.reading

    def get_error(self):
        """
        Get the last error code from the EzoBoard.

        :return: Error code
        """
        return self.error

    def receive_cmd(self, sensor_data_buffer, buffer_len):
        """
        Receive a command response from the EzoBoard.

        :param sensor_data_buffer: Buffer to store the received data
        :param buffer_len: Length of the buffer
        :return: Error code
        """
        try:
            data = self.bus.read_i2c_block_data(self.i2c_address, 0, buffer_len)
            code = data[0]
            sensor_data_buffer[:len(data) - 1] = data[1:]

            if code == EzoBoard.SUCCESS:
                self.error = EzoBoard.SUCCESS
            elif code == EzoBoard.FAIL:
                self.error = EzoBoard.FAIL
            elif code == EzoBoard.NOT_READY:
                self.error = EzoBoard.NOT_READY
            elif code == EzoBoard.NO_DATA:
                self.error = EzoBoard.NO_DATA

        except OSError:
            self.error = EzoBoard.FAIL

        return self.error
