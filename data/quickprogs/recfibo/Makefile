recfibo_trace.html:recfibo.dgb
	dgsim.py recfibo.dgb --with-dump -t 'Recursive function call' -ts stack:10 -ts R0 -ts T0 -ts T1

recfibo.dgb: recfibo.dsf
	dgasm.py recfibo.dsf

clean:
	rm *.dgb *.html

html:recfibo_trace.html
	xdg-open recfibo_trace.html
