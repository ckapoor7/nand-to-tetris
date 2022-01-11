// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(LOOP)
        @SCREEN
        D = A
        @R1
        M = D // set RAM[1] to screen value

(KEYBOARD)
        @KBD
        D = M
        @ON
        D; JGT
        @OFF
        D; JEQ

        @KEYBOARD
        0; JMP 

(ON)
        @R0
        M = -1 // 16-bit 1 (2s complement)
        @DRAW
        0; JMP

(OFF)
        @R0
        M = 0
        @DRAW
        0; JMP

(DRAW)
        @R0
        D = M // get value of R0 set from either on/off

        @R1
        A = M // address of pixel
        M = D // set to either on/off

        @R1
        D = M + 1
        @KBD
        D = A - D // get address of next pixel

        @R1
        M = M + 1 // increase pixel value
        A = M

        @DRAW
        D; JGT // loop till A > 0 (exit otherwise)

        @LOOP
        0; JMP // infinite loop





