from flask import Flask, render_template, abort, url_for
import hashlib

app = Flask(__name__)

# --- Challenge Data ---------------------------------------------------------
# 7 public profiles (IDs 1..7)
PROFILES = {
    1: {
        "id": 1,
        "name": "Amina R.",
        "classe": "3A",
        "filiere": "Réseaux & Sécurité",
        "graduation": "2025-06-30",
        "photo_initials": "AR",
    },
    2: {
        "id": 2,
        "name": "Youssef B.",
        "classe": "2A",
        "filiere": "Développement Web",
        "graduation": "2026-06-30",
        "photo_initials": "YB",
    },
    3: {
        "id": 3,
        "name": "Salma K.",
        "classe": "1A",
        "filiere": "Data Science",
        "graduation": "2027-06-30",
        "photo_initials": "SK",
    },
    4: {
        "id": 4,
        "name": "Omar T.",
        "classe": "4A",
        "filiere": "Cloud & DevOps",
        "graduation": "2024-06-30",
        "photo_initials": "OT",
    },
    5: {
        "id": 5,
        "name": "Hajar M.",
        "classe": "3A",
        "filiere": "Sécurité Applicative",
        "graduation": "2025-06-30",
        "photo_initials": "HM",
    },
    6: {
        "id": 6,
        "name": "Reda C.",
        "classe": "2A",
        "filiere": "IA & ML",
        "graduation": "2026-06-30",
        "photo_initials": "RC",
    },
    7: {
        "id": 7,
        "name": "Imane Z.",
        "classe": "1A",
        "filiere": "Cybersécurité",
        "graduation": "2027-06-30",
        "photo_initials": "IZ",
    },
}

# Hidden record at ID 55 — this is NOT linked anywhere
HIDDEN_ID = 55
FLAG = "FLAG{S1mple_1d0r}"

# --- Helpers ----------------------------------------------------------------

def md5_of_id(n: int) -> str:
    return hashlib.md5(str(n).encode()).hexdigest()

# Precompute path tokens
HASH_TO_ID = {md5_of_id(i): i for i in list(PROFILES.keys()) + [HIDDEN_ID]}
ID_TO_HASH = {i: md5_of_id(i) for i in list(PROFILES.keys()) + [HIDDEN_ID]}

# --- Routes -----------------------------------------------------------------

@app.route("/")
def index():
    cards = []
    for i, p in PROFILES.items():
        cards.append({
            **p,
            "hash": ID_TO_HASH[i],
        })
    return render_template("index.html", profiles=cards)

@app.route("/<token>")
def show_profile(token: str):
    # Insecure: direct object reference via hashed token
    if token not in HASH_TO_ID:
        return render_template("not_found.html", token=token), 404

    target_id = HASH_TO_ID[token]

    # Visible public profiles
    if target_id in PROFILES:
        return render_template("profile.html", profile=PROFILES[target_id], flag=None)

    # Hidden profile (ID 55) exposing the flag
    if target_id == HIDDEN_ID:
        phantom = {
            "id": HIDDEN_ID,
            "name": "(archivé)",
            "classe": "—",
            "filiere": "—",
            "graduation": "—",
            "photo_initials": "??",
        }
        return render_template("profile.html", profile=phantom, flag=FLAG)

    # Fallback (shouldn't happen)
    abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
