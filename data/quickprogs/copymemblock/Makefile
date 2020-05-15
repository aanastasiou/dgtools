copymemblock_trace.html:copymemblock.dgb
	dgsim.py copymemblock.dgb --with-dump -t 'Copy a memory block' -ts R0
	
copymemblock.dgb:copymemblock.dsf
	dgasm.py copymemblock.dsf

clean:
	rm *.dgb *.html

show:copymemblock_trace.html
	xdg-open copymemblock_trace.html
