SUST_CODE=sust_code.ssf

sust_code.dsf: $(SUST_CODE)
	dgsust.py $(SUST_CODE)>sust_code.dsf
		
sust_code.dgb:sust_code.dsf
	dgasm.py sust_code.dsf -g 2U 

sust_code_trace.html:sust_code.dgb
	@tape_offset=$$((252 - `dginspect.py sust_code.dgb|egrep -o -e "'stack': [0-9]+"|sed -e "s/'stack': //"`)); \
	dgsim.py sust_code.dgb --title "$(SUST_CODE)" -mn 4000 -I -ts head_ptr -ts head_val -ts head_val_1 -ts stack:$$tape_offset --theme plain

html:sust_code_trace.html
	xdg-open sust_code_trace.html
	
clean:
	rm sust_code.dsf
	rm *.dgb
	rm sust_code_trace.html
	rm *.css
	rm *.hex
