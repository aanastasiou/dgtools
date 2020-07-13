serialpaging_trace.html: serialpaging.dgb
	dgsim.py serialpaging.dgb -I -mn 200 --with-dump

serialpaging.dgb:serialpaging.dsf
	dgasm.py serialpaging.dsf -g 2U

html:serialpaging_trace.html
	xdg-open serialpaging_trace.html

clean:
	rm *.html
	rm *.dgb
