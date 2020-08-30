"""
    Adds the ability to use Makefiles as "backends" for dgui and other services.
    
    A Makefile configures a compilation process by determining the sequence of operations (assembly, simulation)
    that are to be applied to a .dsf file.
    
    This bit of code allows dgui and other programs to parse a Makefile and auto-configure the "defaults" of the 
    process.
    
    For example, dgui.py is called with a source file as a parameter. If dgui.py finds a makefile in the same directory 
    as the source code file that contains at least two digirule makefile rules that concern the .dsf file mentioned, 
    it will configure itself as per the Makefile and re-produce that same makefile.
    
    From this point of view, the Makefile becomes a "settings backend" for dgui and other programs.
    
:author: Athanasios Anastasiou
:date: Aug 2020
"""
import pyparsing

class MakefileException(Exception):
    pass
    
    
class DgToolsMakefileActionDgsimSymbols:
    """
    Makes symbols computable.
    """
    def __init__(self, parsed_symbols):
        self._parsed_symbols = parsed_symbols
        
    def _symbols2str(self, to_cmd_line=False):
        """
        Returns a string representation of just the input symbols.
        """
        delim = " " if to_cmd_line else ","
        symbol_items = []
        symbol_str = ""
        for a_symbol in self._parsed_symbols:
            symbol_str=f"{(a_symbol['ts']+' ') if to_cmd_line else ''}{a_symbol['symbol_data']['symbol']}"
            if "length" in a_symbol["symbol_data"]:
                symbol_str+=f":{a_symbol['symbol_data']['length']}"
            if "offset" in a_symbol["symbol_data"]:
                symbol_str+=f":{a_symbol['symbol_data']['offset']}"
            symbol_items.append(symbol_str)
        return delim.join(symbol_items)

    def __str__(self):
        return self._symbols2str(to_cmd_line=True)
        
    def defined_symbols_as_str(self):
        """
        Returns the defined symbols as a plain simple space delimited string.
        
        Note:
            * __str__() Is used for plain simple serialisation.
        """
        return self._symbols2str()
        

class DgToolsMakefileAction:
    """
    Represents an action that involves one of the dgtools (Either dgasm or dgsim).
    
    Note:
        * Handles each object's parameters and converting those parameters back to a string representation.
    """
    def __init__(self, action, parsed_parameters):
        """
        Establishes a specific action with its parameters.
        
        :param action: The action to perform corresponds to a 'script'. This is either dgasm.py, or dgsim.py
        :type action: str, values 'dgasm.py' or 'dgsim.py' only
        :param parsed_parameters: Parsed parameter dictionary as received from the parser
        :type parsed_parameters: pyparsing.ParsedResults (Please see the parser for more information on its structure)
        """
        self._action = action
        self._parsed_parameters = parsed_parameters
                
    def __str__(self):
        """
        Compiles the action back to a string that if evaluated on the command line carries out the action.
        """
        # Build the parameter string
        param_str = ""
        for a_param in self._parsed_parameters.values():
            if not isinstance(a_param,str):
                param_str+=f" {' '.join([str(q) for q in a_param])}"
            else:
                param_str+=f" {a_param}"
        return f"{self._action} {param_str}"
        
    @property
    def params(self):
        """
        Returns the parameters that have been parsed for this action.
        """
        return list(self._parsed_parameters.keys())
        
    def __getitem__(self, item):
        """
        Convenience function that allows to get the value of a specific parameter in place.
        """
        try:
            if isinstance(self._parsed_parameters[item], pyparsing.ParseResults):
                # Here, always returning the last item of the parsed result means that the captured value is returned.
                # Note: Usually, parameters are always in a key value form.
                return self._parsed_parameters[item][-1]
            else:
                return self._parsed_parameters[item]
        except KeyError:
            return ""

    def __setitem__(self, item, value):
        """
        Convenience function that allows to set the value of a specific parameter in place.
        """
        if isinstance(self._parsed_parameters[item],pyparsing.ParseResults):
            self._parsed_parameters[item][-1]=value
        else:
            self._parsed_parameters[item]=value


class DgToolsMakefileRule:
    """
    Represents a computable Makefile rule.
    """
    def __init__(self, target, dependencies, action):
        self._target = target
        self._dependencies = dependencies
        self._action = action
    
    def __str__(self):
        return f"{self._target}:{self._dependencies}\n\t{str(self._action[0])}"
        
    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, new_target):
        self._target = new_target
    
    @property
    def dependencies(self):
        return self._dependencies

    @dependencies.setter
    def dependencies(self, new_dep):
        self._dependencies = new_dep

    @property
    def action(self):
        return self._action[0]


class DgToolsMakefile:
    """
    Represents a very very simple view of a Makefile from the point of view of Dgtools actions.
    """
    def __init__(self, prologue, main, epilogue):
        self._prologue = prologue
        self._main = main
        self._epilogue = epilogue
        # This is a convenient index that enables the in-place editing of specific rules
        self._targets = dict(map(lambda x:(x["rule"].target, x["rule"]), self._main))        
        
    def __str__(self):
        makefile_str=f"{self._prologue}\n"
        
        for a_rule in range(len(self._main)):
            makefile_str+=f"{self._main[a_rule]['rule']}\n"
            if "other" in self._main[a_rule]:
                makefile_str+=f"{str(self._main[a_rule]['other'])}\n"
                
        makefile_str+=f"{self._epilogue}\n"
        return makefile_str

    @property
    def targets(self):
        return list(self._targets.keys())
        
    def __getitem__(self, item):
        return self._targets[item]
            

