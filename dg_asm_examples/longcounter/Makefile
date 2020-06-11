long_counter_trace.html: long_counter.dgb
	dgsim.py long_counter.dgb --with-dump -mn 1600
	
long_counter.dgb: long_counter.dsf
	dgasm.py long_counter.dsf
	
html: long_counter_trace.html
	xdg-open long_counter_trace.html
	
clean:
	rm *.dgb
	rm *.html
