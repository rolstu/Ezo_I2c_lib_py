class Sequencer1:
    def __init__(self, step1_func, time1):
        """
        Initializes the Sequencer with a step function and time interval.
        :param step1_func: Function to execute at each step.
        :param time1: Time interval between steps in milliseconds.
        """
        self.t1 = time1  # Step time in milliseconds
        self.s1func = step1_func  # Step function
        self.next_step_time = 0  # Time for the next step

    def reset(self):
        """
        Resets the sequencer, so the next step will run immediately.
        """
        self.next_step_time = 0

    def reset_with_delay(self, delay):
        """
        Resets the sequencer with a delay.
        :param delay: Delay before the next step in milliseconds.
        """
        self.next_step_time = int(time.time() * 1000) + delay  # Convert time to milliseconds

    def run(self):
        """
        Executes the step function if the time since the last step has exceeded the interval.
        """
        current_time = int(time.time() * 1000)  # Get current time in milliseconds
        if current_time >= self.next_step_time:
            self.s1func()  # Call the step function
            self.next_step_time = current_time + self.t1  # Schedule the next step

    def set_step1_time(self, time1):
        """
        Updates the time interval for step1.
        :param time1: New time interval in milliseconds.
        """
        self.t1 = time1

    def get_step1_time(self):
        """
        Returns the time interval for step1.
        :return: Time interval in milliseconds.
        """
        return self.t1
