URI1 = otpauth://totp/alice:bob?secret=ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
URI2 = otpauth://totp/alice:cam?secret=PW4YAYYZVDE5RK2AOLKUATNZIKAFQLZO&issuer=alice

gen:
	python3 totp.py $$(zbarimg -q *.png | sed 's/.*secret=\([^&]*\).*/\1/')

qr:
	qrencode -s 10 -o secret1.png "$(URI1)"
	qrencode -s 10 -o secret2.png "$(URI2)"

key:
	python3 -c 'import base64, os; print(base64.b32encode(os.urandom(20)).decode())'
