arrayindexing_trace.html:arrayindexing.dgb
	dgsim.py arrayindexing.dgb --with-dump -t 'Array indexing' -ts array_idx -ts array_idx_value -ts num_array:10
	
arrayindexing.dgb:arrayindexing.dsf
	dgasm.py arrayindexing.dsf

clean:
	rm *.dgb *.html

html:arrayindexing_trace.html
	xdg-open arrayindexing_trace.html
