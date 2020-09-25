// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// initialize R2 with 0
@R2
M=0

// check if R1 is zero
@R0
D=M
@END        // if it is jump to end
D;JEQ       // because product is 0

// check if R2 is zero
@R1
D=M
@END        // if it is jump to end
D;JEQ       // because product is 0

// Loops to add R1 to R2 R0 times
(LOOP)
    // increment R2 (product value) by R1
    @R2
    D=M     // load R2 value
    @R1
    D=D+M   // R2 + R1
    @R2
    M=D     // save the value back to R2

    // use R0 as a counter of loop
    @R0     
    D=M-1   // decrement it by 1 per iter
    M=D

    // loop runs until R0 is 0
    @LOOP
    D;JGT
(END)

@END
0;JMP // Infinite loop





