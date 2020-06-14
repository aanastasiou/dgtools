statusreghack_trace.html: statusreghack.dgb
	dgsim.py statusreghack.dgb -t "Status Register Hack - Doable?" --with-dump
	
statusreghack.dgb: statusreghack.dsf
	dgasm.py statusreghack.dsf

statusreghack3_trace.html: statusreghack3.dgb
	dgsim.py statusreghack3.dgb -t "Status Register Hack - Save & Restore" -ts R0 --with-dump
	
statusreghack3.dgb: statusreghack3.dsf
	dgasm.py statusreghack3.dsf
	
clean:
	rm *.dgb
	rm *.html
	
html: statusreghack_trace.html statusreghack3_trace.html
	xdg-open statusreghack_trace.html
	xdg-open statusreghack3_trace.html
