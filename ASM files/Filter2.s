;Changes: lines 15, 26, 81-82, 97-98, 110-111

NUM_SAMPLES EQU 2000

        PRESERVE8
		AREA |.text|,CODE,READONLY
		EXPORT Filter
			
Filter
		;save the address of the variables Data->samples,Data->rms_squared and Data->gain into the stack for later use
		PUSH	{R1}
		PUSH	{R0}
		PUSH    {R2}
		PUSH    {R3}
		
        ;Enable FPU
		LDR		R2,=0xE000ED88
		LDR		R3,[R2]
		ORR		R3,R3,#(0xF<<20)
		STR		R3,[R2]
		
		DSB
		ISB
		
		POP     {R4}
		
		ADRL           R6,Coefficients   ;Load the address of Coefficients into R6
		POP            {R2}              ;Retrieve the address of Data->gain
		LDR            R3,[R2]           ;Load the value of Data->gain into R3
		VMOV.F32       S8,R3             ;Load the value of Data->gain into S8
			
		LDR		       R1,[R0]           ;Load the value pointed by R0 into R1
		LDR 	       R3,=0             ;Reset the loop counter	
		ADD            R3,R3,#1          ;Increment counter
		
;*** Calculate the offset (or mean value) of the samples
CALC_OFFSET  
		ADD		       R0,R0,#4          ;Move to next element in the sampling vector
		LDR		       R2,[R0]           ;Load the value pointed by R0 into R1
        ADD		       R1,R1,R2          ;x[n] + x[n-1] + x[n-2] + ... + x[n - (NUM_SAMPLES - 1)]
		ADD            R3,R3,#1
        CMP            R3,#NUM_SAMPLES   ;Check if it has reached the last element in the sampling vector
		POPHS          {R0}              ;If yes, restore initial value of R0 into R0 for next loop
		LDRHS          R3,=0             ;If yes, reset the counter for next loop
		VMOVHS.F32	   S7,R1             ;If yes, move the total sum to S7
		VCVTHS.F32.U32 S7,S7             ;If yes, convert total sum to IEEE 754 float point
		VLDRHS.F32     S1,[R6,#20]       ;If yes, load constant N (inverse of number of samples) into register S1
		VMULHS.F32     S7,S7,S1          ;If yes, perform offset = ( x[n] + x[n-1] + x[n-2] + ... + x[n - (NUM_SAMPLES - 1)] ) / NUM_SAMPLES
        BHS			   LOOP              ;If yes, go to LOOP
        BLO            CALC_OFFSET       ;If no, repeat CALC_OFFSET loop
		
;*** Apply filter
LOOP
		LDR		       R1,[R0]           ;R0 holds the memory address of the array samples[1000], passed as argument in the C program
		VMOV.F32	   S0,R1             ;S0 = x[n]
        VCVT.F32.U32   S0,S0             ;Convert x[n] from int32_t to float IEEE 754
		VSUB.F32       S0,S0,S7          ;Take offset from each sample
		VMOV.F32       S9,S0             ;Save x[n] into S9      
		VLDR.F32       S1,[R6]           ;Load coefficient a0 into auxiliary register S1
        VMUL.F32       S1,S1,S8          ;Apply gain	
		VMUL.F32       S0,S0,S1          ;a0*x[n]		
		CMP            R3,#1	         ;Check if the loop is at its first iteration			
        BLO            LOOP_ZERO         ;If loop counter less than 1, jump to tag LOOP_ZERO (i.e. n=0, so any element [n-1] or [n-2] are zero). Continue otherwise		
		VLDRHS.F32     S1,[R6,#4]        ;Load coefficient a1 into auxiliary register S1
        VMUL.F32       S1,S1,S8          ;Apply gain		
		VMULHS.F32     S1,S2,S1          ;a1*x[n-1]
		VADDHS.F32     S0,S0,S1          ;a0*x[n] + a1*x[n-1]
		VLDRHS.F32     S1,[R6,#8]        ;Load coefficient a2 into auxiliary register S1
		VMUL.F32       S1,S1,S8          ;Apply gain
		VMULHS.F32     S1,S3,S1          ;a2*x[n-2]
		VADDHS.F32     S0,S0,S1          ;a0*x[n] + a1*x[n-1] + a2*x[n-2]
		VLDRHS.F32     S6,[R6,#12]       ;Load coefficient b1 into auxiliary register S6
		VMULHS.F32     S1,S11,S6         ;b1*y[n-1]
		VADDHS.F32     S0,S0,S1          ;a0*x[n] + a1*x[n-1] + a2*x[n-2] + b1*y[n-1]		
		BEQ            LOOP_ONE	         ;If loop counter is equal to 1, jump to tag LOOP_ONE. Continue otherwise		
		VLDRHS.F32     S6,[R6,#16]       ;Load coefficient b2 into auxiliary register S6
		VMULHS.F32     S1,S12,S6         ;b2*y[n-2]
		VADDHS.F32     S0,S0,S1          ;a0*x[n] + a1*x[n-1] + a2*x[n-2] + b1*y[n-1] + b2*y[n-2]
		VPUSH.F32      {S0}              ;Save y[n] into stack	
		VSTR.F32       S0,[R4]           ;Store filtered value
		ADD            R4,R4,#4          ;Increment pointer
		VMOV.F32       S12,S11           ;y[n-1] becomems y[n-2]
		VMOV.F32       S11,S0            ;y[n] becomes y[n-1]
		ADDHS		   R3,R3,#1          ;Increment loop counter		
		CMPHS          R3,#NUM_SAMPLES
		ADDNE		   R0,R0,#4          ;Since data is stored as Little Endian in ARM processors, adding 4 points to the next element in the array samples
		VMOVNE.F32     S3,S2             ;x[n-1] becomes x[n-2] for next loop
		VMOVNE.F32	   S2,S9             ;x[n] becomes x[n-1]
		BNE            LOOP		
		SUBEQ 	       R3,R3,#1          ;Decrement loop counter by one (since the loop range is NUM_SAMPLES - 1) 
        MOVEQ          R1,R3	         ;Save (NUM_SAMPLES - 1) into R1		
		BEQ            RMS_SQUARED
		
LOOP_ONE		
		VPUSH.F32      {S0}		         ;Save y[n] into stack	
        VSTR.F32       S0,[R4]           ;Store filtered value
        ADD            R4,R4,#4		     ;Increment pointer
		VMOV.F32       S12,S11           ;y[n-1] becomems y[n-2]
		VMOV.F32       S11,S0            ;y[n] becomes y[n-1]
		ADD		       R3,R3,#1          ;Increment loop counter
		ADD		       R0,R0,#4          ;Point to the next element in the array sample
		VMOV.F32       S3, S2            ;x[n-1] becomes x[n-2] for next loop
		VMOV.F32	   S2,S9             ;x[n] becomes x[n-1]
		B			   LOOP              ;Inconditional jump back to tag LOOP
		
		
LOOP_ZERO
		VPUSH.F32     {S0}               ;Save y[n] into stack
        VSTR.F32      S0,[R4]            ;Store filtered value
        ADD           R4,R4,#4		     ;Increment pointer
		VMOV.F32      S11,S0             ;y[n] becomes y[n-1]
		VMOV.F32      S2,S9              ;x[n] becomes x[n-1]
		ADD		      R3,R3,#1           ;Increment loop counter
		ADD		      R0,R0,#4           ;Point to the next element in the sampling vector
		B		      LOOP               ;Inconditional jump back to tag LOOP
	

RMS_SQUARED
		CMP           R3,R1	             ;Now we will start a loop by decrementing the counter. Therefore we start by checking if the counter is (NUM_SAMPLES - 1)	
		BNE			  NOT_FIRST_LOOP_RMS_SQUARED
		VPOPEQ.F32    {S0}               ;Retrive y[loop counter] from stack
		VMULEQ.F32    S0,S0,S0           ;(y[(NUM_SAMPLES - 1))^2
		SUBEQ		  R3,R3,#1           ;Decrement loop counter
		B             RMS_SQUARED
		
NOT_FIRST_LOOP_RMS_SQUARED
		VPOP.F32    {S1}                 ;Retrive y[loop counter] from stack
		VMUL.F32    S1,S1,S1             ;y[(loop counter)])^2	
		VADD.F32    S0,S0,S1             ;(y[(NUM_SAMPLES - 1))^2 + y[(NUM_SAMPLES - 2)])^2 + ... + y[(loop counter)])^2		
		SUB		    R3,R3,#1             ;Decrement loop counter
		CMP         R3,#-1	             ;Check if loop counter is -1
		BGT         NOT_FIRST_LOOP_RMS_SQUARED
        VLDREQ.F32  S1,[R6,#20]	         ;Load constant N (inverse of number of samples) into register S1
		VMULEQ.F32  S0,S0,S1             ;SUM( (y[n])^2 ) * 1/N --- rms_squared
		POPEQ       {R1}                 ;Retrive address of the variable rms_squared from the stack
		VSTRHS.F32  S0,[R1]              ;Write rms squared value to variable rms_squared
		ALIGN
		BEQ         STOP      		
		
STOP
        BX		LR

Coefficients

		DCD     0x3CA4A8C1		;0.0251/1.2491 = 0.0201 -- coefficient a0
		DCD     0x3D24A8C1      ;0.0502/1.2491 = 0.0402 -- coefficient a1
		DCD     0x3CA4A8C1		;0.0251/1.2491 = 0.0201 -- coefficient a2
		DCD     0x3FC7CED9      ;1.9498/1.2491 = 1.5610 -- coefficient b1
		DCD     0xBF242C3D      ;-0.8011/1.2491 = -0.6413 -- coefficient b2
			
		DCD     0x3A03126F          ;1/2000. = 0.0005 -- complement of number of samples
			
		ALIGN		
		
		END