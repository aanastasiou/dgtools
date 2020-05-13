selectsort_trace.html:selectsort.dgb
	dgsim.py selectsort.dgb --with-dump -t 'Select Sort' -ts R0 -ts R1 -ts R2 -ts R3 -ts R4 -ts num_array:10 -mn 1500
	
selectsort.dgb:selectsort.dsf
	dgasm.py selectsort.dsf

clean:
	rm *.dgb *.html

show:selectsort_trace.html
	xdg-open selectsort_trace.html
