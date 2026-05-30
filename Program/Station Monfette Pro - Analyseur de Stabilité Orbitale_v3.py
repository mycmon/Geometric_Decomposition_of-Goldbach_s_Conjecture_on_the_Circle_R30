# ============================================================
# Station Monfette Pro - Analyseur de Stabilité Orbitale_v3.py
# BLOC 1 — Imports + Classe + __init__ + Interface de base
# ============================================================

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import scientifique interne
from spirale_gamma2 import *
import rapport_scientifique  # <-- nouveau module

# ============================================================
# Classe principale
# ============================================================

class MonfetteAppPro:

    def __init__(self, root):
        self.root = root
        self.root.title("Station Monfette Pro — Analyseur de Stabilité Orbitale v3")

        # --------------------------------------------------------
        # 1. Couleurs R30 (résidus mod 30)
        # --------------------------------------------------------
        self.couleurs_R = {
            1:  "#FF0000",
            7:  "#FF7F00",
            11: "#FFFF00",
            13: "#7FFF00",
            17: "#00FF00",
            19: "#00FFFF",
            23: "#0000FF",
            29: "#8B00FF"
        }

        # --------------------------------------------------------
        # 2. Frame principale
        # --------------------------------------------------------
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        # --------------------------------------------------------
        # 3. Paramètres utilisateur
        # --------------------------------------------------------
        self.Nmax_var = tk.IntVar(value=5000)

        # --------------------------------------------------------
        # 4. Zone graphique (matplotlib)
        # --------------------------------------------------------
        self.fig = plt.Figure(figsize=(6, 6), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=20)

        # --------------------------------------------------------
        # 5. Panneau de contrôle
        # --------------------------------------------------------
        self.panel = ttk.Frame(self.frame)
        self.panel.grid(row=0, column=1, sticky="n")

        ttk.Label(self.panel, text="N max :").grid(row=0, column=0, sticky="w")
        ttk.Entry(self.panel, textvariable=self.Nmax_var, width=10).grid(row=0, column=1)

        # --------------------------------------------------------
        # 6. Boutons principaux
        # --------------------------------------------------------
        ttk.Button(self.panel, text="Tracer Spirale", command=self.tracer_spirale).grid(row=1, column=0, columnspan=2, pady=5)
        ttk.Button(self.panel, text="Tracer Gamma", command=self.tracer_gamma).grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(self.panel, text="Fusion Spirale × Gamma", command=self.tracer_fusion).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(self.panel, text="Analyse Goldbach", command=self.tracer_goldbach).grid(row=4, column=0, columnspan=2, pady=5)

        # --------------------------------------------------------
        # 7. Nouveau bouton : Export Rapport Scientifique
        # --------------------------------------------------------
        ttk.Button(
            self.panel,
            text="Exporter Rapport Scientifique (FR + EN)",
            command=self.exporter_rapport_scientifique
        ).grid(row=10, column=0, columnspan=2, pady=15)

        # --------------------------------------------------------
        # 8. Initialisation graphique
        # --------------------------------------------------------
        self.ax.set_title("Station Monfette Pro — Prêt")
        self.canvas.draw()

    # ============================================================
    # Fonctions graphiques (définies dans Bloc 2)
    # ============================================================

    def tracer_spirale(self):
        pass  # sera défini dans le Bloc 2

    def tracer_gamma(self):
        pass  # Bloc 2

    def tracer_fusion(self):
        pass  # Bloc 2

    def tracer_goldbach(self):
        pass  # Bloc 2

    # ============================================================
    # Export du rapport scientifique (défini dans Bloc 3)
    # ============================================================

    def exporter_rapport_scientifique(self):
        pass  # Bloc 3
