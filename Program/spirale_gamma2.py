# ============================================================
# spirale_gamma2.py — BLOC 1
# Fonctions mathématiques de base : Spirale mod 30, Gamma, Euler
# ============================================================

import numpy as np
import math
from math import gamma, sqrt, sin, cos, pi


# ============================================================
# 1. Spirale mod 30
# ============================================================

def spirale_mod30(Nmax):
    """
    Retourne un tableau Nx3 :
    - r : rayon
    - theta : angle
    - p : nombre premier
    La spirale est normalisée pour un affichage 3D.
    """
    if Nmax < 2:
        return np.array([])

    # Liste des nombres premiers
    primes = []
    sieve = np.ones(Nmax+1, dtype=bool)
    sieve[0:2] = False

    for i in range(2, int(sqrt(Nmax)) + 1):
        if sieve[i]:
            sieve[i*i:Nmax+1:i] = False

    primes = np.nonzero(sieve)[0]

    if len(primes) == 0:
        return np.array([])

    # Spirale mod 30
    r = np.sqrt(primes)
    theta = primes * (2 * np.pi / 30)

    pts = np.column_stack((r, theta, primes))
    return pts


# ============================================================
# 2. Gamma(s/2) vertical
# ============================================================

def gamma_vertical(N=2000):
    """
    Retourne :
    - t : valeurs de s
    - g : Gamma(s/2)
    Normalisé pour éviter les débordements.
    """
    t = np.linspace(1, 60, N)
    g = np.array([gamma(s/2) for s in t])

    # Normalisation pour stabilité numérique
    g = g / np.max(g)

    return t, g


# ============================================================
# 3. Facteur Euler local
# ============================================================

def euler_factor(p):
    """
    Retourne le facteur Euler local :
    1 / (1 - 1/p)
    """
    if p <= 1:
        return 1.0
    return 1.0 / (1.0 - 1.0/p)


