import numpy as np
from collections import defaultdict

R30 = [1, 7, 11, 13, 17, 19, 23, 29]
SG = [11, 23, 29]
XSG = [1, 7, 13, 17, 19]

# ============================================================
# CONJUGAISON : r ↔ (30-r)
# ============================================================

print("=" * 60)
print("CONJUGAISON ET TUNNELS")
print("=" * 60)

# Pour chaque tunnel (a,b) actif pour N, 
# quel est le tunnel conjugué et pour quel N' ?
print("\nTunnel (a,b) pour N  →  tunnel conjugué (30-a, 30-b) pour N'=60-N")
print("-" * 60)

# Prenons N ≡ 22 mod 30 (cas pur A — le plus rare)
print("\nCas N ≡ 22 mod 30 (pur A : seulement SG×SG)")
tunnels_22 = [(a,b) for a in R30 for b in R30 if (a+b)%30 == 22]
for a,b in tunnels_22:
    ca, cb = (30-a)%30, (30-b)%30
    N_prime = (ca + cb) % 30
    type_ab = "A" if a in SG and b in SG else ("C" if a in XSG and b in XSG else "B")
    type_conj = "A" if ca in R30 and cb in R30 and ca in SG and cb in SG else "?"
    in_R30 = ca in R30 and cb in R30
    print(f"  ({a:2d},{b:2d}) → conjugué ({ca:2d},{cb:2d}), N'≡{N_prime} mod30, dans R30={in_R30}")

print("\nCas N ≡ 2 mod 30 (pur C : seulement XSG×XSG)")
tunnels_2 = [(a,b) for a in R30 for b in R30 if (a+b)%30 == 2]
for a,b in tunnels_2:
    ca, cb = (30-a)%30, (30-b)%30
    N_prime = (ca + cb) % 30
    in_R30 = ca in R30 and cb in R30
    print(f"  ({a:2d},{b:2d}) → conjugué ({ca:2d},{cb:2d}), N'≡{N_prime} mod30, dans R30={in_R30}")

print("\nCas N ≡ 12 mod 30 (pur B : seulement SG×XSG)")
tunnels_12 = [(a,b) for a in R30 for b in R30 if (a+b)%30 == 12]
for a,b in tunnels_12:
    ca, cb = (30-a)%30, (30-b)%30
    N_prime = (ca + cb) % 30
    in_R30 = ca in R30 and cb in R30
    print(f"  ({a:2d},{b:2d}) → conjugué ({ca:2d},{cb:2d}), N'≡{N_prime} mod30, dans R30={in_R30}")

# EOF
# Sortie

# ============================================================
# CONJUGAISON ET TUNNELS
# ============================================================

# Tunnel (a,b) pour N  →  tunnel conjugué (30-a, 30-b) pour N'=60-N
# ------------------------------------------------------------

# Cas N ≡ 22 mod 30 (pur A : seulement SG×SG)
  # (11,11) → conjugué (19,19), N'≡8 mod30, dans R30=True
  # (23,29) → conjugué ( 7, 1), N'≡8 mod30, dans R30=True
  # (29,23) → conjugué ( 1, 7), N'≡8 mod30, dans R30=True

# Cas N ≡ 2 mod 30 (pur C : seulement XSG×XSG)
  # ( 1, 1) → conjugué (29,29), N'≡28 mod30, dans R30=True
  # (13,19) → conjugué (17,11), N'≡28 mod30, dans R30=True
  # (19,13) → conjugué (11,17), N'≡28 mod30, dans R30=True

# Cas N ≡ 12 mod 30 (pur B : seulement SG×XSG)
  # ( 1,11) → conjugué (29,19), N'≡18 mod30, dans R30=True
  # (11, 1) → conjugué (19,29), N'≡18 mod30, dans R30=True
  # (13,29) → conjugué (17, 1), N'≡18 mod30, dans R30=True
  # (19,23) → conjugué (11, 7), N'≡18 mod30, dans R30=True
  # (23,19) → conjugué ( 7,11), N'≡18 mod30, dans R30=True
  # (29,13) → conjugué ( 1,17), N'≡18 mod30, dans R30=True
# Terminé

