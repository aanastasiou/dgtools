rhud_trace.html:rhud.dgb
	dgsim.py rhud.dgb -mn 150 -otf rhud_trace.html -t 'rhud.dsf' -I --with-dump

rhud.dgb:rhud.dsf
	dgasm.py rhud.dsf -o rhud.dgb -g 2U

html:rhud_trace.html
	xdg-open rhud_trace.html

clean:
	 rm *.dgb
	 rm *.html
	 rm *.css
