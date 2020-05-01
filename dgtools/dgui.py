#!/usr/bin/env python
"""
Usage: dgui.py [OPTIONS] INPUT_FILE

  Text based user interface to dgasm and dgsim.

  This script accepts one parameter (INPUT_FILE) that is the .dsf file to go
  through the  compilation procedure.

Options:
  -o, --output_file PATH  Optionally sets the output file
  --help                  Show this message and exit.

:author: Athanasios Anastasiou
:date: April 2020
"""
import os
import sys
import subprocess
import pyparsing
try:
    import urwid
except ModuleNotFoundError:
    print(f"\ndgui.py depends on urwid, a library to build text user interfaces, which was not found on your system.\n"
          f"If you wish to use dgui.py, please install the urwid library with `pip install urwid` and try again.\n")
    sys.exit(1)
import click


def get_symbols_parser():
    """
    Returns a very simple parser to validate the extra symbols passed to the simulator.
    """
    identifier = pyparsing.Regex("[a-zA-Z_][0-9A-Za-z_]*")
    positive_integer = pyparsing.Regex("[0-9]+")
    numeric_param = pyparsing.Suppress(":") + positive_integer
    
    symbol_record = pyparsing.Group(identifier("id") + 
                    pyparsing.Optional(numeric_param("len") + 
                    pyparsing.Optional(numeric_param("offset"))))
    symbol_records = pyparsing.delimitedList(symbol_record)    
    return symbol_records



class MessageBox(urwid.WidgetWrap):
    """
    Presents a standard OK, Cancel message box.
    """
    # Signals emmitted by this widget
    signals=["close"]
    def __init__(self, message):
        """
        Sets up the message box
        """
        ok_cancel = urwid.GridFlow([urwid.AttrMap(urwid.Button("OK".center(15), on_press=self.on_ok),
                                                  "dialog_button_plain",
                                                  "dialog_button_focused"),],
                                   20,4,1,"center")
        mb_widget = urwid.AttrMap(urwid.LineBox(
                                                urwid.ListBox([urwid.Text("\n".join(message)), 
                                                               urwid.Divider("\u2015"), 
                                                               ok_cancel])), "bg")
        
        super().__init__(mb_widget)
        
    def on_ok(self, a_b):
        self._emit("close")
        
    
class ModalDialogBox(urwid.PopUpLauncher):
    """
    A standard modal dialog box that handles all user interaction.
    
    Note:
        * The dialog box handles all user interaction and returns script parameters 
          that are validated and ready to be sent to the dgtools scripts. These 
          parameters are made available to the dialog box caller via properties.
    """
    def __init__(self, input_file, output_file, trace_file=None):
        """
        Initialises the dialog box and determines initial values for all the UI elements.
        """
        
        if output_file is None:
            output_file = f"{os.path.splitext(input_file)[0]}.dgb"
        
        if trace_file is None:
            trace_file = f"{os.path.splitext(input_file)[0]}_trace.html"
        
        trace_title = os.path.split(input_file)[1]
        self._in_file = urwid.Edit("Source file:", input_file)
        self._out_file = urwid.Edit("Binary file:", output_file)
        self._trace_title = urwid.Edit("Trace Title:", trace_title)
        self._trace_file = urwid.Edit("Trace HTML file:", trace_file)
        self._with_mem_dump = urwid.CheckBox("Mem dump at every cycle")
        self._in_interactive_mode = urwid.CheckBox("Interactive mode")
        self._maximum_cycles_to_run = urwid.IntEdit("Maximum cycles to run:",200)
        self._extra_syms = urwid.Edit("Extra symbols to track:")
        
        ok_cancel = urwid.GridFlow([urwid.AttrMap(urwid.Button("OK".center(15),
                                                               on_press = self._on_ok),
                                                  "dialog_button_plain",
                                                  "dialog_button_focused"), 
                                    urwid.AttrMap(urwid.Button("Cancel".center(15), 
                                                               on_press = self._on_cancel),
                                                  "dialog_button_plain",
                                                  "dialog_button_focused")],
                                    20,4,1,"center")
                                    
        final_widget = urwid.AttrMap(urwid.LineBox(urwid.ListBox([
                                                   urwid.AttrMap(urwid.Text("Arrow keys navigate the menu. <Enter> "
                                                                            "or <Space> marks the checkboxes. <Esc> "
                                                                            "cancels everything and returns to "
                                                                            "prompt."),
                                                                 "dialog_help"),
                                                   urwid.AttrMap(urwid.Text("Input/Output"),"dialog_section"),
                                                   urwid.AttrMap(urwid.WidgetDisable(self._in_file),
                                                                 "dialog_plain", "dialog_focused"),
                                                   urwid.AttrMap(self._out_file,"dialog_plain","dialog_focused"),
                                                   urwid.AttrMap(self._trace_file,"dialog_plain","dialog_focused"),
                                                   urwid.AttrMap(urwid.Text("Simulation parameters"),"dialog_section"),     
                                                   urwid.AttrMap(self._trace_title,"dialog_plain","dialog_focused"), 
                                                   urwid.AttrMap(self._with_mem_dump,"dialog_plain","dialog_focused"), 
                                                   urwid.AttrMap(self._in_interactive_mode,
                                                                 "dialog_plain","dialog_focused"), 
                                                   urwid.AttrMap(self._maximum_cycles_to_run,
                                                                 "dialog_plain","dialog_focused"), 
                                                   urwid.AttrMap(self._extra_syms,"dialog_plain","dialog_focused"),
                                                   urwid.Divider("\u2015"),
                                                   ok_cancel]), title="Dgtools Compilation Parameters"),"dialog_plain")
        self._was_ok = False
        super().__init__(final_widget)
        
    def _on_ok(self, a_button):
        validation_messages = []
        # Check the format of extras
        if len(self._extra_syms.edit_text)>0:
            try:
                get_symbols_parser().parseString(self._extra_syms.edit_text)
            except pyparsing.ParseException:
                validation_messages.append("* Please check extra symbols passed.")
        # Check that output directories exist
        output_file_dir = os.path.split(self.output_file)[0]
        if not os.path.isdir(output_file_dir):
            validation_messages.append(f"* Binary file path {output_file_dir} does not exist")

        output_trace_file_dir = os.path.split(self.output_trace_file)[0]
        
        if not os.path.isdir(output_trace_file_dir):
            validation_messages.append(f"* Trace HTML file path {output_trace_file_dir} does not exist")

        if len(validation_messages)>0:
            self._validation_messages = validation_messages
            self.open_pop_up()
        else:
            self._was_ok = True
            raise urwid.ExitMainLoop()
                
    def _on_cancel(self, a_button):
        raise urwid.ExitMainLoop()

    def get_pop_up_parameters(self):
        return {"left":-5, "top":1, "overlay_width":80, "overlay_height":7}

    def create_pop_up(self):
        pop_up = MessageBox(self._validation_messages)
        urwid.connect_signal(pop_up, 'close', lambda button: self.close_pop_up())
        return pop_up

    @property
    def closed_ok(self):
        return self._was_ok
        
    @property
    def input_file(self):
        return self._in_file.edit_text
    
    @property        
    def output_file(self):
        return self._out_file.edit_text
        
    @property
    def output_trace_file(self):
        return self._trace_file.edit_text
        pass
    
    @property        
    def trace_title(self):
        return self._trace_title.edit_text
    
    @property        
    def with_mem_dump(self):
        return self._with_mem_dump.state
    
    @property        
    def in_interactive_mode(self):
        return self._in_interactive_mode.state
    
    @property        
    def maximum_cycles_to_run(self):
        return self._maximum_cycles_to_run.value()

    @property        
    def extra_symbols(self):
        entries_to_return = list(filter(lambda x:len(x)>0,self._extra_syms.edit_text.replace(" ","").split(",")))
        return entries_to_return


