class Sequencer3:
    class ReadingStep:
        STEP1 = 1
        STEP2 = 2
        STEP3 = 3

    def __init__(self, step1_func, time1, step2_func, time2, step3_func, time3):
        """
        Initializes the Sequencer with three step functions and their respective time intervals.
        :param step1_func: Function to execute at step 1.
        :param time1: Time interval for step 1 in milliseconds.
        :param step2_func: Function to execute at step 2.
        :param time2: Time interval for step 2 in milliseconds.
        :param step3_func: Function to execute at step 3.
        :param time3: Time interval for step 3 in milliseconds.
        """
        self.t1 = time1  # Time for step 1
        self.t2 = time2  # Time for step 2
        self.t3 = time3  # Time for step 3
        self.s1func = step1_func  # Step 1 function
        self.s2func = step2_func  # Step 2 function
        self.s3func = step3_func  # Step 3 function
        self.current_step = self.ReadingStep.STEP1  # Start with step 1
        self.next_step_time = 0  # Time for the next step

    def set_step1_time(self, time):
        """
        Updates the time interval for step 1.
        :param time: New time interval for step 1 in milliseconds.
        """
        self.t1 = time

    def set_step2_time(self, time):
        """
        Updates the time interval for step 2.
        :param time: New time interval for step 2 in milliseconds.
        """
        self.t2 = time

    def set_step3_time(self, time):
        """
        Updates the time interval for step 3.
        :param time: New time interval for step 3 in milliseconds.
        """
        self.t3 = time

    def get_step1_time(self):
        """
        Returns the time interval for step 1.
        :return: Time interval for step 1 in milliseconds.
        """
        return self.t1

    def get_step2_time(self):
        """
        Returns the time interval for step 2.
        :return: Time interval for step 2 in milliseconds.
        """
        return self.t2

    def get_step3_time(self):
        """
        Returns the time interval for step 3.
        :return: Time interval for step 3 in milliseconds.
        """
        return self.t3

    def reset(self):
        """
        Resets the sequencer to step 1 and sets the next step time to zero.
        """
        self.current_step = self.ReadingStep.STEP1
        self.next_step_time = 0

    def reset_with_delay(self, delay):
        """
        Resets the sequencer to step 1 with a specified delay.
        :param delay: Delay before the next step in milliseconds.
        """
        self.current_step = self.ReadingStep.STEP1
        self.next_step_time = self._current_millis() + delay  # Get current time in milliseconds

    def run(self):
        """
        Executes the current step function based on the step timer.
        Alternates between step 1, step 2, and step 3 based on their timing.
        """
        current_time = self._current_millis()  # Get current time in milliseconds

        if self.current_step == self.ReadingStep.STEP1:
            if current_time >= self.next_step_time:
                self.s1func()  # Call step 1 function
                self.next_step_time = current_time + self.t1  # Schedule next step 1
                self.current_step = self.ReadingStep.STEP2  # Switch to step 2

        elif self.current_step == self.ReadingStep.STEP2:
            if current_time >= self.next_step_time:
                self.s2func()  # Call step 2 function
                self.next_step_time = current_time + self.t2  # Schedule next step 2
                self.current_step = self.ReadingStep.STEP3  # Switch to step 3

        elif self.current_step == self.ReadingStep.STEP3:
            if current_time >= self.next_step_time:
                self.s3func()  # Call step 3 function
                self.next_step_time = current_time + self.t3  # Schedule next step 3
                self.current_step = self.ReadingStep.STEP1  # Switch back to step 1

    @staticmethod
    def _current_millis():
        """
        Returns the current time in milliseconds.
        Note: This should be replaced with the appropriate method to get time in your application.
        """
        import time
        return int(time.time() * 1000)  # Convert time to milliseconds
