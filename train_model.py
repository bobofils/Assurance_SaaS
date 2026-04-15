from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib

# =========================
# 📊 DATASET ASSURANCE PRO
# =========================

# [âge, revenu, couverture]
X = np.array([
    [25, 200000, 1000000],
    [35, 500000, 3000000],
    [45, 800000, 5000000],
    [60, 300000, 2000000],
    [70, 150000, 1000000],
    [30, 400000, 2500000],
])

# 1 = bon profil, 0 = risque
y = np.array([1, 1, 1, 0, 0, 1])

# =========================
# 🤖 TRAIN MODEL
# =========================
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# =========================
# 💾 SAVE MODEL
# =========================
joblib.dump(model, "model.pkl")

print("✅ Modèle assurance créé avec succès")