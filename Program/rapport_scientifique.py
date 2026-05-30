# ============================================================
# rapport_scientifique.py — VERSION COMPLÈTE ET CORRIGÉE
# Compatible Station Monfette Pro v3
# ============================================================

import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

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

def analyse_goldbach_even(Nmax):
    """
    Analyse Goldbach sur les entiers pairs jusqu'à Nmax.
    """
    even_numbers = np.arange(4, Nmax+1, 2)
    densities = np.array([goldbach_even(n) for n in even_numbers])

    fig = plt.figure(figsize=(7,4))
    plt.plot(even_numbers, densities, '.', markersize=2, color='green')
    plt.title("Goldbach density for even integers")
    plt.xlabel("n (even)")
    plt.ylabel("d(n)")
    img = enregistrer_image(fig, "densite_goldbach_even.png")

    return {
        "min": int(np.min(densities)),
        "max": int(np.max(densities)),
        "mean": float(np.mean(densities)),
        "image": img
    }

# Import scientifique
from spirale_gamma2 import (
    spirale_mod30,
    gamma_vertical,
    fusion_spirale_gamma,
    goldbach_density,
    heatmap_orbitale,
    plot_spirale_3D,
    plot_gamma,
    plot_fusion,
    plot_goldbach,
    plot_heatmap
)

# ============================================================
# Dossier des rapports
# ============================================================

def dossier_rapports():
    path = "/home/michel/Documents/3. Goldbach/rapports/"
    os.makedirs(path, exist_ok=True)
    return path


# ============================================================
# Enregistrement d'une image matplotlib
# ============================================================

