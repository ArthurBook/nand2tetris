// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(MAINLOOP)
  @KBD
  D=M
  @ONKEYPRESS
  D;JNE
  @NOKEYPRESS
  0;JMP

// Set color to black and call write screen
(ONKEYPRESS)
  @color
  M=-1
  @WRITE_SCREEN
  0;JMP

// Set color to white and call write screen
(NOKEYPRESS)
  @color
  M=0
  @WRITE_SCREEN
  0;JMP

// Grab pointer to screen address and enter write loop
(WRITE_SCREEN)
  @SCREEN
  D=A
  @R1
  M=D 
  @24576
  D=A
  @R2
  M=D
  @WRITE_LOOP
  0;JMP

(WRITE_LOOP)
  @R1
  D=M
  @R2
  D=D-M
  @END_WRITE
  D;JGE

  @color
  D=M
  @R1
  A=M
  M=D

  @R1
  M=M+1
  @WRITE_LOOP
  0;JMP

(END_WRITE)
  @MAINLOOP
  0;JMP
