import sys
import math
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QFrame, QGridLayout,
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
)
from PySide6.QtGui import QPen, QBrush, QColor, QFont
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter



# -----------------------------
# Données et logique "mod 30"
# -----------------------------
R30 = [1, 7, 11, 13, 17, 19, 23, 29]
SG = {11, 23, 29}
XSG = {1, 7, 13, 17, 19}
CLASSES = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
PURE = {2, 8, 14, 20, 26, 12, 22}

TYPE_COLORS = {
    "AA": QColor("#f59e0b"),
    "CC": QColor("#38bdf8"),
    "AC": QColor("#a78bfa"),
}

def cls(r):
    return "SG" if r in SG else "XSG"

def cls_tunnel(a, b):
    if a in SG and b in SG:
        return "AA"
    if a not in SG and b not in SG:
        return "CC"
    return "AC"

def angle_deg(r):
    return r * 360 / 30

def angle_rad(r):
    return r * 2 * math.pi / 30

def polar(r, radius=120):
    a = angle_rad(r) - math.pi / 2  # 0° en haut
    return radius * math.cos(a), radius * math.sin(a)

def get_tunnels(nmod):
    tunnels = []
    for a in R30:
        for b in R30:
            if (a + b) % 30 == nmod % 30:
                tunnels.append((a, b, cls_tunnel(a, b)))
    return tunnels


