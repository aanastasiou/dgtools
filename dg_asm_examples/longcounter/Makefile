longcounter_trace.html: longcounter.dgb
	dgsim.py longcounter.dgb -t 'One Long Counter' --with-dump -mn 2600
	
longcounter.dgb: longcounter.dsf
	dgasm.py longcounter.dsf
	
html: longcounter_trace.html
	xdg-open longcounter_trace.html
	
clean:
	rm *.dgb
	rm *.html
