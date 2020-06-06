int2str_trace.html:int2str.dgb
	dgsim.py int2str.dgb --with-dump -t 'uint8 to string conversion' -ts R0 -ts ascii_str:3
	
int2str.dgb:int2str.dsf
	dgasm.py int2str.dsf

clean:
	rm *.dgb *.html

html:int2str_trace.html
	xdg-open int2str_trace.html
