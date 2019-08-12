import setuptools


def long_desc():
    readme = open('README.md').read()
    i = readme.index('[')
    j = readme.index('\nIntroduction')
    k = readme.index('\n\nSource Code')
    m = readme.index('\n\nResources')
    n = readme.index('\n\nLicense')
    return readme[:i] + readme[j:k] + readme[m:n]


setuptools.setup(
    name='mintotp',
    version='0.1.0',
    author='Susam Pal',
    author_email='susam@susam.in',
    description='MinTOTP - Minimal TOTP Generator',
    long_description=long_desc(),
    long_description_content_type='text/markdown',
    url='https://github.com/susam/mintotp',

    py_modules=['mintotp'],
    entry_points={
        'console_scripts': {
            'mintotp = mintotp:main'
        }
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],

    keywords='totp hotp otp hmac cryptography 2fa authenticator',
)
