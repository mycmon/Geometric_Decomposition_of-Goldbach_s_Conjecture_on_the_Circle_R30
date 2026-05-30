"""
Monfette Goldbach — Constantes asymptotiques k_A, k_B, k_C
et Zone de Décharge / Discharge Zone

Graphique interactif avec matplotlib.
Auteur : Michel Monfette, 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider, CheckButtons
from matplotlib.lines import Line2D

# ── Données empiriques ────────────────────────────────────────────────────────

N_labels = [
    r'$10^4$', r'$5{\times}10^4$', r'$10^5$', r'$5{\times}10^5$',
    r'$10^6$', r'$5{\times}10^6$', r'$10^7$', r'$5{\times}10^7$',
    r'$10^8$', r'$2{\times}10^8$'
]
N_values = [1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 2e8]

# Constantes principales (convergence observée)
kA = np.array([0.0890, 0.1030, 0.1100, 0.1180, 0.1210,
               0.1230, 0.1240, 0.1245, 0.1247, 0.1247])
kB = np.array([0.0610, 0.0720, 0.0790, 0.0850, 0.0870,
               0.0890, 0.0890, 0.0891, 0.0892, 0.0892])
kC = np.array([0.0380, 0.0480, 0.0540, 0.0590, 0.0610,
               0.0630, 0.0632, 0.0633, 0.0634, 0.0634])

# Zone de Décharge : tunnels (1,29) et (11,19) — sous la moyenne G1
kA_discharge_1_29  = kA * np.array([0.76, 0.80, 0.83, 0.86, 0.88,
                                     0.90, 0.92, 0.94, 0.96, 0.97])
kA_discharge_11_19 = kA * np.array([0.79, 0.82, 0.85, 0.88, 0.90,
                                     0.91, 0.93, 0.95, 0.97, 0.98])

# Bandes d'incertitude (±écart-type)
kA_err = np.array([0.008, 0.006, 0.005, 0.004, 0.004,
                   0.003, 0.003, 0.003, 0.003, 0.003])
kB_err = np.array([0.006, 0.005, 0.004, 0.003, 0.003,
                   0.002, 0.002, 0.002, 0.002, 0.002])
kC_err = np.array([0.005, 0.004, 0.003, 0.003, 0.002,
                   0.002, 0.002, 0.002, 0.002, 0.002])

# Limites asymptotiques estimées
KA_LIM = 0.1247
KB_LIM = 0.0892
KC_LIM = 0.0634

# Valeur Hardy-Littlewood de référence (normalisée)
HL_ref = np.full(len(N_values), KA_LIM * 1.012)

# ── Mise en page ──────────────────────────────────────────────────────────────

plt.style.use('seaborn-v0_8-whitegrid')
fig = plt.figure(figsize=(13, 9), facecolor='#FAFAF8')
fig.suptitle(
    "Constantes asymptotiques des tunnels de Goldbach mod 30\n"
    "Asymptotic constants of Goldbach tunnels mod 30",
    fontsize=14, fontweight='bold', color='#2C2C2A', y=0.98
)

gs = gridspec.GridSpec(
    3, 2,
    figure=fig,
    left=0.08, right=0.96,
    top=0.91, bottom=0.20,
    hspace=0.42, wspace=0.32
)

ax_main   = fig.add_subplot(gs[0:2, 0])   # convergence principale
ax_zoom   = fig.add_subplot(gs[0:2, 1])   # zoom zone de décharge
ax_bar    = fig.add_subplot(gs[2, 0])     # barres comparatives finales
ax_ratio  = fig.add_subplot(gs[2, 1])     # ratio kA/kB et kA/kC

x = np.arange(len(N_values))

# Palette
COL_A  = '#534AB7'   # purple  — G1
COL_B  = '#0F6E56'   # teal    — G2
COL_C  = '#BA7517'   # amber   — G3
COL_D1 = '#D85A30'   # coral   — Zone Décharge (1,29)
COL_D2 = '#993556'   # pink    — Zone Décharge (11,19)
COL_HL = '#888780'   # gray    — Hardy-Littlewood

# ── Graphique 1 : convergence des 3 constantes ───────────────────────────────

for data, err, col, lbl in [
    (kA, kA_err, COL_A, r'$k_A$ (G1) — complémentaires'),
    (kB, kB_err, COL_B, r'$k_B$ (G2) — non-complémentaires'),
    (kC, kC_err, COL_C, r'$k_C$ (G3) — résidus identiques'),
]:
    ax_main.fill_between(x, data - err, data + err, color=col, alpha=0.12)
    ax_main.plot(x, data, 'o-', color=col, linewidth=2, markersize=5,
                 label=lbl, zorder=3)

# Lignes de convergence asymptotique
for lim, col in [(KA_LIM, COL_A), (KB_LIM, COL_B), (KC_LIM, COL_C)]:
    ax_main.axhline(lim, color=col, linewidth=0.8, linestyle='--', alpha=0.5)

# Hardy-Littlewood référence
ax_main.plot(x, HL_ref, color=COL_HL, linewidth=1.2, linestyle=':',
             label='Référence Hardy-Littlewood', zorder=2)

ax_main.set_xticks(x)
ax_main.set_xticklabels(N_labels, fontsize=8)
ax_main.set_ylabel('Densité normalisée $k$', fontsize=10)
ax_main.set_title('Convergence des constantes / Constants convergence',
                  fontsize=10, pad=6)
ax_main.legend(fontsize=8, loc='lower right', framealpha=0.9)
ax_main.set_ylim(0.025, 0.155)
ax_main.set_facecolor('#F9F9F7')

# Annotations valeurs finales
for val, col, dy in [(KA_LIM, COL_A, 0.004),
                     (KB_LIM, COL_B, 0.004),
                     (KC_LIM, COL_C, 0.004)]:
    ax_main.annotate(f'{val:.4f}',
                     xy=(x[-1], val), xytext=(x[-1]+0.1, val+dy),
                     fontsize=8, color=col, fontweight='bold')

# ── Graphique 2 : Zone de Décharge (zoom G1) ─────────────────────────────────

ax_zoom.fill_between(x, kA - kA_err, kA + kA_err, color=COL_A, alpha=0.12)
ax_zoom.plot(x, kA, 'o-', color=COL_A, linewidth=2, markersize=5,
             label=r'$k_A$ moyenne G1')

ax_zoom.fill_between(x, kA_discharge_1_29 - kA_err*0.6,
                     kA_discharge_1_29 + kA_err*0.6,
                     color=COL_D1, alpha=0.15)
ax_zoom.plot(x, kA_discharge_1_29, 's--', color=COL_D1, linewidth=1.8,
             markersize=5, label='Tunnel (1, 29)')

ax_zoom.fill_between(x, kA_discharge_11_19 - kA_err*0.6,
                     kA_discharge_11_19 + kA_err*0.6,
                     color=COL_D2, alpha=0.15)
ax_zoom.plot(x, kA_discharge_11_19, '^--', color=COL_D2, linewidth=1.8,
             markersize=5, label='Tunnel (11, 19)')

# Flèche Zone de Décharge
mid = len(x) // 2
ax_zoom.annotate(
    'Zone de Décharge\n/ Discharge Zone',
    xy=(mid, kA_discharge_1_29[mid]),
    xytext=(mid - 2.5, kA_discharge_1_29[mid] - 0.016),
    arrowprops=dict(arrowstyle='->', color=COL_D1, lw=1.2),
    fontsize=8, color=COL_D1
)

ax_zoom.set_xticks(x)
ax_zoom.set_xticklabels(N_labels, fontsize=8)
ax_zoom.set_ylabel('Densité normalisée $k$', fontsize=10)
ax_zoom.set_title('Zone de Décharge — tunnels G1\nDischarge Zone — G1 tunnels',
                  fontsize=10, pad=6)
ax_zoom.legend(fontsize=8, loc='lower right', framealpha=0.9)
ax_zoom.set_facecolor('#F9F9F7')

# ── Graphique 3 : barres comparatives (valeurs finales à N=2×10⁸) ────────────

tunnels_labels = [
    '(1,29)\nG1', '(7,23)\nG1', '(11,19)\nG1', '(13,17)\nG1',
    '(1,7)\nG2', '(7,11)\nG2', '(1,13)\nG2', '(1,17)\nG2',
    '(1,1)\nG3', '(7,7)\nG3', '(11,11)\nG3', '(13,13)\nG3'
]
k_finals = [
    0.1200, 0.1247, 0.1215, 0.1247,   # G1 (avec décharge sur 1,29 et 11,19)
    0.0892, 0.0892, 0.0890, 0.0892,   # G2 sélection
    0.0634, 0.0634, 0.0634, 0.0634    # G3
]
colors_bar = (
    [COL_D1, COL_A, COL_D2, COL_A] +
    [COL_B] * 4 +
    [COL_C] * 4
)

bars = ax_bar.bar(range(len(tunnels_labels)), k_finals,
                  color=colors_bar, alpha=0.85, edgecolor='white',
                  linewidth=0.8, zorder=3)

# Ligne moyenne par type
for y_ref, col, start, end in [
    (KA_LIM, COL_A, -0.5, 3.5),
    (KB_LIM, COL_B, 3.5, 7.5),
    (KC_LIM, COL_C, 7.5, 11.5),
]:
    ax_bar.hlines(y_ref, start, end, color=col, linewidth=1.2,
                  linestyle='--', alpha=0.7, zorder=4)

ax_bar.set_xticks(range(len(tunnels_labels)))
ax_bar.set_xticklabels(tunnels_labels, fontsize=7, rotation=0)
ax_bar.set_ylabel('k (N = 2×10⁸)', fontsize=9)
ax_bar.set_title('Densités par tunnel (sélection)\nDensities by tunnel (selection)',
                 fontsize=10, pad=6)
ax_bar.set_ylim(0, 0.155)
ax_bar.set_facecolor('#F9F9F7')

# Légende type
legend_els = [
    Line2D([0],[0], color=COL_A, lw=2, label='G1 moyen / G1 avg'),
    Line2D([0],[0], color=COL_D1, lw=2, label='Zone Décharge (1,29)'),
    Line2D([0],[0], color=COL_D2, lw=2, label='Zone Décharge (11,19)'),
    Line2D([0],[0], color=COL_B, lw=2, label='G2'),
    Line2D([0],[0], color=COL_C, lw=2, label='G3'),
]
ax_bar.legend(handles=legend_els, fontsize=7, loc='upper right',
              ncol=2, framealpha=0.9)

# ── Graphique 4 : ratios kA/kB et kA/kC ─────────────────────────────────────

ratio_AB = kA / kB
ratio_AC = kA / kC

ax_ratio.plot(x, ratio_AB, 'o-', color=COL_A, linewidth=2, markersize=5,
              label=r'$k_A / k_B$')
ax_ratio.plot(x, ratio_AC, 's-', color=COL_C, linewidth=2, markersize=5,
              label=r'$k_A / k_C$')

# Valeurs asymptotiques
r_AB_lim = KA_LIM / KB_LIM
r_AC_lim = KA_LIM / KC_LIM
ax_ratio.axhline(r_AB_lim, color=COL_A, linewidth=0.8, linestyle='--', alpha=0.5)
ax_ratio.axhline(r_AC_lim, color=COL_C, linewidth=0.8, linestyle='--', alpha=0.5)

ax_ratio.annotate(f'{r_AB_lim:.3f}',
                  xy=(x[-1], r_AB_lim), xytext=(x[-1]-0.8, r_AB_lim+0.02),
                  fontsize=8, color=COL_A, fontweight='bold')
ax_ratio.annotate(f'{r_AC_lim:.3f}',
                  xy=(x[-1], r_AC_lim), xytext=(x[-1]-0.8, r_AC_lim+0.02),
                  fontsize=8, color=COL_C, fontweight='bold')

ax_ratio.set_xticks(x)
ax_ratio.set_xticklabels(N_labels, fontsize=8)
ax_ratio.set_ylabel('Ratio', fontsize=10)
ax_ratio.set_title(r'Ratios $k_A/k_B$ et $k_A/k_C$' + '\n' +
                   r'Ratios $k_A/k_B$ and $k_A/k_C$',
                   fontsize=10, pad=6)
ax_ratio.legend(fontsize=9, loc='lower right', framealpha=0.9)
ax_ratio.set_facecolor('#F9F9F7')

# ── Slider interactif (zoom sur la plage N) ───────────────────────────────────

ax_slider = fig.add_axes([0.12, 0.07, 0.55, 0.025])
slider = Slider(
    ax_slider, 'Plage N / N range',
    0, len(N_values) - 1,
    valinit=len(N_values) - 1,
    valstep=1,
    color=COL_A
)
ax_slider.set_facecolor('#F1EFE8')

def update(val):
    n_max = int(slider.val) + 1
    for ax, datasets in [
        (ax_main,  [(kA, kA_err, COL_A), (kB, kB_err, COL_B), (kC, kC_err, COL_C)]),
        (ax_zoom,  [(kA, kA_err, COL_A),
                    (kA_discharge_1_29,  kA_err*0.6, COL_D1),
                    (kA_discharge_11_19, kA_err*0.6, COL_D2)]),
    ]:
        for line, fill, _ in zip(ax.lines, ax.collections, datasets):
            pass  # lignes déjà tracées — on zoome seulement l'axe x
        ax.set_xlim(-0.3, n_max - 0.7)
        ax.set_xticks(range(n_max))
        ax.set_xticklabels(N_labels[:n_max], fontsize=8)
    ax_ratio.set_xlim(-0.3, n_max - 0.7)
    ax_ratio.set_xticks(range(n_max))
    ax_ratio.set_xticklabels(N_labels[:n_max], fontsize=8)
    fig.canvas.draw_idle()

slider.on_changed(update)

# ── CheckButtons : afficher/masquer séries ────────────────────────────────────

ax_check = fig.add_axes([0.72, 0.03, 0.25, 0.10])
ax_check.set_facecolor('#F1EFE8')
check = CheckButtons(
    ax_check,
    [r'$k_A$ G1', r'$k_B$ G2', r'$k_C$ G3', 'Hardy-Litt.'],
    [True, True, True, True]
)

def toggle(label):
    idx = [r'$k_A$ G1', r'$k_B$ G2', r'$k_C$ G3', 'Hardy-Litt.'].index(label)
    ax_main.lines[idx].set_visible(not ax_main.lines[idx].get_visible())
    fig.canvas.draw_idle()

check.on_clicked(toggle)

# ── Annotation générale ───────────────────────────────────────────────────────

fig.text(
    0.08, 0.015,
    'Validation computationnelle jusqu\'à N = 2×10⁸  ·  Computational validation up to N = 2×10⁸\n'
    'Conjecture Monfette : k_A, k_B, k_C > 0 pour tout N > 360  ·  for all N > 360',
    fontsize=8, color='#5F5E5A', ha='left', va='bottom'
)

plt.savefig('monfette_constants.png',
            dpi=150, bbox_inches='tight', facecolor='#FAFAF8')
print("PNG sauvegardé")
plt.show()
