compop_trace.html:compop.dgb
	dgsim.py compop.dgb --with-dump -t 'Comparison Operators' -ts R3 --with-dump
	
compop.dgb:compop.dsf
	dgasm.py compop.dsf

clean:
	rm *.dgb *.html

show:compop_trace.html
	xdg-open compop_trace.html
