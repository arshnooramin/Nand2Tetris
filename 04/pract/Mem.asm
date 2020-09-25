
// fill first and last 16 pixel to black
@SCREEN     // get the first 16 pixels
M=-1        // set them to black

@KBD        // get screen end address
D=A         
@R0         // save address to RAM[0]        
M=D-1       // store the last 16 pixels

@R0         
D=M         // get the last 16 pixel address
A=D
M=-1        // set them to black

// continously check for keyboard inputs
(CHECK)
    @KBD
    D=M     // get keyboard input value
    @R1
    M=D     // store it in RAM[1]
    @CHECK
    0;JMP   // infinite loop