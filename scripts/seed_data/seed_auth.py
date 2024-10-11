from app.auth.tests.factories import UserFactory

# --- User
print("# --- Seed User")
UserFactory.create_batch(10)
