#ifndef ARCANE_VM_H
#define ARCANE_VM_H

typedef enum {
    OP_NOP = 0x00,
    OP_PUSH_NULL = 0x01,
    OP_PUSH_NUMBER = 0x02,
    OP_PUSH_STRING = 0x03,
    OP_POP = 0x04,
    OP_ADD = 0x05,
    OP_SUB = 0x06,
    OP_MUL = 0x07,
    OP_DIV = 0x08,
    OP_MOD = 0x09,
    OP_EQ = 0x0A,
    OP_NEQ = 0x0B,
    OP_LT = 0x0C,
    OP_GT = 0x0D,
    OP_JMP = 0x0E,
    OP_JMP_IF = 0x0F,
    OP_CALL = 0x10,
    OP_RETURN = 0x11,
    OP_LOAD = 0x12,
    OP_STORE = 0x13,
    OP_ALLOCATE = 0x14,
    OP_FREE = 0x15,
    OP_CREATE_FUNCTION = 0x16,
    OP_CREATE_ARRAY = 0x17,
    OP_GET_ELEMENT = 0x18,
    OP_SET_ELEMENT = 0x19,
    OP_NATIVE_CALL = 0x1A,
    OP_CREATE_REFERENCE = 0x1B,
    OP_EXIT = 0x1C
} OpCode;

#endif 