;Author: Alvaro Braga
;email: alvaro.braga3@gmail.com
;relocate_stack2.s: Relocate stack pointer

;Changes: line 13

		AREA |.text|,CODE,READONLY
		EXPORT __relocate_stack
			
__relocate_stack
		POP {R0}
		POP {R1}
		LDR R2, =0x20007DD0
		MOV SP,R2
		PUSH {R1}
		PUSH {R0}
		B   STOP

STOP
        BX		LR
		
		ALIGN
		
		END