# -----------------------------
# Vue graphique : cercle + tunnels
# -----------------------------
class CircleView(QGraphicsView):
    def __init__(self, info_label):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setSceneRect(-180, -180, 360, 360)
        self.info_label = info_label
        self.current_nmod = None
        self._build_static()


    def _build_static(self):
        self.scene.clear()

        # Fond
        bg = QGraphicsEllipseItem(-155, -155, 310, 310)
        bg.setBrush(QBrush(QColor("#080e1c")))
        bg.setPen(QPen(QColor("#0f172a"), 1))
        self.scene.addItem(bg)

        # Cercle principal
        circle = QGraphicsEllipseItem(-120, -120, 240, 240)
        circle.setBrush(Qt.NoBrush)
        circle.setPen(QPen(QColor("#1e2840"), 1.5))
        self.scene.addItem(circle)

        # Axes
        for a_deg in [0, 90, 180, 270]:
            a = math.radians(a_deg - 90)
            x2 = 130 * math.cos(a)
            y2 = 130 * math.sin(a)
            line = QGraphicsLineItem(0, 0, x2, y2)
            line.setPen(QPen(QColor("#0f172a"), 1))
            self.scene.addItem(line)

        # Marques 12°
        for i in range(30):
            a = math.radians(i * 12 - 90)
            r1 = 116
            r2 = 108 if i in R30 else 118
            x1 = r1 * math.cos(a)
            y1 = r1 * math.sin(a)
            x2 = r2 * math.cos(a)
            y2 = r2 * math.sin(a)
            pen = QPen(QColor("#1e3a5f") if i in R30 else QColor("#0f172a"),
                       1.5 if i in R30 else 0.5)
            mark = QGraphicsLineItem(x1, y1, x2, y2)
            mark.setPen(pen)
            self.scene.addItem(mark)

        # Points des résidus (sans état actif pour l'instant)
        for r in R30:
            x, y = polar(r, 120)
            color = QColor("#f59e0b") if r in SG else QColor("#38bdf8")
            R = 6
            outer = QGraphicsEllipseItem(x - (R + 3), y - (R + 3), 2 * (R + 3), 2 * (R + 3))
            outer.setBrush(QBrush(color))
            outer.setPen(Qt.NoPen)
            outer.setOpacity(0.05)
            self.scene.addItem(outer)

            inner = QGraphicsEllipseItem(x - R, y - R, 2 * R, 2 * R)
            inner.setBrush(QBrush(color))
            inner.setPen(QPen(QColor("#0a0c14"), 1.5))
            inner.setOpacity(0.4)
            self.scene.addItem(inner)

            # Label r
            lx, ly = polar(r, 140)
            text = self.scene.addText(str(r), QFont("Space Mono", 9))
            text.setDefaultTextColor(QColor("#334155"))
            text.setPos(lx - text.boundingRect().width() / 2,
                        ly - text.boundingRect().height() / 2)

        # Centre
        center = QGraphicsEllipseItem(-3, -3, 6, 6)
        center.setBrush(QBrush(QColor("#334155")))
        center.setPen(Qt.NoPen)
        self.scene.addItem(center)

        # Légende SG/XSG
        legend_items = [
            (-200, 135, QColor("#f59e0b"), "SG  = {11,23,29}"),
            (-200, 148, QColor("#38bdf8"), "XSG = {1,7,13,17,19}"),
        ]
        for x, y, c, txt in legend_items:
            dot = QGraphicsEllipseItem(x, y - 8, 8, 8)
            dot.setBrush(QBrush(c))
            dot.setPen(Qt.NoPen)
            self.scene.addItem(dot)
            t = self.scene.addText(txt, QFont("Space Mono", 9))
            t.setDefaultTextColor(c)
            t.setPos(x + 12, y - t.boundingRect().height() / 2)

    def draw_for_class(self, nmod):
        self.current_nmod = nmod
        self._build_static()

        # Tunnels actifs
        tunnels = get_tunnels(nmod)
        for a, b, ttype in tunnels:
            x1, y1 = polar(a, 120)
            x2, y2 = polar(b, 120)
            color = TYPE_COLORS[ttype]
            pen = QPen(color, 1.8)
            if a == b:
                pen.setWidthF(0.0)
            pen.setStyle(Qt.DashLine if a != b else Qt.SolidLine)
            line = QGraphicsLineItem(x1, y1, x2, y2)
            line.setPen(pen)
            line.setOpacity(0.5)
            self.scene.addItem(line)

        # Angle cible N
        aN = math.radians(nmod * 12 - 90)
        xN = 100 * math.cos(aN)
        yN = 100 * math.sin(aN)
        arrow = QGraphicsLineItem(0, 0, xN, yN)
        arrow.setPen(QPen(QColor("#f59e0b"), 2.5))
        arrow.setOpacity(0.8)
        self.scene.addItem(arrow)

        cx = 120 * math.cos(aN)
        cy = 120 * math.sin(aN)
        circ = QGraphicsEllipseItem(cx - 6, cy - 6, 12, 12)
        circ.setBrush(QBrush(QColor("#f59e0b")))
        circ.setPen(QPen(QColor("#f59e0b"), 1.5))
        circ.setOpacity(0.3)
        self.scene.addItem(circ)

        # Points des résidus (version "active")
        for r in R30:
            x, y = polar(r, 120)
            color = QColor("#f59e0b") if r in SG else QColor("#38bdf8")
            is_active = any((a == r or b == r) for a, b, _ in tunnels)
            R = 9 if is_active else 6

            outer = QGraphicsEllipseItem(x - (R + 3), y - (R + 3), 2 * (R + 3), 2 * (R + 3))
            outer.setBrush(QBrush(color))
            outer.setPen(Qt.NoPen)
            outer.setOpacity(0.15 if is_active else 0.05)
            self.scene.addItem(outer)

            inner = QGraphicsEllipseItem(x - R, y - R, 2 * R, 2 * R)
            inner.setBrush(QBrush(color))
            inner.setPen(QPen(QColor("#0a0c14"), 1.5))
            inner.setOpacity(1.0 if is_active else 0.4)
            self.scene.addItem(inner)

            # Label r
            lx, ly = polar(r, 140)
            text = self.scene.addText(str(r), QFont("Space Mono", 10 if is_active else 9))
            text.setDefaultTextColor(color if is_active else QColor("#334155"))
            text.setPos(lx - text.boundingRect().width() / 2,
                        ly - text.boundingRect().height() / 2)

            # Angle en degrés si actif
            if is_active:
                ax, ay = polar(r, 152)
                tdeg = self.scene.addText(f"{angle_deg(r):.0f}°", QFont("Space Mono", 8))
                tdeg.setDefaultTextColor(QColor("#475569"))
                tdeg.setPos(ax - tdeg.boundingRect().width() / 2,
                            ay - tdeg.boundingRect().height() / 2)

        self.update_info(nmod)

    def update_info(self, nmod):
        if nmod is None:
            self.info_label.setText(
                "<b>Cliquez sur une classe N mod 30</b> pour voir les tunnels actifs sur le cercle.<br>"
                "Chaque résidu r ∈ ℝ₃₀ est placé à l'angle <b>θ = r × 2π/30</b>.<br>"
                "La contrainte tunnel: <b>θ_p + θ_q ≡ θ_N (mod 2π)</b> — invariant angulaire."
            )
            return

        tunnels = get_tunnels(nmod)
        types = sorted(set(t for _, _, t in tunnels))
        angleN = (nmod * 12) % 360
        is_pure = nmod in PURE

        def type_span(tp):
            n = sum(1 for _, _, t in tunnels if t == tp)
            cls = "sg" if tp == "AA" else "xsg" if tp == "CC" else "ac"
            return f'<span class="{cls}">{tp}({n})</span>'

        type_desc = " + ".join(type_span(tp) for tp in types)

        tunnel_list = []
        for a, b, t in tunnels[:6]:
            cls = "sg" if t == "AA" else "xsg" if t == "CC" else "ac"
            tunnel_list.append(f'<span class="{cls}">({a},{b})</span>')
        extra = ""
        if len(tunnels) > 6:
            extra = f'  <span style="color:#475569">+{len(tunnels)-6} autres</span>'

        html = f"""
        <b>N ≡ {nmod} mod 30</b> {'<span class="sg">★ PURE</span>' if is_pure else ''}<br>
        Angle cible : <b>θ_N = {angleN}°</b>  ({(nmod*2*math.pi/30):.4f} rad)<br>
        Types actifs : {type_desc}  ·  {len(tunnels)} tunnels<br>
        Tunnels : {'  '.join(tunnel_list)}{extra}<br>
        <span style="color:#27ae60">
        Invariant : pour chaque tunnel (a,b) ci-dessus, a×12° + b×12° ≡ {angleN}° (mod 360°)
        </span>
        """
        self.info_label.setText(html)


