hellosum_trace.html:hellosum.dgb
	dgsim.py hellosum.dgb --with-dump -t 'Hello World'
	
hellosum.dgb:hellosum.dsf
	dgasm.py hellosum.dsf

clean:
	rm *.dgb *.html

html:hellosum_trace.html
	xdg-open hellosum_trace.html
