"""

Callback functions for events such as user input and serial I/O

:author: Athanasios Anastasiou
:date: Jun 2020
"""

import sys

class DigiruleCallbackBase:
    """
    Base class for all interactions with the Digirule.
    
    Note:
        * An interaction is any operation that interacts with the Digirule object and 
          exchanges data with it.
    """
    pass
    

class DigiruleCallbackInputBase:
    """
    An input interaction brings data in to the Digirule.
    """
    def get_input(self):
        raise NotImplementedError("Cannot instantiate directly.")
        
    def validate_input(self, input_value):
        raise NotImplementedError("Cannot instantiate directly.")
    
    def __call__(self):
        done = False
        while not done:
            input_value = self.get_input()
            try:
                input_value = self.validate_input(input_value)
                done = True
            except ValueError as e:
                print(str(e))
                
        return input_value
    

class DigiruleCallbackOutputBase:
    """
    An output interaction takes data out of the Digirule.
    """
    def __init__(self):
        self._value = None
        
    @property
    def value(self):
        return self._value
        
    def on_new_data(self, a_value):
        raise NotImplementedError("Cannot instantiate directly.")

    def __call__(self, value_from_digirule):
        self.on_new_data(value_from_digirule)
        

class DigiruleCallbackInputUserInteraction(DigiruleCallbackInputBase):
    """
    Prompts the user for (binary) button input.
    """
    
    def __init__(self, user_prompt):
        """
        Configures the prompt.
        
        :returns: Type checked user input
        :rtype: uint8
        """
        super().__init__()    
        self._user_prompt = user_prompt
        
    def get_input(self):
        return input(self._user_prompt)
        
    def validate_input(self, input_value):
        user_input_numeric = int(input_value, 2)
        if user_input_numeric>255:
            raise ValueError("User input greater than 255")                
        return user_input_numeric
        

class DigiruleCallbackComInUserInteraction(DigiruleCallbackInputUserInteraction):
    """
    Prompts the user for serial port input.
    """
    def validate_input(self, input_value):
        if len(input_value) == 0:
            raise ValueError("User input required")
        
        if input_value[0] == "\\":
            # User tries to enter a byte value
            byte_value = int(input_value[1:])
            if byte_value < 0 or byte_value>255:
                raise ValueError(f"COM Input must be a byte value (0-255). Entered {input_value}.")
            return byte_value
        else:
            # User enters a simple character
            if len(input_value)>1:
                raise ValueError(f"COM Input must be a single ASCII character. Entered {input_value}.")
            return ord(input_value)
            

class DigiruleCallbackComRdyUserInteraction(DigiruleCallbackInputUserInteraction):
    """
    Prompts the user on whether the serial port is ready to receive data.
    """
    def validate_input(self, input_value):
        if len(input_value) == 0:
            raise ValueError("User input required")
        user_value = int(input_value)
        if user_value not in (0,1):
            raise ValueError(f"Please specify READY(1), NOT READY(0). Received {user_value}.")
        return user_value


class DigiruleCallbackComOutStoreMem(DigiruleCallbackOutputBase):
    """
    Stores output from comout.
    """
    def __init__(self):
        self._value = []
        
    def on_new_data(self, a_new_value):
        self._value.append(a_new_value)


class DigiruleCallbackComOutStdout(DigiruleCallbackOutputBase):
    """
    Sends output directly to stdout
    """
    # TODO: MED, It would be more informative if this had a configurable prompt too
    def on_new_data(self, a_new_value):
        sys.stdout.write(chr(a_new_value))
