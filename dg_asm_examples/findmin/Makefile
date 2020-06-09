findmin_trace.html:findmin.dgb
	dgsim.py findmin.dgb --with-dump -t 'Find Minimum' -ts R0 -ts R1 -ts R2 -ts num_array:20 -mn 1500
	
findmin.dgb:findmin.dsf
	dgasm.py findmin.dsf

clean:
	rm *.dgb *.html

html:findmin_trace.html
	xdg-open findmin_trace.html
