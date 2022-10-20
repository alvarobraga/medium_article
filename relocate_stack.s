		AREA |.text|,CODE,READONLY
		EXPORT __relocate_stack
			
__relocate_stack
		POP {R0}
		POP {R1}
		LDR R2,=0x20005E94 ;First address of sampling vector (0x20000000) + SAMPLING_SIZE * 4 + (SAMPLING_SIZE * 4 + 50 * 4)
		MOV SP,R2
		PUSH {R1}
		PUSH {R0}
		B   STOP

STOP
        BX		LR
		
		ALIGN
		
		END