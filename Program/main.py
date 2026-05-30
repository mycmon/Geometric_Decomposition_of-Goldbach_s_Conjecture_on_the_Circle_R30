import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QGridLayout, QFrame
)
from PySide6.QtCore import Qt
import pyqtgraph as pg
from PySide6.QtWidgets import QScrollArea

# Importation des données RAW
from raw_data import RAW


# ------------------------------------------------------------
# Configurations des classes (couleurs Qt standard)
# ------------------------------------------------------------
CONFIGS = {
    "2":  {"sym": "(1,1)",   "asym": "(13,19)+(19,13)", "color": (255, 0, 128)},
    "4":  {"sym": "(17,17)", "asym": "(11,23)+(23,11)", "color": (255, 128, 0)},
    "8":  {"sym": "(19,19)", "asym": "(1,7)+(7,1)",      "color": (0, 180, 0)},
    "14": {"sym": "(7,7)",   "asym": "(1,13)+(13,1)",    "color": (0, 128, 255)},
    "16": {"sym": "(23,23)", "asym": "(17,29)+(29,17)",  "color": (160, 0, 255)},
    "22": {"sym": "(11,11)", "asym": "(23,29)+(29,23)",  "color": (255, 200, 0)},
    "26": {"sym": "(13,13)", "asym": "(7,19)+(19,7)",    "color": (255, 80, 80)},
    "28": {"sym": "(29,29)", "asym": "(11,17)+(17,11)",  "color": (0, 180, 255)},
}


