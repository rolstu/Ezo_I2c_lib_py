import time
from ezo_i2c_util import receive_and_print_response, print_device_info

def receive_command():
    if input_available():  # Assuming a function to check if input is available
        string_buffer = input()  # Replace Serial.readString() with input()
        print("> " + string_buffer)
        string_buffer = string_buffer.upper().strip()  # Convert to uppercase and remove spaces/newlines
        return string_buffer
    return None

def input_available():
    # This function should check if there is input available.
    # In place of 'Serial.available()' use any method depending on your environment
    return True

def select_delay(command):
    if "CAL" in command or "R" in command:
        time.sleep(1.2)  # 1200ms delay
    else:
        time.sleep(0.3)  # 300ms delay

def process_command(string_buffer, device_list, default_board):
    if string_buffer == "LIST":
        list_devices(device_list, default_board)
    elif string_buffer.startswith("ALL:"):
        cmd = string_buffer.split(':')[1]  # Extract the command after "ALL:"
        for device in device_list:
            device.send_cmd(cmd)

        select_delay(cmd)

        for device in device_list:
            receive_and_print_response(device)

    elif string_buffer:
        index = string_buffer.find(':')
        if index != -1:
            name_to_find = string_buffer[:index].upper().strip()
            cmd = string_buffer[index + 1:]

            addr_found = False
            for device in device_list:
                if name_to_find == device.get_name():
                    default_board = device
                    addr_found = True
                    break

            if addr_found:
                default_board.send_cmd(cmd)
            else:
                print(f"No device named {name_to_find}")
                return
        else:
            default_board.send_cmd(string_buffer)

        if string_buffer != "SLEEP":
            select_delay(string_buffer)
            receive_and_print_response(default_board)

def list_devices(device_list, default_board):
    for device in device_list:
        if device == default_board:
            print("--> ", end="")
        else:
            print(" - ", end="")
        print_device_info(device)
        print("")

def iot_cmd_print_listcmd_help():
    print("list              prints the names and addresses of all the devices in the")
    print("                  device list, with an arrow pointing to the default board")

def iot_cmd_print_allcmd_help():
    print("all:[query]       sends a query to all devices in the device list, and")
    print("                  prints their responses")

def iot_cmd_print_namedquery_help():
    print("[name]:[query]    sends a query to the device with the name [name], and")
    print("                  makes that device the default board")
    print("                      ex: PH:status sends a status query to the device")
    print("                      named PH")
