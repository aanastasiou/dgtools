hellosum_output_trace.html:hellosum.dgb
	dgsim.py hellosum.dgb -mn 100 -otf hellosum_output_trace.html -t 'Hello World' --with-dump

hellosum.dgb:hellosum.dsf
	dgasm.py hellosum.dsf -o hellosum.dgb

html:hellosum_output_trace.html
	xdg-open hellosum_output_trace.html

clean:
	 rm *.dgb
	 rm *.html
	 rm *.css