# ============================================================
# BLOC 2 — Fonctions graphiques : Spirale, Gamma, Fusion, Goldbach
# ============================================================

    def tracer_spirale(self):
        """
        Affiche la spirale mod 30 en 3D.
        """
        Nmax = self.Nmax_var.get()
        pts = spirale_mod30(Nmax)

        if pts.size == 0:
            messagebox.showerror("Erreur", "Aucun point généré.")
            return

        r = pts[:, 0]
        theta = pts[:, 1]
        p = pts[:, 2]

        X = (r * np.cos(theta)) / r.max()
        Y = (r * np.sin(theta)) / r.max()
        Z = p

        self.ax.clear()
        self.ax.scatter(X, Y, Z, s=5, c=p, cmap='viridis')
        self.ax.set_title(f"Spirale mod 30 — Nmax = {Nmax}")
        self.canvas.draw()


    def tracer_gamma(self):
        """
        Affiche Gamma(s/2) en 2D.
        """
        t, g = gamma_vertical()

        self.ax.clear()
        self.ax.plot(t, g, color='cyan')
        self.ax.set_title("Gamma(s/2)")
        self.ax.set_xlabel("s")
        self.ax.set_ylabel("Gamma(s/2)")
        self.canvas.draw()


    def tracer_fusion(self):
        """
        Affiche la fusion Spirale × Gamma en 3D.
        """
        Nmax = self.Nmax_var.get()
        pts = spirale_mod30(Nmax)

        if pts.size == 0:
            messagebox.showerror("Erreur", "Aucun point généré.")
            return

        r = pts[:, 0]
        theta = pts[:, 1]
        p = pts[:, 2]

        # Gamma
        t_gamma, g_gamma = gamma_vertical()
        proj = -(p % 60)
        Z = np.interp(proj, t_gamma, g_gamma)

        X = (r * np.cos(theta)) / r.max()
        Y = (r * np.sin(theta)) / r.max()

        self.ax.clear()
        self.ax.scatter(X, Y, Z, s=5, c=Z, cmap='plasma')
        self.ax.set_title("Fusion Spirale × Gamma")
        self.canvas.draw()


    def tracer_goldbach(self):
        """
        Affiche la densité Goldbach locale.
        """
        Nmax = self.Nmax_var.get()
        pts = spirale_mod30(Nmax)

        if pts.size == 0:
            messagebox.showerror("Erreur", "Aucun point généré.")
            return

        p = pts[:, 2]
        densites = np.array([goldbach_density(int(pi)) for pi in p])

        self.ax.clear()
        self.ax.plot(p, densites, '.', markersize=3, color='orange')
        self.ax.set_title("Densité Goldbach locale")
        self.ax.set_xlabel("p")
        self.ax.set_ylabel("d(p)")
        self.canvas.draw()
# ============================================================
# BLOC 3 — Export du Rapport Scientifique (FR + EN)
# ============================================================

    def exporter_rapport_scientifique(self):
        """
        Génère automatiquement :
        - rapport_scientifique_FR.md
        - rapport_scientifique_EN.md
        - rapport_scientifique_FR.pdf
        - rapport_scientifique_EN.pdf
        - rapport_scientifique_FR_simple.pdf
        - rapport_scientifique_EN_simple.pdf
        dans le dossier :
        /home/michel/Documents/3. Goldbach/rapports/
        """
        Nmax = self.Nmax_var.get()

        # Confirmation visuelle
        self.ax.clear()
        self.ax.text2D(0.1, 0.5, "Génération du rapport scientifique...\nVeuillez patienter.",
                       transform=self.ax.transAxes, fontsize=12)
        self.canvas.draw()

        try:
            # Appel au module scientifique
            ok = rapport_scientifique.generer_rapport(Nmax)

            if ok:
                messagebox.showinfo(
                    "Rapport généré",
                    "Les rapports FR + EN (MD + PDF) ont été générés avec succès.\n\n"
                    "Dossier : /home/michel/Documents/3. Goldbach/rapports/"
                )
            else:
                messagebox.showerror(
                    "Erreur",
                    "Une erreur est survenue lors de la génération du rapport."
                )

        except Exception as e:
            messagebox.showerror(
                "Erreur critique",
                f"Une exception est survenue :\n{e}"
            )

# ============================================================
#  MAIN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = MonfetteAppPro(root)
    root.mainloop()
