# DGTOOLS

DGTools is a set of tools for developing software for a...slider.

Not just any slider, but the [Digirule]() sliders by bradsprojects.

## Tools developed

1. A Digirule Virtual Machine.
    * This is equivalent to having a Digirule and it can be used to try out software before 
      "uploading" it to the hardware. "Uploading" anything slightly more complex than 
      flashing an LED or adding two numbers can be tedious (and this is definitely a 
      feature of the Digirule: Make every click count), so you want to make sure it runs 
      as intended.
    * This VM can be accessed programmatically (so, basically, do whatever you like with it), 
      but it is also used to produce a full "trace" of a program with the state of the CPU
      and its memory space at each step of the computation.

2. An assembler
    * This accepts an assembly text file and produces binary code that can be executed by 
      the virtual machine or be "uploaded" to the hardware.
    * The assembler understands the full reportoir of the Digirule ASM and adds directives 
      to define labels, memory areas and mnemonic symbols.

There are more tools in development.

Enjoy
AA
