import re

def remove_number_prefix(text):
  """Removes number prefixes (e.g., "1.", "2.", "3.") from strings."""
  return re.sub(r"^\d+\. ", "", text)