class DgToolsMakefileParser:
    """
    Handles the parsing, in-place editing and re-synthesis of a Makefile.
    """
    def __init__(self):
        self._makefile_parser = self._get_parser()
        
    def __call__(self, makefile_text):
        return self._makefile_parser.parseString(makefile_text)[0]
        
    @staticmethod   
    def _get_parser():
        """
        Parser definitions
        """
        # DGSIM PARSER
        # Generic File
        a_file = pyparsing.Regex("[^ \!\$\`\&\*\(\)\+\:\\n]+")
        # Generic identifier
        an_idf = pyparsing.Regex("[a-zA-Z_][a-zA-Z_0-9]+")
        
        max_n = (pyparsing.Regex("-mn|--max-n") + 
                 pyparsing.Regex("[0-9]+").setParseAction(lambda s,loc,tok:int(tok[0])))
        
        skip_n = (pyparsing.Regex("-sn|--skip-n") + 
                  pyparsing.Regex("[0-9]+").setParseAction(lambda s,loc,tok:int(tok[0])))
        
        interactive_mode = pyparsing.Regex("-I|--interactive-mode")
        with_dump = pyparsing.Regex("-wd|--with-dump")
        title = (pyparsing.Regex("--title|-t") + pyparsing.quotedString())
        otf = pyparsing.Regex("-otf|--output-trace_file") + a_file
        omf = pyparsing.Regex("-omf|--output-memdump_file") + a_file
        theme = pyparsing.Regex("--theme") + an_idf
        
        trace_symbol = pyparsing.Group(pyparsing.Regex("[a-zA-Z_][a-zA-Z0-9_]*")("symbol") + 
                                       pyparsing.Optional(pyparsing.Suppress(":") + 
                                       pyparsing.Regex("[0-9]+")("length") + 
                                       pyparsing.Optional(pyparsing.Suppress(":") + 
                                                          pyparsing.Regex("[0-9]+")("offset"))))
                                                          
        trace_symbols = pyparsing.OneOrMore(pyparsing.Group(pyparsing.Regex("-ts|--trace-symbol")("ts") + 
                                                            trace_symbol("symbol_data"))).setParseAction(lambda s,loc,tok:DgToolsMakefileActionDgsimSymbols(tok))

        dgsim_rule = (pyparsing.Suppress("dgsim.py") + 
                      a_file("input_file") + 
                      (pyparsing.Optional(max_n)("max_n") & 
                       pyparsing.Optional(skip_n)("skip_n") & 
                       pyparsing.Optional(interactive_mode)("interactive_mode") & 
                       pyparsing.Optional(with_dump)("with_dump") & 
                       pyparsing.Optional(title)("title") & 
                       pyparsing.Optional(otf)("otf") & 
                       pyparsing.Optional(omf)("omf") &
                       pyparsing.Optional(theme)("theme") & 
                       pyparsing.Optional(trace_symbols)("trace_symbols"))).setParseAction(lambda s,loc,tok:DgToolsMakefileAction(action="dgsim.py",
                                                                                                                                  parsed_parameters = tok)) 
        
        # DGASM PARSER
        output_file = (pyparsing.Regex("-o|--output-file") + a_file)
        target = (pyparsing.Regex("-g|--target") + pyparsing.Regex("2(A|U)"))
 
 
        dgasm_rule = (pyparsing.Suppress("dgasm.py") + 
                      a_file("input_file") + 
                      (pyparsing.Optional(output_file)("output_file") & 
                       pyparsing.Optional(target)("target"))).setParseAction(lambda s,loc,tok:DgToolsMakefileAction(action="dgasm.py", 
                                                                                                                    parsed_parameters = tok)) 
        # MAKEFILE RULE                                                                                                            
        makefile_rule = (a_file("target_file") + 
                         pyparsing.Suppress(":") + 
                         a_file("dependencies") + 
                         (dgsim_rule ^ 
                          dgasm_rule)("action")).setParseAction(lambda s,loc,tok:DgToolsMakefileRule(target=tok["target_file"], 
                                                                                                     dependencies=tok["dependencies"], 
                                                                                                     action=tok["action"]))
                
        # MAKEFILE
        other = pyparsing.SkipTo(makefile_rule)

        makefile = (pyparsing.Optional(other)("prologue") +
                    pyparsing.OneOrMore(pyparsing.Group(makefile_rule("rule") + 
                                        pyparsing.Optional(other)("other")))("main") + 
                    pyparsing.Optional(pyparsing.SkipTo(pyparsing.StringEnd()))("epilogue")).setParseAction(lambda x,loc,tok:DgToolsMakefile(prologue=tok["prologue"], 
                                                                                                                                             main=tok["main"], 
                                                                                                                                             epilogue=tok["epilogue"]))

        return makefile
    
# if __name__ == "__main__":
    # with open("Makefile") as fd:
        # data=fd.read()
        
    # v = DgToolsMakefileParser()(data)
