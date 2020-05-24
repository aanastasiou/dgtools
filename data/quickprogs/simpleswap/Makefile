swap_simple_trace.html: swap_simple.dgb
	dgsim.py swap_simple.dgb -ts R0 -ts R1 -ts R2 -t 'Plain swap'
	
swap_indirect_trace.html: swap_indirect.dgb
	dgsim.py swap_indirect.dgb -ts R0 -ts R1 -ts R2 -t 'Indirect swap'

swap_simple.dgb: swap_simple.dsf
	dgasm.py swap_simple.dsf
	
swap_indirect.dgb: swap_indirect.dsf
	dgasm.py swap_indirect.dsf
	
clean:
	rm *.dgb *html
	
show: swap_indirect_trace.html swap_simple_trace.html
	chromium-browser swap_simple_trace.html &
	chromium-browser swap_indirect_trace.html &
