"""Deprecated developer test. Skipped by default."""

import pytest

pytestmark = pytest.mark.skip(reason="Deprecated developer test removed from required suite")

# Intentionally empty to avoid importing heavy dependencies or running code
