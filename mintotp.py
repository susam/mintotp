#!/usr/bin/python3

import base64
import hmac
import struct
import sys
import time


def hotp(key, counter, digits=6, digest='sha1'):
    padding = '=' * ((8 - len(key)) % 8)
    key_bytes = base64.b32decode(key.upper() + padding)
    counter_bytes = struct.pack(">Q", counter)
    mac = hmac.new(key_bytes, counter_bytes, digest).digest()
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-digits:].rjust(digits, '0')


def totp(key, time_step=30):
    return hotp(key, int(time.time() / time_step))


def main():
    for key in sys.stdin:
        print(totp(key.strip()))


if __name__ == '__main__':
    main()
