#!/usr/bin/python3

import base64
import hmac
import struct
import sys
import time


def hotp(secret, counter, digits=6, algo='sha1'):
    padding = '=' * ((8 - len(secret)) % 8)
    secret_bytes = base64.b32decode(secret.upper() + padding)
    counter_bytes = struct.pack(">Q", counter)
    mac = hmac.digest(secret_bytes, counter_bytes, algo)
    offset = mac[-1] & 0x0f
    truncated = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(truncated)[-digits:].rjust(digits, '0')


def totp(secret, interval=30):
    return hotp(secret, int(time.time() / interval))


if __name__ == '__main__':
    for secret in sys.argv[1:]:
        print(totp(secret))
