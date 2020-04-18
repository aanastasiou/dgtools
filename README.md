# dgtools

dgtools is a set of tools for developing software for a...ruler.

Not just any ruler, but the [Digirule2](https://bradsprojects.com/digirule2/) by 
[bradsprojects](https://bradsprojects.com).

## Tool Overview

1. `dgasm`

   * The assembler, accepts a human readable `.asm` text file with Digirule2 ASM and 
     produces a `.dgb` binary file with compiled code ready to be executed on the hardware.
   
2. `dginspect`

   * The binary file "inspector", accepts a `.dgb` binary file and produces a human readable 
     "dump" of the full 256 byte memory range to stdout. It also allows a user to apply certain 
     modifications to the memory space without re-compiling.
   
3. `dgsim`

   * The Digirule2 Virtual Machine, accepts a `.dgb` binary file and produces:
       1. A human readable (HTML) trace of every state change the CPU goes through at each 
          timestep of execution.
       2. The final `.dgb` file that contains the final state of the memory space at the end of 
          execution.
     
These three tools work together to write, debug and simulate code for the Digirule 2 prior to "uploading" it to the 
actual hardware.

The most common workflow is:

1. Use a text editor to write human readable assembly code.
2. Call `dgasm.py` to compile the binary
3. Call `dgsim.py` to run and debug the binary
4. Use `dginspect.py` to check a binary file, get/set values from the virtual machine or key the code in.


## Installation

### Pre-requisites

1. Linux
2. Python >3.6
3. [`virtualenv`](https://pypi.org/project/virtualenv/)

### Process

1. Download the code from the repository
2. `> virtualenv -p python3.6 pyenv`
3. `> source pyenv/bin/activate`
4. To start using `dgtools`:
     * `pip install -e ./` (From within the `dgtools/` directory that contains the `setup.py` file)
     * This will make the `dgtools` scripts callable from any position in the filesystem, as long as the 
       virtual environment is activated.
5. If you are interested in developing `dgtools` further: 
     * `pip install -r requirements.txt`


## Where to from here?

``dgtools`` documentation is up on [ReadTheDocs](https://dgtools.readthedocs.io/en/latest/) and in ``doc/``.

* The features of each of the programs included in `dgtools` are best demonstrated through 
[this introductory walkthrough](https://dgtools.readthedocs.io/en/latest/introductory_topics.html)

* Advanced uses of the Digirule 2 ASM are discussed in 
 [this advanced walkthrough](https://dgtools.readthedocs.io/en/latest/advanced_topics.html)

Enjoy

Athanasios Anastasiou
