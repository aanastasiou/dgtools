assoc_array_trace.html:assoc_array.dgb
	dgsim.py assoc_array.dgb --with-dump 
	
assoc_array.dgb:assoc_array.dsf
	dgasm.py assoc_array.dsf -g 2U
	
html: assoc_array_trace.html
	xdg-open array_trace.html
	
clean:
	rm *.html
	rm *.dgb
