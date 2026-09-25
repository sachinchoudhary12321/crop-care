"""Pydantic request/response schemas — the API contract.

Schemas are pure DTOs (data containers + validation) and are shared across
layers so the ML/service output and the HTTP response never drift apart.
"""