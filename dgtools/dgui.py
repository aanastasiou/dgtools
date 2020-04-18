#!/usr/bin/env python
"""

A minimal UI to the whole toolchain based on urwid

:author: Athanasios Anastasiou
:date: April 2020
"""
import os
import sys
import urwid
import click

    
class ModalDialogBox(urwid.WidgetWrap):
    def __init__(self, input_file, output_file):
        if output_file is None:
            output_file = f"{os.path.splitext(input_file)[0]}.dgb"
        
        trace_title = os.path.split(input_file)[1]
        self._in_file = urwid.Edit("Source file:", input_file)
        self._out_file = urwid.Edit("Binary file:", output_file)
        text = urwid.Text("Simulation parameters")
        self._trace_title = urwid.Edit("Trace Title:", trace_title)
        self._with_mem_dump = urwid.CheckBox("Mem dump at every cycle")
        self._in_interactive_mode = urwid.CheckBox("Interactive mode")
        self._maximum_cycles_to_run = urwid.IntEdit("Maximum cycles to run:",200)
        self._extra_syms = urwid.Edit("Extra symbols to track:")
        ok_cancel = urwid.GridFlow([urwid.Button("OK".center(15),on_press = self._on_ok), 
                                    urwid.Button("Cancel".center(15), on_press = self._on_cancel)],20,4,1,"center")
        final_widget = urwid.ListBox([urwid.Text("Input/Output"),
                                       self._in_file,
                                       self._out_file,
                                       text,     
                                       self._trace_title, 
                                       self._with_mem_dump, 
                                       self._in_interactive_mode, 
                                       self._maximum_cycles_to_run, 
                                       self._extra_syms,
                                       ok_cancel])
        self._was_ok = False
        super().__init__(final_widget)
        
    def _on_ok(self, a_button):
        self._was_ok = True
        raise urwid.ExitMainLoop()
                
    def _on_cancel(self, a_button, on_done):
        raise urwid.ExitMainLoop()
    
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


@click.command()
@click.argument("input_file",type=click.Path(exists=True))
@click.option("--output_file","-o",type=click.Path(), help="Optionally sets the output file")
def main(input_file, output_file):
    """
    Help for UI
    """
    palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue'),]
    
    params_dialog_box = ModalDialogBox(input_file, output_file)
    
    loop = urwid.MainLoop(urwid.AttrMap(params_dialog_box, "default"), palette)
    loop.run()
    # Format and produce output here
    if params_dialog_box.closed_ok:
        add_params = f"-mn {params_dialog_box.maximum_cycles_to_run} "
        if params_dialog_box.in_interactive_mode:
            add_params+="-I "
        if len(params_dialog_box.trace_title):
            add_params+=f"-t {params_dialog_box.trace_title} "
        if params_dialog_box.with_mem_dump:
            add_params+=f"--with-dump "
        if len(params_dialog_box.extra_symbols)>0:
            add_params+=" ".join(map(lambda x:f"-ts {x}",params_dialog_box.extra_symbols))
        sys.stdout.write(f"dgasm.py {params_dialog_box.input_file} && \
                           dgsim.py {params_dialog_box.output_file} {add_params}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
