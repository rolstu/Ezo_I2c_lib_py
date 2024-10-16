def print_device_info(device):
    """
    Prints the device name and I2C address.
    
    :param device: The EzoBoard object
    """
    print(f"{device.get_name()} {device.get_address()}")


def print_success_or_error(device, success_string):
    """
    Prints a success message or an error message based on the device's last command response.
    
    :param device: The EzoBoard object
    :param success_string: The message to print if the command was successful
    """
    error = device.get_error()
    if error == EzoBoard.SUCCESS:
        print(success_string)
    elif error == EzoBoard.FAIL:
        print("Failed")
    elif error == EzoBoard.NOT_READY:
        print("Pending")
    elif error == EzoBoard.NO_DATA:
        print("No Data")
    elif error == EzoBoard.NOT_READ_CMD:
        print("Not Read Cmd")


def receive_and_print_response(device):
    """
    Receives the response from the device and prints it.
    
    :param device: The EzoBoard object
    """
    receive_buffer = ['\x00'] * 32  # Buffer to hold the response
    device.receive_cmd(receive_buffer, 32)  # Get the response

    print_success_or_error(device, " - ")  # Print the success/error message
    print_device_info(device)  # Print the device name and address
    print(f": {''.join(receive_buffer).strip()}")  # Print the actual response


def receive_and_print_reading(device):
    """
    Receives the reading from the device and prints it.
    
    :param device: The EzoBoard object
    """
    print(f"{device.get_name()}: ", end="")
    device.receive_read_cmd()  # Get the reading

    # Print the reading or an error message
    reading = f"{device.get_last_received_reading():.2f}"
    print_success_or_error(device, reading)
