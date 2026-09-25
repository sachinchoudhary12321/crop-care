"""SQLAlchemy ORM models (tables) live in this package.

This package is intentionally empty — fake database functionality is worse
than none. The concrete models are created in the **Database Integration
task** and must inherit from `app.database.base.Base`.

Planned models (initial design):
  * User            — farmer accounts (future auth)
  * CropImage       — uploaded image metadata (path, hash, size, ...)
  * Prediction      — prediction history (disease label, confidence, model version)
  * Disease         — disease catalogue (label, crop, description, ...)
  * Recommendation  — generated treatment recommendations
  * ChatSession / ChatMessage — chatbot conversations
"""