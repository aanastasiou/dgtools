selectsort_trace.html:selectsort.dgb
	dgsim.py selectsort.dgb --with-dump -t 'Select Sort' -ts R0 -ts R1 -ts R2 -ts R3 -ts R4 -ts R5 -ts R6 -ts num_array:10 -mn 2500
	
selectsort.dgb:selectsort.dsf
	dgasm.py selectsort.dsf

clean:
	rm *.dgb *.html

html:selectsort_trace.html
	xdg-open selectsort_trace.html
