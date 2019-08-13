MinTOTP
=======

MinTOTP is a minimal TOTP generator written in Python.

[![View Source][Source SVG]][src]
[![PyPI Package][PyPI SVG]][pypi]
[![MIT License][License SVG]][L]
[![Build Status][Travis SVG]][travis]

[Source SVG]: https://img.shields.io/badge/view-source-brightgreen.svg
[src]: mintotp.py
[PyPI SVG]: https://img.shields.io/pypi/v/mintotp.svg
[License SVG]: https://img.shields.io/badge/license-MIT-blue.svg
[Travis SVG]: https://travis-ci.com/susam/mintotp.svg?branch=master
[travis]: https://travis-ci.com/susam/mintotp


Contents
--------

* [Introduction](#introduction)
* [Source Code](#source-code)
* [Install](#install)
  * [From PyPI](#from-pypi)
  * [From GitHub](#from-github)
* [Get Started](#get-started)
  * [With Base32 Key](#with-base32-key)
  * [With Encrypted Base32 Key](#with-encrypted-base32-key)
  * [With QR Code](#with-qr-code)
  * [With Encrypted QR Code](#with-encrypted-qr-code)
  * [Multiple Keys](#multiple-keys)
  * [Command Line Arguments](#command-line-arguments)
* [Tradeoff](#tradeoff)
* [Alternative: OATH Toolkit](#alternative-oath-toolkit)
* [Resources](#resources)
* [License](#license)
* [Thanks](#thanks)


Introduction
------------

TOTP stands for Time-Based One-Time Password. Many websites and services
require two-factor authentication (2FA) or multi-factor authentication
(MFA) where the user is required to present two or more pieces of
evidence:

  - Something only the user knows, e.g., password, passphrase, etc.
  - Something only the user has, e.g., hardware token, mobile phone, etc.
  - Something only the user is, e.g., biometrics.

A TOTP value serves as the second factor, i.e., it proves that the user
is in possession of a device (e.g., mobile phone) that contains a TOTP
secret key from which the TOTP value is generated. Usually the service
provider that provides a user's account also issues a secret key encoded
either as a Base32 string or as a QR code. This secret key is added to
an authenticator app (e.g., Google Authenticator) on a mobile device.
The app can then generate TOTP values based on the current time.
By default, it generates a new TOTP value every 30 seconds.

MinTOTP is a Python tool that can be used to generate TOTP values from a
secret key. Additionally, it exposes its functionality as module-level
functions for Python developers. It can be used on any system with
Python 3.4 or later installed on it.


Source Code
-----------

At the heart of the TOTP algorithm lies the HOTP algorithm. HOTP stands
for HMAC-based One-Time Password. HMAC stands for Hash-based Message
Authentication Code. Here are the relevant RFCs to learn more about
these algorithms:

  - [RFC 2104]: HMAC: Keyed-Hashing for Message Authentication
  - [RFC 4226]: HOTP: An HMAC-Based One-Time Password Algorithm
  - [RFC 6238]: TOTP: Time-Based One-Time Password Algorithm

[RFC 2104]: https://tools.ietf.org/html/rfc2104
[RFC 4226]: https://tools.ietf.org/html/rfc4226
[RFC 6238]: https://tools.ietf.org/html/rfc6238

The source code in [`mintotp.py`][src] generates TOTP values from a
secret key and current time. It's just 30 lines of code (actually 20
lines if we ignore the shebang and blank lines). There are no comments
in the code, so a brief description of the code is presented in this
section. Here is the entire code presented once again for convenience:

```python
#!/usr/bin/python3

import base64
import hmac
import struct
import sys
import time


def hotp(key, counter, digits=6, digest='sha1'):
    key = base64.b32decode(key.upper() + '=' * ((8 - len(key)) % 8))
    counter = struct.pack('>Q', counter)
    mac = hmac.new(key, counter, digest).digest()
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-digits:].rjust(digits, '0')


def totp(key, time_step=30, digits=6, digest='sha1'):
    return hotp(key, int(time.time() / time_step), digits, digest)


def main():
    args = [int(x) if x.isdigit() else x for x in sys.argv[1:]]
    for key in sys.stdin:
        print(totp(key.strip(), *args))


if __name__ == '__main__':
    main()
```

In the code above, we use the `hmac` module available in the Python
standard library to implement HOTP. The implementation can be found in
the `hotp()` function. It is a pretty straightforward implementation of
[RFC 2104: Section 5: HOTP Algorithm][RFC 2104-5]. It takes a
Base32-encoded secret key and a counter as input. It returns a 6-digit
HOTP value as output.

The `totp()` function implements the TOTP algorithm. It is a thin
wrapper around the HOTP algorithm. The TOTP value is obtained by
invoking the HOTP function with the secret key and the number of time
intervals (30 second intervals by default) that have elapsed since Unix
epoch (1970-01-01 00:00:00 UTC).

[RFC 2104-5]: https://tools.ietf.org/html/rfc4226#section-5


Install
-------

MinTOTP requires Python 3.4 or later. If Python 3.4 or later is present
on your system, follow one of the two sections below to get MinTOTP on
your system.


### From PyPI

If you want to install the MinTOTP package from [PyPI][pypi] as a Python
module on your system, then follow the steps provided below. Doing so
makes MinTOTP available as the `mintotp` command that you can run on the
terminal. A module named `mintotp` also becomes available that you can
`import` in your own Python code.

 1. Enter the following command to install MinTOTP on your system:

    ```shell
    pip3 install mintotp
    ```

 2. Test that MinTOTP works fine as a command:

    ```shell
    mintotp <<< ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
    ```

    A 6-digit TOTP value should appear as the output.

 3. Test that MinTOTP can be used as a library module:

    ```pycon
    $ python3
    >>> import mintotp
    >>> mintotp.totp('ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS')
    >>> mintotp.hotp('ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS', 42)
    ```

    The `totp()` function call should return a 6-digit TOTP value based
    on the current time. The `hotp()` call should return the following
    HOTP value: `626854`.


### From GitHub

If you do not want to install MinTOTP to your system as a command but
you want to work with the [`mintotp.py`][src] source file directly
clone the GitHub repository of this project.

 1. Clone GitHub repository of this project and enter its top-level
    directory.

    ```shell
    git clone https://github.com/susam/mintotp.git
    cd mintotp
    ```

 2. Test that [`mintotp.py`][src] works fine:

    ```shell
    python3 mintotp.py <<< ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
    ```

    A 6-digit TOTP value should appear as the output.

 3. Test that [`mintotp.py`][src] can be imported as a module:

    ```pycon
    $ python3
    >>> import mintotp
    >>> mintotp.totp('ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS')
    >>> mintotp.hotp('ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS', 42)
    ```

    The `totp()` function call should return a 6-digit TOTP value based
    on the current time. The `hotp()` call should return the following
    HOTP value: `626854`.

All examples provided in the sections below assume that MinTOTP has been
installed from PyPI. If you choose to use MinTOTP from GitHub instead,
replace all occurrences of `mintotp` in the example commands below with
`python3 mintotp.py`.


Get Started
-----------

This section presents a few examples to quickly get started with
MinTOTP.

Note that this section uses a few example secret keys and QR codes. They
are merely examples that come with this project for you to quickly test
the program with. They should not be used for any real account that
requires TOTP-based two-factor authentication. Usually, the issuer of a
real account (such as an account on a website or an organization) would
also issue a secret key or a secret QR code to you which you must use to
generate TOTP values for the purpose of logging into that account.


### With Base32 Key

 1. Enter this command:

    ```shell
    mintotp <<< ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
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

The previous section uses an example key to show how this tool works. If
you use this tool to generate TOTP values from a real secret key for a
real account, you must encrypt your secret key to keep it safe.

The steps below show the usage of GPG to encrypt our example secret key.
You would have to replace this example secret key with a real secret key
that you want to use to generate TOTP values.

 1. Install GNU Privacy Guard (also known as GnuPG or GPG):

    ```shell
    # On macOS
    brew install gnupg

    # On Debian, Ubuntu, etc.
    apt-get update
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

    Press <kbd>enter</kbd> to end the line. Press <kbd>control</kbd> +
    <kbd>d</kbd> to end input. The encrypted secret key would be saved
    in a file named `secret.gpg`.

 3. Generate TOTP value from the encrypted key:

    ```shell
    gpg -q -o - secret.gpg | mintotp
    ```

 4. You can also generate TOTP value and copy it to system clipboard:

    ```shell
    # On macOS
    gpg -q -o - secret.gpg | mintotp | pbcopy

    # On Linux
    gpg -q -o - secret.gpg | mintotp | xclip
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
    gpg -q -o - secret.gpg | mintotp | tee /dev/stderr | pbcopy

    # On Linux
    gpg -q -o - secret.gpg | mintotp | tee /dev/stderr | xclip
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
    used in the previous sections.

 4. Now enter this command to extract the secret key from the QR code
    and feed it to MinTOTP.

    ```shell
    zbarimg -q secret1.png | sed 's/.*secret=\([^&]*\).*/\1/' | mintotp
    ```

 5. Scan the QR code shown above in step 3 with a TOTP-based
    authenticator app. For example, if you have Google Authenticator on
    your mobile phone, open it, tap the button with plus sign, select
    "Scan a barcode", and scan the QR code shown above in step 3. A
    6-digit TOTP value should appear for the new key.

 6. Run the command in step 3 again and verify that the TOTP value
    printed by MinTOTP matches the TOTP value that appears in the
    authenticator app.


### With Encrypted QR Code

The previous example uses an example QR code to show how this tool
works. If you use this tool to generate TOTP values from a real QR code
for a real account, you must encrypt your QR code to keep it safe.

The steps below show the usage of GPG to encrypt our example QR code.
You would have to replace the example QR code with a real QR code that
you want to use to generate TOTP values.

 1. Install GNU Privacy Guard (also known as GnuPG or GPG):

    ```shell
    # On macOS
    brew install gnupg

    # On Debian, Ubuntu, etc.
    apt-get update
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
    zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/' | mintotp
    ```

 4. You can also generate the TOTP value and copy it to system clipboard:

    ```shell
    # On macOS
    zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/' | mintotp | pbcopy

    # On Linux
    zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/' | mintotp | xclip
    ```

 5. In case you want to see the TOTP value on the terminal while it is
    also copied to the system clipboard, use one of these commands:

    ```shell
    # On macOS
    zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/' | mintotp | tee /dev/stderr | pbcopy

    # On Linux
    zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/' | mintotp | tee /dev/stderr | xclip
    ```

### Multiple Keys

This tool accepts one or more Base32 secret keys as standard input. Each
key must occur in its own line.

 1. Generate multiple TOTP values, one for each of multiple Base32 keys:

    ```shell
    mintotp <<eof
    ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
    PW4YAYYZVDE5RK2AOLKUATNZIKAFQLZO
    eof
    ```

 2. Generate TOTP values for multiple keys in multiple QR codes:

    ```shell
    zbarimg -q *.png | sed 's/.*secret=\([^&]*\).*/\1/' | mintotp
    ```

### Command Line Arguments

In order to keep this tool as minimal as possible, it does not come with
any command line options. In fact, it does not even have the `--help`
option. It does support a few command line arguments though. Since there
is no help output from the tool, this section describes the command line
arguments for this tool.

Here is a synopsis of the command line arguments supported by this tool:

```
mintotp [TIME_STEP [DIGITS [DIGEST]]]
```

Here is a description of each argument:

  - `TIME_STEP`

    TOTP time-step duration (in seconds) during which a TOTP value is
    valid. A new TOTP value is generated after time-step duration
    elapses. (Default: `30`)

  - `DIGITS`

    Number of digits in TOTP value. (Default: `6`)

  - `DIGEST`

    Cryptographic hash algorithm to use while generating TOTP value.
    (Default: `sha1)

    Possible values are `sha1`, `sha224`, `sha256`, `sha384`, and
    `sha512`.

Here are some usage examples of these command line arguments:

 1. Generate TOTP value with a time-step size of 60 seconds:

    ```shell
    mintotp 60 <<< ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
    ```

 2. Generate 8-digit TOTP value:

    ```shell
    mintotp 60 8 <<< ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
    ```

 3. Use SHA-256 hash algorithm to generate TOTP value:

    ```shell
    mintotp 60 6 sha256 <<< ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
    ```

The behaviour of the tool is undefined if it is used in any way other
than what is described above. For example, although surplus command line
arguments are ignored currently, this behaviour may change in future, so
what should happen in case of surplus arguments is left undefined in
this document.


Tradeoff
--------

If you use this tool to generate TOTP values on a desktop/laptop device
while logging into a website that requires TOTP-based two-factor (2FA)
or multi-factor authentication (MFA) from the same device, you should be
aware that doing so trades off some security for convenience.

2FA or MFA relies on the user presenting at least two pieces of evidence
(factors) to an authentication system: something only the user knows and
something only the user has.

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

In other words, for higher security, it is good to generate TOTP values
on a separate device. However, if the inconvenience of getting a
separate device prevents you from using 2FA or MFA altogether, then you
might find this tool helpful. It allows to trade off some security for
convenience which is still more secure than not having 2FA or MFA at
all. Whether trading some security for convenience is acceptable to you
or not is something you need to decide for yourself.


Alternative: OATH Toolkit
-------------------------

There is an `oathtool` command available in OATH Toolkit that can also
generate TOTP values from TOTP secret keys. However, one of the issues
currently with `oathtool` is that it requires the secret key to be
provided as a command line argument which is generally insecure because
command line arguments are visible to all system users and processes.
See the following two posts to read more about this:

  - [Debian bug report: oathtool: has no secure way to provide a key][post1]
  - [OATH-Toolkit-help: oathtool should not require secret key on command line][post2]

[post1]: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=839278
[post2]: https://lists.gnu.org/archive/html/oath-toolkit-help/2012-01/msg00008.html

The `oathtool` command is intended to be used as a debugging tool and
not for generating real TOTP values for real accounts. It would remain
so until the issue described in the two URLs above is fixed. However, it
is still good to be aware that `oathtool` can do what MinTOTP does. This
section presents some examples about this:

 1. Install OATH Toolkit:

    ```shell
    # On macOS
    brew install oath-toolkit

    # On Debian, Ubuntu, etc.
    apt-get update
    apt-get install oathtool
    ```

 2. Generate TOTP from a Base32 key:

    ```shell
    oathtool --totp -b ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
    ```

 3. Generate TOTP from an encrypted Base32 key:

    ```shell
    oathtool --totp -b $(gpg -q -o - secret.gpg)
    ```

    Section [With Encrypted Base32 Key](#with-encrypted-base32-key)
    explains how to create the encrypted key (`secret.gpg`) with GPG.

 4. Generate TOTP from a QR code:

    ```shell
    oathtool --totp -b $(zbarimg -q secret1.png | sed 's/.*secret=\([^&]*\).*/\1/')
    ```

 5. Generate TOTP from an encrypted QR code:

    ```shell
    oathtool --totp -b $(zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/')
    ```

    Section [With Encrypted QR Code](#with-encrypted-qr-code) explains
    how to create the encrypted QR code (`secret1.png.gpg`) with GPG.

 6. Generate TOTP value and copy it to system clipboard:

    ```shell
    # On macOS
    oathtool --totp -b $(gpg -q -o - secret.gpg) | pbcopy
    oathtool --totp -b $(zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/') | pbcopy

    # On Linux
    oathtool --totp -b $(gpg -q -o - secret.gpg) | xclip
    oathtool --totp -b $(zbarimg -q <(gpg -q -o - secret1.png.gpg) | sed 's/.*secret=\([^&]*\).*/\1/') | xclip
    ```


Resources
---------

Here is a list of useful links about this project:

  - [Documentation](https://github.com/susam/mintotp#readme)
  - [Latest release][pypi]
  - [Changelog](https://github.com/susam/mintotp/blob/master/CHANGES.md)
  - [Issue tracker](https://github.com/susam/mintotp/issues)
  - [Source code](https://github.com/susam/mintotp)

[pypi]: https://pypi.org/project/mintotp/


License
-------

This is free and open source software. You can use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of it,
under the terms of the MIT License. See [LICENSE.md][L] for details.

This software is provided "AS IS", WITHOUT WARRANTY OF ANY KIND,
express or implied. See [LICENSE.md][L] for details.

[L]: LICENSE.md


Support
-------

To report bugs, suggest improvements, or ask questions, please create a
new issue at <http://github.com/susam/mintotp/issues>.


Thanks
------

Thanks to [Prateek Nischal][PN] for getting me involved with TOTP. I
referred to his TOTP implementation at
[prateeknischal/qry/util/totp.py][PNTOTP] while writing my own.

[PN]: https://github.com/prateeknischal
[PNTOTP]: https://github.com/prateeknischal/qry/blob/master/util/totp.py
