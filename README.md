# 8-Bit Microcoded CPU

An 8-bit CPU built in LogicCircuit, with a custom instruction set, a Python assembler, and annotated demonstrations of instruction execution.

The project connects the full execution path: writing an assembly program, generating machine code, fetching instructions from memory, and executing them through microcode-controlled hardware. Register probes and a decimal display make the results easy to inspect.

## Features

- **Data transfer:** Move immediate values, register contents, and memory data.
- **Memory access:** Read and write memory using direct and register-indirect addressing.
- **Arithmetic:** Addition, subtraction, increment, and decrement.
- **Bitwise logic:** AND, OR, XOR, and NOT.
- **Program control:** Comparisons, conditional branches, and unconditional jumps.
- **Execution control:** Reset, continuous execution, manual stepping, and halt.
- **Python toolchain:** Assemble programs and generate the control ROM image.

## Architecture

| Component | Configuration |
| --- | --- |
| Data path | 8-bit |
| Program counter | 8-bit |
| Main memory | 64 KiB, with 16-bit addresses and 8-bit data |
| Machine instruction | 3 bytes: `IR`, `DST`, `SRC` |
| Microinstruction | 32-bit |
| Control store | 65,536 × 32 bits, or 256 KiB |
| Microcode address | 8-bit instruction + 4-bit status + 4-bit cycle |

The CPU includes a shared bus, an ALU, a microprogrammed control unit, RAM, and registers for instruction processing and data storage.

Memory addresses use separate high and low 8-bit fields. The program counter itself is 8-bit.

**Register behavior:** `A` and `B` also serve as ALU input registers. Arithmetic and logic instructions may overwrite them, so programs should account for these side effects.

The `D` register is connected to a decimal display. Register probes show hexadecimal values, allowing the two representations to be compared directly.

## Instruction Set

The verified demonstrations cover the following instructions:

| Category | Instructions |
| --- | --- |
| Data transfer and memory access | `MOV` |
| Arithmetic | `ADD`, `SUB`, `INC`, `DEC` |
| Bitwise logic | `AND`, `OR`, `XOR`, `NOT` |
| Comparison | `CMP` |
| Branching | `JMP`, `JNZ` |
| Execution control | `HLT` |

The instruction definitions also include `NOP`, `JZ`, `JO`, `JNO`, `JP`, and `JNP`. `JP` and `JNP` use the parity flag.

### Addressing Modes

| Mode | Example |
| --- | --- |
| Immediate | `MOV D, 10` |
| Register | `MOV C, D` |
| Direct memory | `MOV D, [0x80]` |
| Register-indirect memory | `MOV D, [B]` |

Legal operand combinations depend on the instruction. For example, arithmetic instructions accept a register destination and an immediate or register source.

The assembler currently recognizes `A`, `B`, `C`, `D`, `SS`, `CS`, and `SP`.

## Project Files

```text
CPU.CircuitProject    CPU circuit and embedded memory contents
compiler.py           Assembly parser and machine-code generator
assembly.py           Instruction definitions and micro-operation sequences
controller.py         Control ROM image generator
pin.py                Control-signal definitions and register identifiers
build.py              Runs the microcode generator and assembler
program.asm           Assembly source program
program.bin           Generated program image
micro.bin             Generated control ROM image
image_to_vga_bin.py   Image-to-ROM data conversion utility
```

## Getting Started

### Requirements

- LogicCircuit
- Python 3

### Assemble and Run a Program

1. Open `CPU.CircuitProject` in LogicCircuit.
2. Replace the contents of `program.asm` with a short test program:

   ```asm
   MOV D, 0x0A
   ```

3. Generate the program image:

   ```bash
   python compiler.py
   ```

4. Load `program.bin` into the main RAM's initial contents, starting at address `0x0000`.
5. Start the circuit simulation, enable CPU execution with `POW`, and reset as needed.
6. Inspect the register probes and decimal display.

The expected result is:

```text
D register:     0x0A
Decimal output: 10
```

The assembler automatically appends `HLT` to the program.

## Example Programs

### Arithmetic

```asm
MOV D, 10
ADD D, 5
MOV C, D
SUB D, 3
INC D
DEC D
```

Final results:

```text
C = 15
D = 12
```

`C` preserves the addition result while `D` continues through the remaining operations.

### Memory Access

```asm
MOV [0x80], 10
MOV A, [0x80]
MOV B, 0x80
MOV C, [B]
MOV [B], 0x2A
MOV D, [0x80]
MOV [0x81], C
```

Final results:

```text
A = 10
B = 0x80
C = 10
D = 42

RAM[0x80] = 42
RAM[0x81] = 10
```

This demonstrates direct reads, indirect reads and writes, and storing a register value in memory.

### Comparison and Branching

```asm
MOV D, 0
MOV C, 3

LOOP:
INC D
DEC C
CMP C, 0
JNZ LOOP

JMP DONE
MOV D, 99

DONE:
```

The loop runs three times, leaving `D = 3` and `C = 0`. The final jump skips `MOV D, 99`.

Labels must appear on their own lines and end with a colon.

## Assembler and Microcode

Each machine instruction occupies three bytes:

```text
[ IR ][ DST ][ SRC ]
```

For example:

```text
MOV D, 0x0A  →  84 0B 0A
HLT          →  3F 00 00
```

`compiler.py` removes comments, parses operands, resolves labels, checks addressing combinations, and writes the encoded bytes to `program.bin`.

The CPU fetches each instruction in six microsteps:

```text
1. PC  → MAR
2. RAM → IR,  PC + 1
3. PC  → MAR
4. RAM → DST, PC + 1
5. PC  → MAR
6. RAM → SRC, PC + 1
```

The control unit then selects the instruction's execution sequence.

To regenerate the control ROM image:

```bash
python controller.py
```

`build.py` runs both the microcode generator and the assembler:

```bash
python build.py
```

## Current Limitations

- Stack instruction definitions and the circuit's embedded microcode still need to be synchronized. `PUSH` and `POP` are outside the verified demonstrations. Check version consistency before replacing the control ROM.
- Numeric operands are encoded in one byte. Use values from `0` to `255`; negative literal syntax is not implemented.
- Some hardware registers are not yet exposed through the assembler.
- The project includes a separate 100 × 100 image-display circuit and an image conversion utility. This display circuit is not connected to the CPU data path.

## Documentation

The accompanying project manual includes annotated circuit screenshots, test programs, expected results, and explanations of the assembler and control logic.
