BF_CODE=assign.bfc

bf_code.dsf:$(BF_CODE)
	dgbf.py $(BF_CODE)>bf_code.dsf
	
bf_code.dgb:bf_code.dsf
	dgasm.py bf_code.dsf -g 2U
	
bf_code_trace.html:bf_code.dgb
	@tape_offset=$$((252 - `dginspect.py bf_code.dgb|egrep -o -e "'tape': [0-9]+"|sed -e "s/'tape': //"`)); \
	dgsim.py bf_code.dgb -mn 1500 -I -ts dp -ts tape:$$tape_offset --theme plain
	
html:bf_code_trace.html
	xdg-open bf_code_trace.html

clean:
	rm bf_code.dsf
	rm *.hex
	rm *.dgb
	rm bf_code_trace.html
	rm *.css