def enregistrer_image(fig, filename):
    path = os.path.join(dossier_rapports(), filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return path


# ============================================================
# Enregistrement d'un fichier texte
# ============================================================

def enregistrer_texte(filename, contenu):
    path = os.path.join(dossier_rapports(), filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(contenu)
    return path


# ============================================================
# Conversion PDF (WeasyPrint)
# ============================================================

def convertir_pdf_weasyprint(md_path, pdf_path):
    try:
        from weasyprint import HTML
        HTML(md_path).write_pdf(pdf_path)
    except Exception as e:
        print("Erreur WeasyPrint :", e)


# ============================================================
# Conversion PDF (markdown-pdf)
# ============================================================

def convertir_pdf_markdownpdf(md_path, pdf_path):
    try:
        os.system(f"markdown-pdf '{md_path}' -o '{pdf_path}'")
    except Exception as e:
        print("Erreur markdown-pdf :", e)


# ============================================================
# ANALYSES SCIENTIFIQUES
# ============================================================

def analyse_spirale_mod30(Nmax):
    pts = spirale_mod30(Nmax)
    if pts.size == 0:
        return {"variance": 0, "tunnels_actifs": 0}

    residues = np.array([int(p % 30) for p in pts[:, 2]])
    variance = np.var(residues)
    tunnels = len(np.unique(residues))

    # Image
    fig = plt.figure(figsize=(6, 4))
    plt.hist(residues, bins=30, color="blue")
    img = enregistrer_image(fig, "spirale_residus_mod30.png")

    return {
        "variance": float(variance),
        "tunnels_actifs": int(tunnels),
        "image": img
    }


def analyse_gamma():
    t, g = gamma_vertical()

    fig = plt.figure(figsize=(6, 4))
    plt.plot(t, g, color="cyan")
    img = enregistrer_image(fig, "gamma_s2.png")

    return {
        "stats": {
            "max": float(np.max(g)),
            "min": float(np.min(g)),
            "pics": int(np.sum(g > 0.95))
        },
        "image": img
    }


def analyse_fusion(Nmax):
    fig = plot_fusion(Nmax)
    img = enregistrer_image(fig, "fusion_spirale_gamma.png")

    X, Y, Z, p = fusion_spirale_gamma(Nmax)
    if Z is None:
        return {"continuite_verticale": 0, "image": img}

    contin = float(np.linalg.norm(np.diff(Z)))

    return {
        "continuite_verticale": contin,
        "image": img
    }


def analyse_goldbach(Nmax):
    pts = spirale_mod30(Nmax)
    p = pts[:, 2]

    dens = np.array([goldbach_density(int(pi)) for pi in p])

    fig = plt.figure(figsize=(6, 4))
    plt.plot(p, dens, '.', markersize=3, color='orange')
    img1 = enregistrer_image(fig, "densite_goldbach.png")

    fig2 = plot_heatmap(Nmax)
    img2 = enregistrer_image(fig2, "heatmap_orbitale.png")

    return {
        "stats": {
            "moyenne": float(np.mean(dens)),
            "minimum": float(np.min(dens)),
            "maximum": float(np.max(dens))
        },
        "image_densite": img1,
        "image_heatmap": img2
    }


def analyse_adelique(Nmax):
    pts = spirale_mod30(Nmax)
    p = pts[:, 2]

    E = np.array([1/(1 - 1/pi) for pi in p])
    t, g = gamma_vertical()
    G = np.interp(-(p % 60), t, g)
    D = np.array([goldbach_density(int(pi)) for pi in p])

    corr_EG = float(np.corrcoef(E, G)[0, 1])
    corr_GD = float(np.corrcoef(G, D)[0, 1])
    corr_ED = float(np.corrcoef(E, D)[0, 1])

    fig = plt.figure(figsize=(6, 4))
    plt.scatter(E, D, s=3, alpha=0.5)
    img = enregistrer_image(fig, "fusion_adelique.png")

    return {
        "corr_Euler_Gamma": corr_EG,
        "corr_Gamma_Goldbach": corr_GD,
        "corr_Euler_Goldbach": corr_ED,
        "image": img
    }


# ============================================================
# GÉNÉRATION DES RAPPORTS (FR + EN)
# ============================================================

def generer_markdown_FR(Nmax, A):
    d = dossier_rapports()
    md = []

    md.append("# Rapport Scientifique — Station Monfette Pro\n")
    md.append(f"**Généré le :** {datetime.now()}\n")
    md.append(f"**N max analysé :** {Nmax}\n")
    md.append("---\n")

    # Spirale
    md.append("## 1. Spirale mod 30\n")
    md.append(f"- Variance : **{A['spirale']['variance']:.6f}**\n")
    md.append(f"- Tunnels actifs : **{A['spirale']['tunnels_actifs']}**\n")
    md.append(f"![Spirale]({A['spirale']['image']})\n\n")

    # Gamma
    md.append("## 2. Gamma(s/2)\n")
    md.append(f"- Max : **{A['gamma']['stats']['max']:.6f}**\n")
    md.append(f"- Min : **{A['gamma']['stats']['min']:.6f}**\n")
    md.append(f"- Pics : **{A['gamma']['stats']['pics']}**\n")
    md.append(f"![Gamma]({A['gamma']['image']})\n\n")

    # Fusion
    md.append("## 3. Fusion Spirale × Gamma\n")
    md.append(f"- Continuité verticale : **{A['fusion']['continuite_verticale']:.6f}**\n")
    md.append(f"![Fusion]({A['fusion']['image']})\n\n")

    # Goldbach
    md.append("## 4. Analyse Goldbach\n")
    md.append(f"- Moyenne : **{A['goldbach']['stats']['moyenne']:.6f}**\n")
    md.append(f"- Minimum : **{A['goldbach']['stats']['minimum']:.6f}**\n")
    md.append(f"- Maximum : **{A['goldbach']['stats']['maximum']:.6f}**\n")
    md.append(f"![Densité]({A['goldbach']['image_densite']})\n\n")
    md.append(f"![Heatmap]({A['goldbach']['image_heatmap']})\n\n")
    
    # Goldbach (even integers)
    md.append("## 5. Goldbach Analysis (even integers)\n")
    md.append(f"- Minimum: **{A['goldbach_even']['min']}**\n")
    md.append(f"- Maximum: **{A['goldbach_even']['max']}**\n")
    md.append(f"- Average: **{A['goldbach_even']['mean']:.6f}**\n")
    md.append(f"![Goldbach Even]({A['goldbach_even']['image']})\n\n")

    # Adélique
    md.append("## 6. Analyse Adélique\n")
    md.append(f"- Corr(Euler, Gamma) : **{A['adelique']['corr_Euler_Gamma']:.6f}**\n")
    md.append(f"- Corr(Gamma, Goldbach) : **{A['adelique']['corr_Gamma_Goldbach']:.6f}**\n")
    md.append(f"- Corr(Euler, Goldbach) : **{A['adelique']['corr_Euler_Goldbach']:.6f}**\n")
    md.append(f"![Adelique]({A['adelique']['image']})\n\n")

    return "\n".join(md)


def generer_markdown_EN(Nmax, A):
    d = dossier_rapports()
    md = []

    md.append("# Scientific Report — Station Monfette Pro\n")
    md.append(f"**Generated on:** {datetime.now()}\n")
    md.append(f"**N max analyzed:** {Nmax}\n")
    md.append("---\n")

    md.append("## 1. Spiral mod 30\n")
    md.append(f"- Variance: **{A['spirale']['variance']:.6f}**\n")
    md.append(f"- Active tunnels: **{A['spirale']['tunnels_actifs']}**\n")
    md.append(f"![Spiral]({A['spirale']['image']})\n\n")

    md.append("## 2. Gamma(s/2)\n")
    md.append(f"- Max: **{A['gamma']['stats']['max']:.6f}**\n")
    md.append(f"- Min: **{A['gamma']['stats']['min']:.6f}**\n")
    md.append(f"- Peaks: **{A['gamma']['stats']['pics']}**\n")
    md.append(f"![Gamma]({A['gamma']['image']})\n\n")

    md.append("## 3. Spiral × Gamma Fusion\n")
    md.append(f"- Vertical continuity: **{A['fusion']['continuite_verticale']:.6f}**\n")
    md.append(f"![Fusion]({A['fusion']['image']})\n\n")

    md.append("## 4. Goldbach Analysis\n")
    md.append(f"- Average: **{A['goldbach']['stats']['moyenne']:.6f}**\n")
    md.append(f"- Minimum: **{A['goldbach']['stats']['minimum']:.6f}**\n")
    md.append(f"- Maximum: **{A['goldbach']['stats']['maximum']:.6f}**\n")
    md.append(f"![Density]({A['goldbach']['image_densite']})\n\n")
    md.append(f"![Heatmap]({A['goldbach']['image_heatmap']})\n\n")

    
    md.append("## 5. Adelic Analysis\n")
    md.append(f"- Corr(Euler, Gamma): **{A['adelique']['corr_Euler_Gamma']:.6f}**\n")
    md.append(f"- Corr(Gamma, Goldbach): **{A['adelique']['corr_Gamma_Goldbach']:.6f}**\n")
    md.append(f"- Corr(Euler, Goldbach): **{A['adelique']['corr_Euler_Goldbach']:.6f}**\n")
    md.append(f"![Adelic]({A['adelique']['image']})\n\n")

    return "\n".join(md)


# ============================================================
# FONCTION PRINCIPALE
# ============================================================

def generer_rapport(Nmax):

    analyses = {
        "spirale": analyse_spirale_mod30(Nmax),
        "gamma": analyse_gamma(),
        "fusion": analyse_fusion(Nmax),
        "goldbach": analyse_goldbach(Nmax),
        "goldbach_even": analyse_goldbach_even(Nmax),
        "adelique": analyse_adelique(Nmax)
    }




    # Markdown FR
    md_FR = generer_markdown_FR(Nmax, analyses)
    fichier_md_FR = enregistrer_texte("rapport_scientifique_FR.md", md_FR)

    # Markdown EN
    md_EN = generer_markdown_EN(Nmax, analyses)
    fichier_md_EN = enregistrer_texte("rapport_scientifique_EN.md", md_EN)

    # PDF WeasyPrint
    #convertir_pdf_weasyprint(fichier_md_FR, os.path.join(dossier_rapports(), "rapport_scientifique_FR.pdf"))
    #convertir_pdf_weasyprint(fichier_md_EN, os.path.join(dossier_rapports(), "rapport_scientifique_EN.pdf"))

    # PDF markdown-pdf
    #convertir_pdf_markdownpdf(fichier_md_FR, os.path.join(dossier_rapports(), "rapport_scientifique_FR_simple.pdf"))
    #convertir_pdf_markdownpdf(fichier_md_EN, os.path.join(dossier_rapports(), "rapport_scientifique_EN_simple.pdf"))

    return True
