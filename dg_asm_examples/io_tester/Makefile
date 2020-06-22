io_tester_trace.html: io_tester.dgb
	dgsim.py io_tester.dgb -I
	
io_tester.dgb: io_tester.dsf
	dgasm.py io_tester.dsf
	
clean:
	rm *.html
	rm *.dgb
	
html: io_tester_trace.html
	xdg-open io_tester_trace.html
