# embed_scripts.py
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "automation_scripts.json")
EMBEDDING_FILE = os.path.join(BASE_DIR, "embeddings", "script_embeddings.npy")
ID_MAP_FILE = os.path.join(BASE_DIR, "embeddings", "id_map.json")

model = SentenceTransformer("all-MiniLM-L6-v2")

with open(DATA_FILE, "r") as f:
    scripts = json.load(f)

texts = []
id_map = {}

for i, script in enumerate(scripts):
    # Combine logic from script code, name, and launch_point_object for better matching
    text = f"{script['script_code']} {script['name']} {script['launch_point_object']}"
    texts.append(text)
    id_map[str(i)] = i  # Simple mapping

embeddings = model.encode(texts)

# Save embeddings and id_map
np.save(EMBEDDING_FILE, embeddings)

with open(ID_MAP_FILE, "w") as f:
    json.dump(id_map, f)

print("✅ Embeddings and id_map saved.")
