funcall_trace.html:funcall.dgb
	dgsim.py funcall.dgb --with-dump -t 'Function call convention' -ts stack:10 -ts R0

stack_trace.html:stack.dgb
	dgsim.py stack.dgb --with-dump -t 'A stack and its operations' -ts stack:10 -ts R0 -ts R1
	
funcall.dgb: funcall.dsf
	dgasm.py funcall.dsf

stack.dgb:stack.dsf
	dgasm.py stack.dsf

clean:
	rm *.dgb *.html

html:stack_trace.html funcall_trace.html
	xdg-open stack_trace.html
	xdg-open funcall_trace.html
