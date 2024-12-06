// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@COMP_eq_1_TRUE
D;JMP
@SP
A=M-1
M=0
@COMP_eq_1_END
0;JMP
(COMP_eq_1_TRUE)
@SP
A=M-1
M=-1
(COMP_eq_1_END)
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@COMP_eq_2_TRUE
D;JMP
@SP
A=M-1
M=0
@COMP_eq_2_END
0;JMP
(COMP_eq_2_TRUE)
@SP
A=M-1
M=-1
(COMP_eq_2_END)
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@COMP_eq_3_TRUE
D;JMP
@SP
A=M-1
M=0
@COMP_eq_3_END
0;JMP
(COMP_eq_3_TRUE)
@SP
A=M-1
M=-1
(COMP_eq_3_END)
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@COMP_lt_4_TRUE
D;JLT
@SP
A=M-1
M=0
@COMP_lt_4_END
0;JMP
(COMP_lt_4_TRUE)
@SP
A=M-1
M=-1
(COMP_lt_4_END)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@COMP_lt_5_TRUE
D;JLT
@SP
A=M-1
M=0
@COMP_lt_5_END
0;JMP
(COMP_lt_5_TRUE)
@SP
A=M-1
M=-1
(COMP_lt_5_END)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@COMP_lt_6_TRUE
D;JLT
@SP
A=M-1
M=0
@COMP_lt_6_END
0;JMP
(COMP_lt_6_TRUE)
@SP
A=M-1
M=-1
(COMP_lt_6_END)
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@COMP_gt_7_TRUE
D;JGT
@SP
A=M-1
M=0
@COMP_gt_7_END
0;JMP
(COMP_gt_7_TRUE)
@SP
A=M-1
M=-1
(COMP_gt_7_END)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@COMP_gt_8_TRUE
D;JGT
@SP
A=M-1
M=0
@COMP_gt_8_END
0;JMP
(COMP_gt_8_TRUE)
@SP
A=M-1
M=-1
(COMP_gt_8_END)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@COMP_gt_9_TRUE
D;JGT
@SP
A=M-1
M=0
@COMP_gt_9_END
0;JMP
(COMP_gt_9_TRUE)
@SP
A=M-1
M=-1
(COMP_gt_9_END)
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// neg
@SP
A=M-1
M=-M
// and
@SP
AM=M-1
D=M
A=A-1
M=M&D
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
AM=M-1
D=M
A=A-1
M=M|D
// not
@SP
A=M-1
M=!M
