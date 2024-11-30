// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

(INIT)
  @R0 // R0 register
  D=M
  
  @i  // Variable holding iteration number of add loop
  M=D

  @R2 // Initialize result registry
  M=0

// Inplace add (subtract) from R1 to (from) R2 <R1>times 
(ITER)
  @i
  D=M

  @INCRPOSITIVE
  D; JGT

  @INCRNEGATIVE
  D; JLT

// Infinite loop when we are done (i == 0)
(END)
  @END
  0; JMP

// Increment the i registry and GOTO subtract
(INCRPOSITIVE)
  @i 
  M=M-1
  @ADDSELF
  0; JMP

// Increment the i registry and GOTO subtract
(INCRNEGATIVE)
  @i 
  M=M+1
  @SUBSELF
  0; JMP // Continue back to the addition loop

// Inplace add R1 to the result registry
(ADDSELF)
  @R1
  D=M
  @R2
  M=M+D
  @ITER
  0; JMP 

// Inplace subtract R1 from the result registry
(SUBSELF)
  @R1
  D=M
  @R2
  M=M-D
  @ITER
  0; JMP 

  
