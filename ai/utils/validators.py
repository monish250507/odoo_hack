def validate_structured_output(data: dict) -> bool:
    # Perform complex semantic validation beyond Pydantic types here
    # e.g., checking if values are within realistic bounds
    if not data:
        return False
    return True
