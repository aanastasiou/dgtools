swapmemblock_trace.html:swapmemblock.dgb
	dgsim.py swapmemblock.dgb --with-dump -t 'Swap two memory blocks' -ts R0:6 -ts R1:6 -ts R2:6
	
swapmemblock.dgb:swapmemblock.dsf
	dgasm.py swapmemblock.dsf

clean:
	rm *.dgb *.html

show:swapmemblock_trace.html
	xdg-open swapmemblock_trace.html
