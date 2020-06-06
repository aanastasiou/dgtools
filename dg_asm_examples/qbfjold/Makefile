qbfjold_trace.html:qbfjold.dgb
	dgsim.py qbfjold.dgb --with-dump -t 'QBFJOLD' -ts R0 -ts R1
	
qbfjold.dgb:qbfjold.dsf
	dgasm.py qbfjold.dsf

clean:
	rm *.dgb *.html

html:qbfjold_trace.html
	xdg-open qbfjold_trace.html
