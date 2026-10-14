
import json
import random
import string

input_path = r"c:\Code\copilot-adoption-view-power-bi\sample.json"
output_path = r"c:\Code\copilot-adoption-view-power-bi\sample.anonymized.json"

def random_word(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def get_random_login(existing):
    while True:
        word = random_word(random.randint(6, 12))
        if word not in existing:
            return word

# First pass: collect all unique (user_id, user_login) pairs
unique_pairs = set()
with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        try:
            obj = json.loads(line)
            key = (obj["user_id"], obj["user_login"])
            unique_pairs.add(key)
        except Exception:
            continue

# Build mapping
user_map = {}
next_id = 100001
existing_logins = set()
for key in unique_pairs:
    new_login = get_random_login(existing_logins)
    user_map[key] = (next_id, new_login)
    existing_logins.add(new_login)
    next_id += 1

# Second pass: apply mapping
anonymized_lines = []
for line in lines:
    try:
        obj = json.loads(line)
        key = (obj["user_id"], obj["user_login"])
        if key in user_map:
            obj["user_id"], obj["user_login"] = user_map[key]
        anonymized_lines.append(json.dumps(obj))
    except Exception:
        anonymized_lines.append(line.strip())

with open(output_path, "w", encoding="utf-8") as f:
    for l in anonymized_lines:
        f.write(l + "\n")

print(f"Anonymized file saved to {output_path}")