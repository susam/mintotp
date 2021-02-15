Changelog
=========

0.3.0 (2021-02-15)
------------------

### Changed

- Use `str.zfill` instead of `str.rjust` for adding leading zeros.


0.2.0 (2019-08-13)
------------------

### Added

- Add license information in package metadata.
- Add `digits` and `digest` to `totp()` parameter list.
- Add command line arguments for time-step, digits, and digest.

### Changed

- Rename `secret` to `key` in `hotp()` and `totp()` parameter lists.
- Rename `interval` to `time_step` in `totp()` parameter list.


0.1.0 (2019-08-12)
------------------

### Added

- Add a minimal TOTP generator.
- Expose `hotp()` and `totp()` as module-level functions.
- Add project documentation.