# ============================================================
# 4. Densité Goldbach locale (approximation rapide)
# ============================================================
def goldbach_even(n):
    """
    Goldbach density for even integers n >= 4.
    Returns the number of prime decompositions n = p + q.
    """
    if n < 4 or n % 2 != 0:
        return 0

    sieve = np.ones(n+1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if sieve[i]:
            sieve[i*i:n+1:i] = False

    primes = np.nonzero(sieve)[0]

    count = 0
    for p in primes:
        q = n - p
        if q < 2:
            break
        if sieve[q]:
            count += 1

    return count

def goldbach_density(n):
    """
    Approximation rapide de la densité Goldbach :
    d(n) = nombre de représentations n = p + q
    avec p, q premiers.
    """
    if n < 4:
        return 0

    # Crible rapide
    sieve = np.ones(n+1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(sqrt(n)) + 1):
        if sieve[i]:
            sieve[i*i:n+1:i] = False

    primes = np.nonzero(sieve)[0]

    count = 0
    for p in primes:
        if p > n:
            break
        q = n - p
        if q >= 2 and sieve[q]:
            count += 1

    return count
# ============================================================
# spirale_gamma2.py — BLOC 2
# Fonctions avancées : Fusion Spirale × Gamma, coordonnées 3D
# ============================================================

# ============================================================
# 5. Fusion Spirale × Gamma (version mathématique)
# ============================================================

def fusion_spirale_gamma(Nmax):
    """
    Retourne :
    - X, Y : coordonnées normalisées de la spirale
    - Z : projection Gamma(s/2)
    - p : liste des nombres premiers
    """
    pts = spirale_mod30(Nmax)
    if pts.size == 0:
        return None, None, None, None

    r = pts[:, 0]
    theta = pts[:, 1]
    p = pts[:, 2]

    # Coordonnées normalisées
    X = (r * np.cos(theta)) / r.max()
    Y = (r * np.sin(theta)) / r.max()

    # Gamma
    t_gamma, g_gamma = gamma_vertical()
    proj = -(p % 60)
    Z = np.interp(proj, t_gamma, g_gamma)

    return X, Y, Z, p


# ============================================================
# 6. Heatmap orbitale (résidus mod 30)
# ============================================================

def heatmap_orbitale(Nmax):
    """
    Retourne une matrice 30x30 représentant
    les transitions (a -> b) des résidus mod 30.
    """
    pts = spirale_mod30(Nmax)
    if pts.size == 0:
        return np.zeros((30, 30), dtype=int)

    p = pts[:, 2]
    residues = np.array([int(pi % 30) for pi in p])

    heat = np.zeros((30, 30), dtype=int)

    for i in range(len(residues) - 1):
        a = int(residues[i])
        b = int(residues[i + 1])
        heat[a, b] += 1

    return heat



# ============================================================
# 7. Coordonnées 3D complètes (pour affichage)
# ============================================================

def spirale_3D(Nmax):
    """
    Retourne :
    - X, Y, Z : coordonnées 3D de la spirale mod 30
    - p : liste des nombres premiers
    """
    pts = spirale_mod30(Nmax)
    if pts.size == 0:
        return None, None, None, None

    r = pts[:, 0]
    theta = pts[:, 1]
    p = pts[:, 2]

    X = (r * np.cos(theta)) / r.max()
    Y = (r * np.sin(theta)) / r.max()
    Z = p

    return X, Y, Z, p


# ============================================================
# 8. Densité Goldbach (vecteur complet)
# ============================================================

def goldbach_vector(p_list):
    """
    Retourne un vecteur de densités Goldbach
    pour une liste de nombres premiers.
    """
    return np.array([goldbach_density(int(p)) for p in p_list])


# ============================================================
# 9. Résidus mod 30 (vecteur)
# ============================================================

def residus_mod30(p_list):
    """
    Retourne les résidus mod 30 pour une liste de p.
    """
    return np.array([p % 30 for p in p_list])
# ============================================================
# spirale_gamma2.py — BLOC 3
# Graphiques, tourbillon dynamique, exports
# ============================================================

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# 10. Tracé Spirale 3D (figure autonome)
# ============================================================

def plot_spirale_3D(Nmax, save_path=None):
    X, Y, Z, p = spirale_3D(Nmax)
    if X is None:
        return None

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(X, Y, Z, s=5, c=p, cmap='viridis')
    ax.set_title(f"Spirale mod 30 — Nmax = {Nmax}")

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return save_path

    return fig


# ============================================================
# 11. Tracé Gamma(s/2)
# ============================================================

def plot_gamma(save_path=None):
    t, g = gamma_vertical()

    fig = plt.figure(figsize=(7, 4))
    plt.plot(t, g, color='cyan')
    plt.title("Gamma(s/2)")
    plt.xlabel("s")
    plt.ylabel("Gamma(s/2)")

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return save_path

    return fig


# ============================================================
# 12. Tracé Fusion Spirale × Gamma
# ============================================================

def plot_fusion(Nmax, save_path=None):
    X, Y, Z, p = fusion_spirale_gamma(Nmax)
    if X is None:
        return None

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(X, Y, Z, s=5, c=Z, cmap='plasma')
    ax.set_title("Fusion Spirale × Gamma")

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return save_path

    return fig


# ============================================================
# 13. Tracé densité Goldbach
# ============================================================

def plot_goldbach(Nmax, save_path=None):
    pts = spirale_mod30(Nmax)
    if pts.size == 0:
        return None

    p = pts[:, 2]
    densites = goldbach_vector(p)

    fig = plt.figure(figsize=(7, 4))
    plt.plot(p, densites, '.', markersize=3, color='orange')
    plt.title("Densité Goldbach locale")
    plt.xlabel("p")
    plt.ylabel("d(p)")

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return save_path

    return fig


# ============================================================
# 14. Tracé Heatmap orbitale
# ============================================================

def plot_heatmap(Nmax, save_path=None):
    heat = heatmap_orbitale(Nmax)

    fig = plt.figure(figsize=(6, 5))
    plt.title("Heatmap orbitale (a,b)")
    plt.imshow(heat, cmap='inferno')
    plt.colorbar()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return save_path

    return fig


# ============================================================
# 15. Tourbillon dynamique (rotation automatique)
# ============================================================

def plot_spirale_tourbillon(Nmax, frames=120, save_path=None):
    """
    Génère une animation simple (rotation) de la spirale mod 30.
    Retourne la liste des images (frames).
    """
    X, Y, Z, p = spirale_3D(Nmax)
    if X is None:
        return None

    images = []

    for angle in range(frames):
        fig = plt.figure(figsize=(7, 6))
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(X, Y, Z, s=5, c=p, cmap='viridis')
        ax.view_init(30, angle * 3)
        ax.set_title(f"Tourbillon Spirale — frame {angle}")

        if save_path:
            frame_path = f"{save_path}_frame_{angle:03d}.png"
            fig.savefig(frame_path, dpi=120, bbox_inches='tight')
            images.append(frame_path)
            plt.close(fig)
        else:
            images.append(fig)

    return images


# ============================================================
# 16. Export PNG (fonction générique)
# ============================================================

def export_png(fig, path):
    """
    Sauvegarde une figure matplotlib.
    """
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return path


# ============================================================
# 17. API publique (pour Station Monfette Pro)
# ============================================================

__all__ = [
    "spirale_mod30",
    "spirale_3D",
    "gamma_vertical",
    "fusion_spirale_gamma",
    "goldbach_density",
    "goldbach_vector",
    "residus_mod30",
    "heatmap_orbitale",
    "plot_spirale_3D",
    "plot_gamma",
    "plot_fusion",
    "plot_goldbach",
    "plot_heatmap",
    "plot_spirale_tourbillon",
    "export_png",
    "goldbach_even",
    "euler_factor"
]
