MinTOTP
=======

This is a minimal TOTP generator written in 19 lines of Python code.

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
  * [With Encrypted Base32 Key](#with-encrypted-base32-key)
  * [With QR Code](#with-qr-code)
  * [With Encrypted QR Code](#with-encrypted-qr-code)
  * [Multiple Keys](#multiple-keys)
* [Caution](#caution)
* [License](#license)


Introduction
------------

TOTP stands for Time-based One-Time Password. At the heart of the TOTP
algorithm lies the HOTP algorithm. HOTP stands for HMAC-based One-Time
Password. HMAC stands for Hash-based Message Authentication Code. Here
are the relevant RFCs to learn more about these algorithms:

  - [RFC 2104]: HMAC: Keyed-Hashing for Message Authentication
  - [RFC 4226]: HOTP: An HMAC-Based One-Time Password Algorithm
  - [RFC 6238]: TOTP: Time-Based One-Time Password Algorithm

[RFC 2104]: https://tools.ietf.org/html/rfc2104
[RFC 4226]: https://tools.ietf.org/html/rfc4226
[RFC 6238]: https://tools.ietf.org/html/rfc6238

The source code in [`totp.py`](totp.py) contains the code to show how
TOTP values are generated from a secret key and current time. It's just
26 lines of code (actually 18 lines if we ignore the shebang and blank
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
    for secret in sys.stdin:
        print(totp(secret.strip()))
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

This section presents a few examples to quickly get started with the
[`totp.py`](totp.py) program.

Note that this section uses a few example secret keys and QR codes. They
are merely examples that come with this project for you to quickly test
the program with. They should not be used for any real account that
requires TOTP-based two-factor authentication. Usually, the issuer of a
real account (such as an account on a website or an organization) would
also issue a secret key or secret QR code to you which you must use to
generate TOTP values for the purpose of logging into that account.


### With Base32 Key

 1. Enter this command:

    ```shell
    echo ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS | python3 totp.py
    ```

    The output should be a 6-digit TOTP value.

 2. Add the following key to a TOTP-based authenticator app:

    ```
    ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
    ```

    For example, if you have Google Authenticator on your mobile phone,
    open it, tap the button with plus sign, select "Enter a provided
    key", enter any account name and "Time-based" and enter the
    above key. Set the dropdown menu to "Time-based" and tap the "Add"
    button. A 6-digit TOTP value should appear for the new key.

 3. Run the command in step 1 again and verify that the TOTP value
    printed by the Python program matches the TOTP value that appears in
    the authenticator app.


### With Encrypted Base32 Key

While the previous example uses an example key to show how this tool
works, in case you decide to use this tool to generate TOTP values from
a real secret key for a real account, you must encrypt your secret key
to keep it safe.

The steps below show the usage of GPG to encrypt our example secret key.

 1. Install GNU Privacy Guard (also known as GnuPG or GPG):

    ```shell
    # On macOS
    brew install gnupg

    # On Debian, Ubuntu, etc.
    apt-get install gnupg
    ```

 2. Encrypt the secret key using GPG. First enter this command:

    ```shell
    gpg -c -o secret.gpg
    ```

    Then enter a [strong passphrase] when it prompts for it. Re-enter
    the passphase to confirm it. Then paste the following key as input:

    ```
    ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
    ```

    Press <kbd>Enter</kbd> to end the line. Press <kbd>control</kbd> +
    <kbd>d</kbd> to end input. The encrypted secret key would be saved
    in a file named `secret.gpg`.

 3. Generate TOTP value from the encrypted key:

    ```shell
    gpg -q -o - secret.gpg | python3 totp.py
    ```

 4. You can also generate TOTP value and copy it to system clipboard:

    ```shell
    # On macOS
    gpg -q -o - secret.gpg | python3 totp.py | pbcopy

    # On Linux
    gpg -q -o - secret.gpg | python3 totp.py | xclip
    ```

    Now you can easily paste the TOTP value to any login form that
    requires it. On Linux, of course, you need to have `xclip` installed
    to use it. On Debian, Ubuntu, etc. it can be installed with the
    `apt-get install xclip` command. To paste the value copied into the
    clipboard by `xclip`, middle-click on mouse.

 5. In case you want to see the TOTP value on the terminal while it is
    also copied to the system clipboard, use one of these commands:

    ```shell
    # On macOS
    gpg -q -o - secret.gpg | python3 totp.py | tee /dev/stderr | pbcopy

    # On Linux
    gpg -q -o - secret.gpg | python3 totp.py | tee /dev/stderr | xclip
    ```

[strong passphrase]: https://www.gnupg.org/faq/gnupg-faq.html#strong_passphrase


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

 3. Enter this command to read the data in the QR code:

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
    and feed it to the Python tool.

    ```shell
    zbarimg -q secret1.png | sed 's/.*secret=\([^&]*\).*/\1/' | python3 totp.py
    ```

 5. Scan the QR code shown above in step 3 with a TOTP-based
    authenticator app. For example, if you have Google Authenticator on
    your mobile phone, open it, tap the button with plus sign, select
    "Scan a barcode", and scan the QR code shown above in step 3. A
    6-digit TOTP value should appear for the new key.

 6. Run the command in step 3 again and verify that the TOTP value
    printed by the Python tool matches the TOTP value that appears in
    the authenticator app.


### With Encrypted QR Code

While the previous example uses an example QR code to show how this tool
works, in case you decide to use this tool to generate TOTP values from
a real QR code for a real account, you must encrypt your QR code to keep
it safe.

The steps below show the usage of GPG to encrypt our example QR code.

 1. Install GNU Privacy Guard (also known as GnuPG or GPG):

    ```shell
    # On macOS
    brew install gnupg

    # On Debian, Ubuntu, etc.
    apt-get install gnupg
    ```

 2. Encrypt the QR code using GPG. First enter this command:

    ```shell
    gpg -c secret1.png
    ```

    Then enter a [strong passphrase] when it prompts for it. Re-enter
    the passphase to confirm it. The encrypted QR code would be saved in
    a file named `secret1.png.gpg`.

 3. Delete the unencrypted QR code file securely:

    ```shell
    # On macOS
    rm -P secret1.png

    # On Linux
    shred -u secret1.png
    ```

 4. Generate TOTP value from the encrypted QR code file:

    ```shell
    zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/' | python3 totp.py
    ```

 4. You can also generate the TOTP value and copy it to system clipboard:

    ```shell
    # On macOS
    zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/' | python3 totp.py | pbcopy

    # On Linux
    zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/' | python3 totp.py | xclip
    ```

 5. In case you want to see the TOTP value on the terminal while it is
    also copied to the system clipboard, use one of these commands:

    ```shell
    # On macOS
    zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/' | python3 totp.py | tee /dev/stderr | pbcopy

    # On Linux
    zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/' | python3 totp.py | tee /dev/stderr | xclip
    ```

### Multiple Keys

This tool accepts one or more Base32 secret keys as standard input. Each
key must occur in its own line.

 1. Generate multiple TOTP values, one for each of multiple Base32 keys:

    ```shell
    python3 totp.py <<eof
    ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
    PW4YAYYZVDE5RK2AOLKUATNZIKAFQLZO
    eof
    ```

 2. Generate TOTP values for multiple keys in multiple QR codes:

    ```shell
    zbarimg -q *.png | sed 's/.*secret=\([^&]*\).*/\1/' | python3 totp.py
    ```


Caution
-------

It can be tempting to use this tool to generate TOTP values on a
desktop/laptop device while logging into a website that requires
TOTP-based two-factor authentication from the same device. One should be
aware that this trades some security for convenience.

Two-factor authentication (2FA) relies on the user presenting two pieces
of evidence (factors) to an authentication system: something only the
user knows and something only the user has.

If this tool is run to generate TOTP values on the same desktop/laptop
device that you are using to log into a website, then you should
consider that if your desktop/laptop device is compromised, then both
authentication factors can be compromised. The attacker can steal the
first authentication factor that only you should know (e.g., password)
by running a key logger on the compromised device. The attacker can also
steal the second authentication factor that only you should have (e.g.,
TOTP secret key) because it would be read by this tool on the same
compromised device; if this tool can read the TOTP secret key on the
compromised device, so can the attacker.

Having clarified that, it is still safer to have 2FA than not have it at
all. Whether trading some security for convenience is acceptable to you
or not is something you need to decide for yourself.


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
