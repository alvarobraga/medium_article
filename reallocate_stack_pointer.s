		AREA |.text|,CODE,READONLY
		EXPORT __reallocate_stack
			
__reallocate_stack
		;First address of sampling vector (0x20000000) + SAMPLING_SIZE * 4 + (SAMPLING_SIZE * 4 + 50 * 4)
		LDR R0,=0x20005E94
		MOV SP,R0
		B   STOP

STOP
        BX		LR
		
		ALIGN
		
		END