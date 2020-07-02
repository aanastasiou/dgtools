fixedpointmath_trace.html: fixedpointmath.dgb
	dgsim.py fixedpointmath.dgb -ts R0 -ts R1 -ts R2
	
fixedpointmath.dgb: fixedpointmath.dsf
	dgasm.py fixedpointmath.dsf -g 2U
	
html: fixedpointmath_trace.html
	xdg-open fixedpointmath_trace.html &
	
clean:
	rm *.html
	rm *.dgb
