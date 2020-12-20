![](https://dgtools.readthedocs.io/en/latest/_images/full_banner_dg.png)

# dgtools

dgtools is a complete toolkit for developing software for the [Digirule](https://bradsprojects.com/digirule2/) 
series (`2A/2U`) of hardware by [bradsprojects](https://bradsprojects.com).

## Overview

1. `dgasm`

   * The assembler, accepts a human readable `.asm` text file with Digirule ASM and 
     produces:
       1. A `.dgb` binary file with compiled code ready for simulation by `dgsim.py` .
       2. A `.hex` file (in the case of 2U) to be downloaded to the board.
   
2. `dginspect`

   * The binary file "inspector", accepts a `.dgb` binary file and produces a human readable 
     "dump" of the full 256 byte memory range to stdout. It also allows a user to apply certain 
     modifications to the memory space without re-compiling.
   
3. `dgsim`

   * The Digirule Virtual Machine, accepts a `.dgb` binary file and produces:
       1. A human readable HTML (themeable) trace of every state change the CPU goes through at each 
          timestep of execution.
       2. An additional `.dgb` file that contains the final state of the memory space at the end of 
          program execution.
               
These tools work together to write, debug and simulate code for the Digirule 2 prior to transfering it to the 
actual hardware. 

`dgtools` also includes some "extras", such as:

1. A Sublime text `.dsf` ASM plugin, 
2. A console gui (`dgui.py`) that can handle compilation/simulation in one step 
3. A code formatter (`dgform.py`), to pretty print source code.
4. [Brainfuck](https://esolangs.org/wiki/Brainfuck) and [Super Stack!](https://esolangs.org/wiki/Super_Stack!) compilers for the Digirule 2U.

The most common workflow is to:

1. Use a text editor to write human readable assembly code.
2. Call `dgasm.py` to compile the binary
3. Call `dgsim.py` to run and debug the binary
4. *(Alternatively, call `dgui` to perform both of the above in sequence)*
5. Use `dginspect.py` to check a binary file, get/set values from the virtual machine or key the code in.


## Installation

### Pre-requisites

1. Linux
2. Python >=3.6
3. [`virtualenv`](https://pypi.org/project/virtualenv/)


### Install from PyPi with pip

* `pip install dgtools`


### Install latest development version  

1. Checkout the dgtools repository
2. `> virtualenv -p python3.8 pyenv`
3. `> source pyenv/bin/activate`
4. To start using `dgtools`:
     * `pip install -e ./` (From within the `dgtools/` directory that contains the `setup.py` file)
     * This will make the `dgtools` scripts callable from any position in the filesystem, as long as the 
       `pyenv` virtual environment is activated.
5. If you are interested in developing `dgtools` further: 
     * `pip install -r requirements.txt`


## Where to from here?

``dgtools`` documentation is up on [ReadTheDocs](https://dgtools.readthedocs.io/en/latest/) and of course
in ``doc/``.

Practical examples of how to use `dgtools` are available in 
[this introductory walkthrough](https://dgtools.readthedocs.io/en/latest/introductory_topics.html).

Once you familiarise yourself with the tools and Digirule's ASM, you might want to move to 
[the advanced walkthrough](https://dgtools.readthedocs.io/en/latest/advanced_topics.html) or 
check out other [programming examples](https://dgtools.readthedocs.io/en/latest/code_projects.html) 
in `dg_asm_eamples/`.

## dgrdo.org

The ASM toolchain along with the brainfuck and Super Stack! compilers is available online at https://www.dgrdo.org. 
For more information see [this introduction on its functionality](https://www.dgrdo.org/static/info/about/index.html)

Enjoy!

Athanasios Anastasiou