def handle_esc(key):
    if key=="esc":
        raise urwid.ExitMainLoop()
    
    
@click.command()
@click.argument("input_file",type=click.Path(exists=True))
@click.option("--output_file","-o",type=click.Path(), help="Optionally sets the output file")
def main(input_file, output_file):
    """
    Text based user interface to dgasm and dgsim.
    
    This script accepts one parameter (INPUT_FILE) that is the .dsf file to go through the 
    compilation procedure.
    
    \f
    :param input_file: The .dsf file that has to be compiled
    :type input_file: str
    :param output_file: The .dgb file that is to be created
    :type output_file: str
    """
    palette = [
    ('dialog_plain', 'light gray', 'dark blue'),
    ("dialog_bright", "white", "dark blue"),
    ("dialog_focused", "white", "dark gray"),
    ("dialog_button_plain", "black", "light gray"),
    ("dialog_button_focused", "white", "dark red"),
    ("dialog_section", "white", "light blue"),
    ("dialog_help", "light gray", "dark blue"),
    ('bg', 'black', 'light gray'),]
    
    params_dialog_box = ModalDialogBox(input_file, output_file)
    
    loop = urwid.MainLoop(urwid.Overlay(urwid.AttrMap(params_dialog_box, "bg"),
                                        urwid.AttrMap(urwid.SolidFill("\u2588"),"bg"),
                                                      align="center",
                                                      width=66,
                                                      valign="middle", 
                                                      height=16), palette, 
                                                      unhandled_input=handle_esc,
                                                      pop_ups = True)
    loop.run()
    # Format and produce output here
    if params_dialog_box.closed_ok:
        # Run the assembler here
        dgasm_params = ["dgasm.py",params_dialog_box.input_file]
        if len(params_dialog_box.output_file):
            dgasm_params.extend(["-o", params_dialog_box.output_file])
        
        dgsim_params = ["dgsim.py", params_dialog_box.output_file, "-mn", str(params_dialog_box.maximum_cycles_to_run)]
        if len(params_dialog_box.output_trace_file):
            dgsim_params.extend(["-otf", params_dialog_box.output_trace_file])
        if len(params_dialog_box.trace_title):
            dgsim_params.extend(["-t", params_dialog_box.trace_title])
        if params_dialog_box.in_interactive_mode:
            dgsim_params.extend(["-I"])
        if params_dialog_box.with_mem_dump:
            dgsim_params.extend(["--with-dump"])
        if len(params_dialog_box.extra_symbols)>0:
            for a_symbol in params_dialog_box.extra_symbols:
                dgsim_params.extend(["-ts", f"{a_symbol}"])
        
        dgasm_process = subprocess.Popen(dgasm_params, stdout=subprocess.PIPE, text=True)
        if dgasm_process.wait()!=0:
            sys.stdout.write(dgasm_process.stdout.read())
        else:
            sys.stdout.write("Compilation succesful.\n")
            # If that was succesful, run the simulator
            dgsim_process = subprocess.Popen(dgsim_params, stdout=subprocess.PIPE, text=True)
            if dgsim_process.wait()!=0:
                sys.stdout.write(dgsim_process.stdout.read())
            else:
                sys.stdout.write("Simulation succesful.\n")
    else:
        sys.stdout.write("Compilation canceled\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
