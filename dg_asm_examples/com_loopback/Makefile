com_loopback_trace.html:com_loopback.dgb
	dgsim.py com_loopback.dgb -mn 20 -otf com_loopback_trace.html -t 'com_loopback.dsf' -I

com_loopback.dgb:com_loopback.dsf
	dgasm.py com_loopback.dsf -o com_loopback.dgb -g 2U

html:com_loopback_trace.html
	xdg-open com_loopback_trace.html

clean:
	 rm *.dgb
	 rm *.html
	 rm *.css
