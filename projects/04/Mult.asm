// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// RAM[2] = RAM[0] * RAM[1]

// set initial value to 0
@R2
M = 0

// check if value is > 0
@R0
D = M
@END
D; JEQ

// do the same thing for RAM[1]
@R1
D = M
@END
D; JEQ

// store the numbers being multiplied
@R0
D = M
@R3
M = D // RAM[3] = RAM[0]

(LOOP)
        @R1
        D = M
        @R2
        M = M + D // RAM[2] = RAM[1] + RAM[2]
        @R3
        M = M - 1 // repeat this RAM[0] times
        D = M

        @LOOP
        D; JGT // repeat till R3 > 0

(END)
        @END
        0; JMP // infinite loop 
