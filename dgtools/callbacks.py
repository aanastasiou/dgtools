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
        * An interaction is any operation that interacts with a Digirule object and 
          exchanges data.
        * Use interactions to simulate interfaces with entities that are external to 
          the Digirule.
        * Callbacks have a label that provides a brief description so that the user knows
          which interaction this is for.
    """
    
    def __init__(self, cb_label):
        """
        Configures the label of the interaction callback.
        
        :returns: Type checked user input
        :rtype: uint8
        """

        if not isinstance(cb_label, str):
            raise TypeError(f"Callback labels are expected to be str, received {type(cb_label)}.")
        self._cb_label = cb_label
    
    @property
    def label(self):
        return self._cb_label
    
    @label.setter
    def label(self, new_label):
        if not isinstance(new_label, str):
            raise TypeError(f"Callback labels are expected to be str, received {type(new_label)}.")
        self._cb_label = new_label
        


class DigiruleCallbackInputBase(DigiruleCallbackBase):
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
    

class DigiruleCallbackOutputBase(DigiruleCallbackBase):
    """
    An output interaction takes data out of the Digirule.
    """
    def __init__(self, cb_label):
        super().__init__(cb_label)
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
    def get_input(self):
        return input(self.label)
        
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
                raise ValueError(f"COM Input must be a single ASCII character or '\\0-255' (e.g. \\65 for A). Entered {input_value}.")
            return ord(input_value)
            

class DigiruleCallbackComOutStoreMem(DigiruleCallbackOutputBase):
    """
    Stores output from comout.
    """
    def __init__(self):
        self._value = []
        
    def on_new_data(self, a_new_value):
        self._value.append(a_new_value)


# TODO: LOW, Rename DigiruleCallbackComOutStdout to a more generic name because it is more generally applicable.
class DigiruleCallbackComOutStdout(DigiruleCallbackOutputBase):
    """
    Sends output directly to stdout.
    """
    def on_new_data(self, a_new_value):
        sys.stdout.write(f"{self.label} {chr(a_new_value):3s} - 0x{(a_new_value & 0xFF):03X}\n")


class DigiruleCallbackPinInUserInteraction(DigiruleCallbackInputUserInteraction):
    """
    Prompts the user for pin input.
    """
    def validate_input(self, input_value):
        if len(input_value) == 0:
            raise ValueError("User input required")
            
        if input_value not in ["0","1"]:
            raise ValueError(f"Pin Input should be a single character ('0' or '1'). Entered {input_value}.")

        return int(input_value) & 0xFF