# ------------------------------------------------------------
# Fenêtre principale
# ------------------------------------------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Système Monfette – Ratio Cumulatif (Qt6 Standard)")
        self.resize(1100, 2800)

        self.active = set(CONFIGS.keys())
        self.zoom_active = False

        layout = QVBoxLayout(self)
        
        # --------------------------------------------------------
        # Zone défilante pour les notes
        # --------------------------------------------------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        
        # --------------------------------------------------------
        # Bloc d'information : Note théorique
        # --------------------------------------------------------
        note1 = QLabel(
            "<b>Système Monfette · Asymétries SG/XSG · MOD 30</b><br>"
            "<br>"
            "Ratio cumulatif : Tunnels asymétriques / Tunnel symétrique<br>"
            "Pour chaque classe N ≡ k mod 30 avec tunnel symétrique (a,a), "
            "ratio (#asym) / (#sym) cumulatif sur N ∈ [3000, 297 000]<br>"
            "<br>"
            "<b>4 — LIMITE UNIVERSELLE</b><br>"
            "Pour toutes les 8 classes avec tunnel symétrique (a,a), "
            "le ratio cumulatif converge vers 4.<br>"
            "<br>"
            "Décomposition : ×2 orientation (deux tunnels (a,b) et (b,a)) × "
            "×2 densité (deux familles de résidus vs une)<br>"
            "<br>"
            "min à N=297k : 3.948<br>"
            "max à N=297k : 4.058<br>"
            "N→∞ prédit : 4.000<br>"
        )
        note1.setWordWrap(True)
        note1.setStyleSheet("font-size: 13px; padding: 6px;")
        scroll_layout.addWidget(note1)
        
        # --------------------------------------------------------
        # Bloc d'information : Valeurs finales
        # --------------------------------------------------------
        note2 = QLabel(
            "<b>Valeurs finales à N ≈ 297 000</b><br><br>"
            "N ≡ 26 mod 30 — 3.9481 — sym (13,13) — asym (7,19)+(19,7)<br>"
            "N ≡ 14 mod 30 — 3.9603 — sym (7,7) — asym (1,13)+(13,1)<br>"
            "N ≡ 22 mod 30 — 3.9904 — sym (11,11) — asym (23,29)+(29,23)<br>"
            "N ≡ 4 mod 30 — 3.9938 — sym (17,17) — asym (11,23)+(23,11)<br>"
            "N ≡ 16 mod 30 — 4.0043 — sym (23,23) — asym (17,29)+(29,17)<br>"
            "N ≡ 28 mod 30 — 4.0063 — sym (29,29) — asym (11,17)+(17,11)<br>"
            "N ≡ 8 mod 30 — 4.0296 — sym (19,19) — asym (1,7)+(7,1)<br>"
            "N ≡ 2 mod 30 — 4.0580 — sym (1,1) — asym (13,19)+(19,13)<br>"
            "<br>"
            "<i>Loi p–e Monfette · Calcul vectorisé numpy · Crible d'Ératosthène · N ∈ [3k, 297k]</i>"
        )
        note2.setWordWrap(True)
        note2.setStyleSheet("font-size: 13px; padding: 6px;")
        scroll_layout.addWidget(note2)
        
        # --------------------------------------------------------
        # Grille des valeurs finales (dans la zone scroll)
        # --------------------------------------------------------
        grid_frame = QFrame()
        grid_layout = QGridLayout(grid_frame)
        
        final_vals = []
        for cls, pts in RAW.items():
            final_vals.append((cls, pts[-1]["r"]))
        
        final_vals.sort(key=lambda x: x[1])
        
        for i, (cls, val) in enumerate(final_vals):
            lbl = QLabel(f"≡{cls} : {val:.4f}")
            grid_layout.addWidget(lbl, i // 4, i % 4)
        
        scroll_layout.addWidget(grid_frame)
        
        # --------------------------------------------------------
        # Graphique PyQtGraph (en dehors du scroll)
        # --------------------------------------------------------
        self.plot = pg.PlotWidget()
        self.plot.showGrid(x=True, y=True)
        self.plot.setLabel("left", "Ratio r")
        self.plot.setLabel("bottom", "N")
        self.plot.setYRange(3.0, 5.0)
        layout.addWidget(self.plot)
        
        # --------------------------------------------------------
        # Boutons
        # --------------------------------------------------------
        btn_row = QHBoxLayout()
        layout.addLayout(btn_row)


        self.btns = {}

        for cls, cfg in CONFIGS.items():
            btn = QPushButton(f"≡{cls}   {cfg['sym']}")
            btn.setCheckable(True)
            btn.setChecked(True)
            btn.clicked.connect(lambda _, c=cls: self.toggle_class(c))
            btn_row.addWidget(btn)
            self.btns[cls] = btn

        # Bouton Zoom
        self.btn_zoom = QPushButton("Zoom ×4±0.5")
        self.btn_zoom.clicked.connect(self.toggle_zoom)
        btn_row.addWidget(self.btn_zoom)

        # --------------------------------------------------------
        # Grille des valeurs finales
        # --------------------------------------------------------
        grid_frame = QFrame()
        grid_layout = QGridLayout(grid_frame)

        final_vals = []
        for cls, pts in RAW.items():
            final_vals.append((cls, pts[-1]["r"]))

        final_vals.sort(key=lambda x: x[1])

        for i, (cls, val) in enumerate(final_vals):
            lbl = QLabel(f"≡{cls} : {val:.4f}")
            grid_layout.addWidget(lbl, i // 4, i % 4)

        layout.addWidget(grid_frame)


        # --------------------------------------------------------
        # Tracer initial
        # --------------------------------------------------------
        self.update_plot()

    # ------------------------------------------------------------
    # Toggle d'une classe
    # ------------------------------------------------------------
    def toggle_class(self, cls):
        if cls in self.active:
            self.active.remove(cls)
        else:
            self.active.add(cls)
        self.update_plot()

    # ------------------------------------------------------------
    # Zoom structurel
    # ------------------------------------------------------------
    def toggle_zoom(self):
        self.zoom_active = not self.zoom_active
        if self.zoom_active:
            self.plot.setYRange(3.5, 4.5)
            self.btn_zoom.setText("Vue large")
        else:
            self.plot.setYRange(3.0, 5.0)
            self.btn_zoom.setText("Zoom ×4±0.5")

    # ------------------------------------------------------------
    # Mise à jour du graphe
    # ------------------------------------------------------------
    def update_plot(self):
        self.plot.clear()

        # Ligne horizontale Y=4
        self.plot.addLine(y=4, pen=pg.mkPen((255, 180, 0), width=2, style=Qt.DashLine))

        # Tracer chaque classe active
        for cls, cfg in CONFIGS.items():
            if cls not in self.active:
                continue

            pts = RAW[cls]
            xs = [p["N"] for p in pts]
            ys = [p["r"] for p in pts]

            pen = pg.mkPen(cfg["color"], width=2)
            self.plot.plot(xs, ys, pen=pen)


# ------------------------------------------------------------
# Lancement
# ------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
