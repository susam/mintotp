Toy TOTP Generator
==================

This is a tiny toy TOTP generator.

[![View Source][Source SVG]][Source File]
[![MIT License][License SVG]][L]

[Source SVG]: https://img.shields.io/badge/view-source-brightgreen.svg
[Source File]: totp.py
[License SVG]: https://img.shields.io/badge/license-MIT-blue.svg
[L]: LICENSE.md


Contents
--------

* [Introduction](#introduction)
* [Get Started](#get-started)
  * [With Base32 Key](#with-base32-key)
  * [With QR Code](#with-qr-code)
* [Usage](#usage)
* [Caution](#caution)
* [License](#license)


Introduction
------------

TOTP stands for Time-based One-Time Password. At the heart of the TOTP
algorithm lies the HOTP algorithm. HOTP stands for HMAC-based One-Time
Password. Here are the relevant RFCs to learn more about these
algorithms:

  - [RFC 2104]: HMAC: Keyed-Hashing for Message Authentication
  - [RFC 4226]: HOTP: An HMAC-Based One-Time Password Algorithm
  - [RFC 6238]: TOTP: Time-Based One-Time Password Algorithm

[RFC 2104]: https://tools.ietf.org/html/rfc2104
[RFC 4226]: https://tools.ietf.org/html/rfc4226
[RFC 6238]: https://tools.ietf.org/html/rfc6238

The source code in [totp.py](totp.py) contains toy code to show how TOTP
values are generated from a secret key and current time. It's just 26
lines of code (actually 18 lines if we ignore the shebang and blank
lines). There are no comments in the code, so a brief description of the
code is presented in this section. Here is the entire code presented
once again for convenience:

```python
#!/usr/bin/python3

import base64
import hmac
import struct
import sys
import time


def hotp(secret, counter, digits=6, digest='sha1'):
    padding = '=' * ((8 - len(secret)) % 8)
    secret_bytes = base64.b32decode(secret.upper() + padding)
    counter_bytes = struct.pack(">Q", counter)
    mac = hmac.new(secret_bytes, counter_bytes, digest).digest()
    offset = mac[-1] & 0x0f
    truncated = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(truncated)[-digits:].rjust(digits, '0')


def totp(secret, interval=30):
    return hotp(secret, int(time.time() / interval))


if __name__ == '__main__':
    for secret in sys.argv[1:]:
        print(totp(secret))
```

In the code above, we use the `hmac` module available in the Python
standard library to implement HOTP. The implementation can be found in
the `hotp()` function. It is a pretty straightforward implementation of
[RFC 2104: Section 5: HOTP Algorithm][RFC 2104-5]. It takes a
Base32-encoded secret key and a counter as input. It returns a 6-digit
HOTP value.

The `totp()` function implements the TOTP algorithm. It is a thin
wrapper around the HOTP algorithm. The TOTP value is obtained by
invoking the HOTP function with the secret key and the number of time
intervals (30 second intervals by default) that have elapsed since Unix
epoch (1970-01-01 00:00:00 UTC).

[RFC 2104-5]: https://tools.ietf.org/html/rfc4226#section-5


Get Started
-----------

### With Base32 Key

 1. Enter this command:

        python3 totp.py ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS

    The output should be a 6-digit TOTP value.

 2. If you have Google Authenticator on your mobile phone, open it, tap
    its add button (`+` sign), select "Enter a provided key", enter any
    account name and "Time-based" and enter the following key:

        ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS

     Set the dropdown menu to "Time-based" and tap the "Add" button. A
     6-digit TOTP value should appear for the new key.

 3. Run the command in step 1 again and verify that the TOTP value
    printed by the Python script matches the TOTP value that appears in
    Google Authenticator.


### With QR Code

 1. Install `zbarimg` to scan QR codes:

    ```shell
    # On macOS
    brew install zbar

    # On Debian, Ubuntu, etc.
    apt-get install zbar-tools
    ```

 2. Download and save the following QR code on your system:\
    [![QR code for TOTP secret key](secret1.png)](secret1.png)\
    The QR code above can also be found in this file:
    [secret1.png](secret1.png).

 3. Enter this command to data in the QR code:


    ```shell
    zbarimg -q secret1.png
    ```

    The output should be:

    ```
    QR-Code:otpauth://totp/alice:bob?secret=ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
    ```

    Note that the secret key in the URI is same as the secret key we
    used in the previous section.

 4. Now enter this command to extract the secret key from the QR code
    and feed it to the Python script.

    ```shell
    python3 totp.py $(zbarimg -q secret1.png | sed 's/.*secret=\([^&]*\).*/\1/')
    ```

 5. If you have Google Authenticator on your mobile phone, open it, tap
    its add button (`+` sign), select "Scan a barcode", and scan the QR
    code shown above in step 3. A 6-digit TOTP value should appear for
    the new key.

 6. Run the command in step 3 again and verify that the TOTP value
    printed by the Python script matches the TOTP value that appears in
    Google Authenticator.


Usage
-----

The script [totp.py](totp.py) accepts one or more Base32 secret keys as
command line arguments and generates TOTP values from the secret keys.
Here are a few examples:

 1. Generate multiple TOTP values, one for each of multiple Base32 keys:

    ```shell
    python3 totp.py ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS PW4YAYYZVDE5RK2AOLKUATNZIKAFQLZO
    ```

 2. Generate TOTP values for multiple keys in multiple QR codes:

    ```shell
    python3 totp.py $(zbarimg -q *.png | sed 's/.*secret=\([^&]*\).*/\1/')
    ```

 3. Generate TOTP value for a key and copy it to clipboard :wink: on macOS:

    ```shell
    python3 totp.py ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS | pbcopy
    ```

 4. Generate TOTP value for a key, print it, and copy it to clipboard on
    macOS.

    ```shell
    python3 totp.py ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS | tee /dev/stderr | pbcopy
    ```


Caution
-------

This project is only a proof of concept to demonstrate how TOTP values
are generated. It can be tempting to use this to generate TOTP values on
a desktop/laptop device while logging into a website that requires
TOTP-based two-factor authentication from the same device. However,
doing so defeats the purpose of two-factor authentication (2FA). If your
desktop/laptop device is compromised, then both authentication factors
would be compromised. The attacker can steal the first authentication
factor that only you should know (e.g., password) by running a key
logger on the compromised device. The attacker can also steal the second
authentication factor that only you should have (e.g., TOTP secret key)
because it would be read by this script on the same compromised device;
if this script can read the TOTP secret key on the compromised device,
so can the attacker.


License
-------

This is free and open source software. You can use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of it,
under the terms of the MIT License. See [LICENSE.md][L] for details.

This software is provided "AS IS", WITHOUT WARRANTY OF ANY KIND,
express or implied. See [LICENSE.md][L] for details.


Thanks
------

Thanks to [Prateek Nischal][PN] for getting me involved with TOTP. I
referred to his TOTP implementation at
[prateeknischal/qry/util/totp.py][PNTOTP] while writing my own.

[PN]: https://github.com/prateeknischal
[PNTOTP]: https://github.com/prateeknischal/qry/blob/master/util/totp.py
