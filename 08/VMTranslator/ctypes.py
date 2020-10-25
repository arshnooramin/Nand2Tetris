# command type enumerations
ARITHMETIC = 0
PUSH = 2
POP = 3
LABEL = 4
GOTO = 5
IF = 6
FUNCTION = 7
RETURN = 8
CALL = 9

# arithmetic type enumerations
UN_OP = 10      # not, neg
BI_OP = 11      # add, sub, and, or
COMP = 12       # eq, lt, gt

# push/pop groups and type enumeration
GROUP_1 = 13    # this, local, argument, that, temp
GROUP_2 = 14    # static, pointer
CONSTANT = 15   # constant
