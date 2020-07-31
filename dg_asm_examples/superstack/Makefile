sust_program.dsf: sust_program.ssf
	./superstack_to_asm.py sust_program.ssf>sust_program.dsf
	
sust_program_trace.html:sust_program.dgb
	dgsim.py sust_program.dgb -I -mn 4000 -ts stack:14 -ts head_ptr -ts head_val -ts head_val_1
	
sust_program.dgb:sust_program.dsf
	dgasm.py sust_program.dsf -g 2U 
	
html:sust_program_trace.html
	xdg-open sust_program_trace.html
	
clean:
	rm sust_program.dsf
	rm sust_program.dgb
	rm sust_program_memdump.dgb
	rm sust_program_trace.html
	
