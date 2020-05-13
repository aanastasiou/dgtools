forloop_trace.html:forloop.dgb
	dgsim.py forloop.dgb --with-dump -t 'For loop' -ts R0
	
forloop.dgb:forloop.dsf
	dgasm.py forloop.dsf

clean:
	rm *.dgb *.html

show:forloop_trace.html
	xdg-open forloop_trace.html