# -----------------------------
# Fenêtre principale
# -----------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goldbach — Cercle Radian & Tunnels (Python)")
        self.resize(1100, 720)

        main_layout = QVBoxLayout(self)

        # Header
        header = QLabel(
            "<h2>Goldbach — Cercle Radian &amp; Tunnels</h2>"
            "<div style='color:#64748b;font-size:11px;'>"
            "Structure géométrique de (ℤ/30ℤ)★ · Loi p-e Monfette · 2026"
            "</div>"
        )
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Layout principal : gauche = cercle, droite = tables
        layout = QHBoxLayout()
        main_layout.addLayout(layout)


        # --------------------------------------------------------
        # Panneau : Invariant angulaire
        # --------------------------------------------------------
        inv = QLabel(
            "<div style='background:#0f1a0a; border:1px solid #27AE60; "
            "border-radius:10px; padding:10px; font-size:10px; line-height:1.0;'>"
            "<span style='color:#FFFFFF;font-size:12px;'>✦ Invariant angulaire (nouveau résultat)</span><br>"
            "<span style='color:#FFFFFF;font-size:12px;'>Pour tout tunnel (a,b) actif pour N :</span><br>"
            "<span style='color:#FFFFFF;font-size:12px;'>θ_a + θ_b ≡ θ_N (mod 2π)</span><br>"
            "<span style='color:#FFFFFF;font-size:12px;'>où θ_r = r × 2π/30.</span><br>"
            "<span style='color:#FFFFFF;font-size:12px;'>Tous les tunnels actifs convergent vers le même angle N×12°.</span><br>"
            "<span style='color:#FFFFFF;font-size:12px;'>→ La contrainte de Goldbach est une contrainte de phase sur le cercle.</span><br>"

        )
        inv.setWordWrap(True)
        inv.setTextFormat(Qt.RichText)
        main_layout.addWidget(inv)


        # ---- Colonne gauche : cercle + contrôles + info ----
        left = QVBoxLayout()
        layout.addLayout(left, 2)

        # Boutons classes
        ctrl_layout = QHBoxLayout()
        left.addLayout(ctrl_layout)
        self.class_buttons = {}

        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.info_label.setTextFormat(Qt.RichText)
        self.info_label.setStyleSheet("font-size:11px; color:#000000;")
        self.info_label.setMinimumHeight(90)

        self.circle_view = CircleView(self.info_label)
        left.addWidget(self.circle_view, 1)

        # Construire les boutons
        for nm in CLASSES:
            btn = QPushButton(f"N≡{nm}")
            btn.setCheckable(True)
            btn.setStyleSheet(
                "QPushButton { font-size:11px; padding:4px 8px; }"
                "QPushButton:checked { background:#1a1200; color:#f59e0b; border:1px solid #f59e0b; }"
            )
            btn.clicked.connect(self.make_class_handler(nm))
            ctrl_layout.addWidget(btn)
            self.class_buttons[nm] = btn

        left.addWidget(self.info_label)


        # ---- Colonne droite : tables côte à côte ----
        right = QHBoxLayout()
        layout.addLayout(right, 3)
        
        # --- Table résidus ---
        residu_frame = QFrame()
        residu_layout = QVBoxLayout(residu_frame)
        lbl_res = QLabel("Les 8 résidus sur le cercle")
        lbl_res.setStyleSheet("font-weight:bold; font-size:13px;")
        residu_layout.addWidget(lbl_res)
        
        self.residu_table = QTableWidget(0, 4)
        self.residu_table.setHorizontalHeaderLabels(["r", "θ (°)", "θ (rad)", "Classe"])
        self.residu_table.verticalHeader().setVisible(False)
        self.residu_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.residu_table.setSelectionMode(QTableWidget.NoSelection)
        residu_layout.addWidget(self.residu_table)
        
        right.addWidget(residu_frame, 1)
        
        # --- Table tunnels ---
        tunnel_frame = QFrame()
        tunnel_layout = QVBoxLayout(tunnel_frame)
        lbl_tun = QLabel("Table déterministe N mod 30 → Tunnels")
        lbl_tun.setStyleSheet("font-weight:bold; font-size:13px;")
        tunnel_layout.addWidget(lbl_tun)
        
        self.tunnel_table = QTableWidget(0, 4)
        self.tunnel_table.setHorizontalHeaderLabels(["N mod 30", "Angle θ_N", "Types", "# Tunnels"])
        self.tunnel_table.verticalHeader().setVisible(False)
        self.tunnel_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tunnel_table.setSelectionMode(QTableWidget.NoSelection)
        tunnel_layout.addWidget(self.tunnel_table)
        
        right.addWidget(tunnel_frame, 1)
 

        # Remplir les tables
        self.populate_residu_table()
        self.populate_tunnel_table()

        # État initial
        self.circle_view.update_info(None)

    def make_class_handler(self, nm):
        def handler():
            # décocher les autres
            for k, b in self.class_buttons.items():
                if k != nm:
                    b.setChecked(False)
            self.class_buttons[nm].setChecked(True)
            self.circle_view.draw_for_class(nm)
        return handler

    def populate_residu_table(self):
        self.residu_table.setRowCount(len(R30))
        for i, r in enumerate(R30):
            deg = angle_deg(r)
            rad = angle_rad(r)
            cls_str = cls(r)
            items = [
                QTableWidgetItem(str(r)),
                QTableWidgetItem(f"{deg:.0f}°"),
                QTableWidgetItem(f"{rad:.4f}"),
                QTableWidgetItem(cls_str),
            ]
            for j, it in enumerate(items):
                if cls_str == "SG":
                    it.setForeground(QColor("#f59e0b"))
                else:
                    it.setForeground(QColor("#38bdf8"))
                self.residu_table.setItem(i, j, it)
        self.residu_table.resizeColumnsToContents()

    def populate_tunnel_table(self):
        self.tunnel_table.setRowCount(len(CLASSES))
        for i, nm in enumerate(CLASSES):
            tunnels = get_tunnels(nm)
            types = sorted(set(t for _, _, t in tunnels))
            type_str_parts = []
            for tp in types:
                color = TYPE_COLORS[tp]
                txt = f"{tp}"
                item = QTableWidgetItem(txt)
                item.setForeground(color)
                # On ne peut pas mettre du HTML dans QTableWidgetItem, donc on concatène à côté
                type_str_parts.append(txt)
            type_str = " + ".join(type_str_parts)

            is_pure = nm in PURE
            star = "★ " if is_pure else ""
            row_items = [
                QTableWidgetItem(f"{star}{nm}"),
                QTableWidgetItem(f"{(nm*12)%360}°"),
                QTableWidgetItem(type_str),
                QTableWidgetItem(str(len(tunnels))),
            ]
            for j, it in enumerate(row_items):
                if is_pure and j == 0:
                    it.setForeground(QColor("#f59e0b"))
                    font = it.font()
                    font.setBold(True)
                    it.setFont(font)
                self.tunnel_table.setItem(i, j, it)
        self.tunnel_table.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
