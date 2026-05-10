"""Tests for the secure password generator."""

from test_opsyn.password import AMBIGUOUS_CHARS, PasswordOptions, generate_password


class TestGeneratePassword:
    def test_default_length(self):
        pw = generate_password()
        assert len(pw) == 16

    def test_custom_length(self):
        pw = generate_password(PasswordOptions(length=32))
        assert len(pw) == 32

    def test_default_includes_all_classes(self):
        """Default password contains uppercase, lowercase, digits, and symbols."""
        pw = generate_password()
        assert any(c.isupper() for c in pw)
        assert any(c.islower() for c in pw)
        assert any(c.isdigit() for c in pw)
        assert any(not c.isalnum() for c in pw)

    def test_uppercase_only(self):
        pw = generate_password(
            PasswordOptions(upper=True, lower=False, digits=False, symbols=False)
        )
        assert pw.isupper()

    def test_lowercase_only(self):
        pw = generate_password(
            PasswordOptions(upper=False, lower=True, digits=False, symbols=False)
        )
        assert pw.islower()

    def test_digits_only(self):
        pw = generate_password(
            PasswordOptions(upper=False, lower=False, digits=True, symbols=False)
        )
        assert pw.isdigit()

    def test_no_symbols(self):
        pw = generate_password(PasswordOptions(symbols=False))
        assert pw.isalnum()

    def test_exclude_ambiguous(self):
        pw = generate_password(PasswordOptions(exclude_ambiguous=True, length=64))
        for c in AMBIGUOUS_CHARS:
            assert c not in pw

    def test_exclude_ambiguous_with_all_classes(self):
        """Excluding ambiguous chars still produces a valid password."""
        pw = generate_password(PasswordOptions(exclude_ambiguous=True))
        assert len(pw) == 16
        assert any(c.isupper() for c in pw)
        assert any(c.islower() for c in pw)
        assert any(c.isdigit() for c in pw)

    def test_minimum_length_equals_enabled_classes(self):
        """Minimum length equals the number of enabled character classes."""
        pw = generate_password(
            PasswordOptions(
                upper=True, lower=True, digits=False, symbols=False, length=2
            )
        )
        assert len(pw) == 2

    def test_length_too_short_raises(self):
        try:
            generate_password(PasswordOptions(length=1))
            raise AssertionError("Expected ValueError")
        except ValueError as exc:
            assert "too short" in str(exc)

    def test_no_classes_enabled_raises(self):
        try:
            generate_password(
                PasswordOptions(upper=False, lower=False, digits=False, symbols=False)
            )
            raise AssertionError("Expected ValueError")
        except ValueError as exc:
            assert "at least one" in str(exc).lower()

    def test_passwords_are_random(self):
        """Two generated passwords are unlikely to be identical."""
        pw1 = generate_password()
        pw2 = generate_password()
        assert pw1 != pw2
