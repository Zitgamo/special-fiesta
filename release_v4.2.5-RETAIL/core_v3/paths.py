import os

# --- THE NAVIGATIONAL SOUL OF THE FLEET ---
# This file ensures absolute portability across any directory structure.

# 1. Base Detection
# This script is in core_v3/, so the CORE_DIR is the current folder.
CORE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Root Detection
# The project root is one level up from core_v3/
ROOT_DIR = os.path.dirname(CORE_DIR)

# 3. Critical Asset Paths
DB_PATH = os.path.join(CORE_DIR, "iron_core.db")
DNA_PATH = os.path.join(CORE_DIR, "dna.json")
SECRETS_PATH = os.path.join(CORE_DIR, "secrets.json")

# 4. Legacy/External References
# (Add any other static paths here)

print(f" >> [PATHS] Sovereign Environment: {ROOT_DIR}")
