// Runs an infinite loop that listens to the keyboard input.

// reset screen address
(START)
    @SCREEN // screen address
    D=A
    @R0
    M=D     // store screen start address in R0

// main loop to check keyboard RAM
(MAIN)
    @KBD
    D=M     // load the value in KBD address
    @BLACK
    D;JNE   // jump to black loop if not 0

// loop to set white to a pixel
(WHITE)
    D=0
    @SET
    0;JMP   // jump to set

// loop to set black to a pixel
(BLACK)
    D=-1

(SET) 
    @R0     // get the curr screen pixel address
    A=M 
    M=D     // set the screen pixel

    @R0
    M=M+1   // Increment the address for next pixel

    @KBD    // KBD address is the last screen reg
    D=A
    @R0
    D=D-M   // decrement the pixel reg address
    
    @START
    D;JLE   // if all pixels are filled; reset

    @MAIN
    0;JMP // Continue the fill screen loop