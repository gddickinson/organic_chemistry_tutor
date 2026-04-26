"""Phase 48b (round 171) — *Tools → Isomer relationships…*
dialog.

Tabbed singleton modeless dialog backed by
:mod:`orgchem.core.isomers`.  Three tabs: **Stereoisomers**
(SMILES → list of stereoisomer canonical SMILES),
**Tautomers** (SMILES → list of tautomer canonical SMILES),
**Classify pair** (two SMILES → relationship string from the
canonical RELATIONSHIPS vocabulary).

Singleton modeless — `IsomerExplorerDialog.singleton(parent)`
returns the same instance across opens so the user's last
input persists.  Wired through *Tools → Isomer
relationships…* (Ctrl+Shift+B).
"""
from __future__ import annotations
import logging
from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSpinBox,
    QTabWidget, QTextBrowser, QVBoxLayout, QWidget,
)

from orgchem.core.isomers import (
    classify_isomer_relationship, enumerate_stereoisomers,
    enumerate_tautomers, molecular_formula,
)

log = logging.getLogger(__name__)


# Map RELATIONSHIPS string → human-friendly label + colour.
_RELATIONSHIP_LABELS = {
    "identical":          ("Identical molecules",
                           "#1B6E1B"),
    "constitutional":     ("Constitutional / structural "
                           "isomers", "#0066CC"),
    "enantiomer":         ("Enantiomers (mirror images)",
                           "#9933CC"),
    "diastereomer":       ("Diastereomers", "#9933CC"),
    "meso":               ("Meso compound", "#9933CC"),
    "tautomer":           ("Tautomers (proton-transfer "
                           "isomers)", "#CC6600"),
    "different-molecule": ("Different molecules — not "
                           "isomers", "#666666"),
}


class IsomerExplorerDialog(QDialog):
    """Tabbed isomer-relationship explorer."""

    _instance: Optional["IsomerExplorerDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "IsomerExplorerDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Isomer relationships")
        self.setModal(False)
        self.resize(840, 620)
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8)

        self._tabs = QTabWidget()
        self._tabs.addTab(self._build_stereo_tab(),
                          "Stereoisomers")
        self._tabs.addTab(self._build_tautomer_tab(),
                          "Tautomers")
        self._tabs.addTab(self._build_classify_tab(),
                          "Classify pair")
        outer.addWidget(self._tabs, 1)

        footer = QHBoxLayout()
        footer.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        footer.addWidget(close_btn)
        outer.addLayout(footer)

    # ---------- Stereoisomers tab ----------
    def _build_stereo_tab(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)

        row = QHBoxLayout()
        row.addWidget(QLabel("SMILES:"))
        self._stereo_smiles = QLineEdit()
        self._stereo_smiles.setPlaceholderText(
            "e.g. CC(O)C(O)CO  (under-specified — expands to "
            "every stereoisomer)")
        row.addWidget(self._stereo_smiles, 1)
        row.addWidget(QLabel("Max:"))
        self._stereo_max = QSpinBox()
        self._stereo_max.setRange(1, 64)
        self._stereo_max.setValue(16)
        row.addWidget(self._stereo_max)
        run_btn = QPushButton("Enumerate")
        run_btn.clicked.connect(self._on_stereo_run)
        row.addWidget(run_btn)
        lay.addLayout(row)

        self._stereo_meta = QLabel("")
        self._stereo_meta.setWordWrap(True)
        lay.addWidget(self._stereo_meta)
        self._stereo_list = QListWidget()
        lay.addWidget(self._stereo_list, 1)
        return page

    def _on_stereo_run(self) -> None:
        smi = self._stereo_smiles.text().strip()
        if not smi:
            self._stereo_meta.setText(
                "<i>Enter a SMILES above.</i>")
            self._stereo_list.clear()
            return
        cap = self._stereo_max.value()
        res = enumerate_stereoisomers(smi, max_results=cap)
        self._populate_smiles_list(
            self._stereo_list, res.canonical_smiles_list)
        f = molecular_formula(smi) or "(unparseable)"
        meta = (f"<b>Input:</b> {_esc(smi)} "
                f"&nbsp;·&nbsp; <b>Formula:</b> "
                f"{_esc(f)} &nbsp;·&nbsp; "
                f"<b>Stereoisomers found:</b> "
                f"{len(res.canonical_smiles_list)}")
        if res.truncated:
            meta += (
                f" <span style='color:#C02020'>"
                f"(truncated at max={cap})</span>"
            )
        self._stereo_meta.setText(meta)

    # ---------- Tautomers tab ----------
    def _build_tautomer_tab(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)

        row = QHBoxLayout()
        row.addWidget(QLabel("SMILES:"))
        self._taut_smiles = QLineEdit()
        self._taut_smiles.setPlaceholderText(
            "e.g. CC(=O)CC(=O)C  (2,4-pentanedione)")
        row.addWidget(self._taut_smiles, 1)
        row.addWidget(QLabel("Max:"))
        self._taut_max = QSpinBox()
        self._taut_max.setRange(1, 64)
        self._taut_max.setValue(16)
        row.addWidget(self._taut_max)
        run_btn = QPushButton("Enumerate")
        run_btn.clicked.connect(self._on_taut_run)
        row.addWidget(run_btn)
        lay.addLayout(row)

        self._taut_meta = QLabel("")
        self._taut_meta.setWordWrap(True)
        lay.addWidget(self._taut_meta)
        self._taut_list = QListWidget()
        lay.addWidget(self._taut_list, 1)
        return page

    def _on_taut_run(self) -> None:
        smi = self._taut_smiles.text().strip()
        if not smi:
            self._taut_meta.setText(
                "<i>Enter a SMILES above.</i>")
            self._taut_list.clear()
            return
        cap = self._taut_max.value()
        res = enumerate_tautomers(smi, max_results=cap)
        self._populate_smiles_list(
            self._taut_list, res.canonical_smiles_list)
        f = molecular_formula(smi) or "(unparseable)"
        meta = (f"<b>Input:</b> {_esc(smi)} "
                f"&nbsp;·&nbsp; <b>Formula:</b> "
                f"{_esc(f)} &nbsp;·&nbsp; "
                f"<b>Tautomers found:</b> "
                f"{len(res.canonical_smiles_list)}")
        if res.truncated:
            meta += (
                f" <span style='color:#C02020'>"
                f"(truncated at max={cap})</span>"
            )
        self._taut_meta.setText(meta)

    # ---------- Classify-pair tab ----------
    def _build_classify_tab(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)

        row_a = QHBoxLayout()
        row_a.addWidget(QLabel("SMILES A:"))
        self._cls_a = QLineEdit()
        self._cls_a.setPlaceholderText(
            "e.g. C[C@H](O)C(=O)O  ((R)-lactic acid)")
        row_a.addWidget(self._cls_a, 1)
        lay.addLayout(row_a)

        row_b = QHBoxLayout()
        row_b.addWidget(QLabel("SMILES B:"))
        self._cls_b = QLineEdit()
        self._cls_b.setPlaceholderText(
            "e.g. C[C@@H](O)C(=O)O  ((S)-lactic acid)")
        row_b.addWidget(self._cls_b, 1)
        lay.addLayout(row_b)

        run_row = QHBoxLayout()
        run_row.addStretch(1)
        run_btn = QPushButton("Classify relationship")
        run_btn.clicked.connect(self._on_classify_run)
        run_row.addWidget(run_btn)
        lay.addLayout(run_row)

        self._cls_result = QTextBrowser()
        self._cls_result.setOpenExternalLinks(False)
        self._cls_result.setMinimumHeight(180)
        lay.addWidget(self._cls_result, 1)

        return page

    def _on_classify_run(self) -> None:
        a = self._cls_a.text().strip()
        b = self._cls_b.text().strip()
        if not a or not b:
            self._cls_result.setHtml(
                "<p><i>Enter both SMILES above.</i></p>")
            return
        rel = classify_isomer_relationship(a, b)
        label, colour = _RELATIONSHIP_LABELS.get(
            rel, (rel, "#000000"))
        f_a = molecular_formula(a) or "(unparseable)"
        f_b = molecular_formula(b) or "(unparseable)"
        body = (
            f"<h3 style='color:{colour}'>{_esc(label)}</h3>"
            f"<p><b>relationship:</b> "
            f"<code>{_esc(rel)}</code></p>"
            f"<table border='0' cellspacing='4' "
            f"cellpadding='3'>"
            f"<tr><th></th><th>SMILES</th><th>Formula</th>"
            f"</tr>"
            f"<tr><td><b>A</b></td>"
            f"<td><code>{_esc(a)}</code></td>"
            f"<td>{_esc(f_a)}</td></tr>"
            f"<tr><td><b>B</b></td>"
            f"<td><code>{_esc(b)}</code></td>"
            f"<td>{_esc(f_b)}</td></tr>"
            f"</table>"
        )
        # Brief explainer per relationship class.
        explainers = {
            "identical": (
                "<p>The two inputs canonicalise to the same "
                "SMILES (same connectivity AND same "
                "stereochemistry).</p>"
            ),
            "constitutional": (
                "<p>Same molecular formula, different "
                "connectivity.  Constitutional / structural "
                "isomers usually have distinct physical "
                "properties (bp, mp, logP, NMR shifts).</p>"
            ),
            "enantiomer": (
                "<p>Same connectivity, opposite stereochemistry "
                "at every stereocentre — non-superimposable "
                "mirror images.  Identical physical properties "
                "EXCEPT for opposite optical rotation + "
                "opposite biological activity at chiral "
                "receptors.</p>"
            ),
            "diastereomer": (
                "<p>Same connectivity, different stereochemistry "
                "but NOT mirror images.  Diastereomers have "
                "<i>different</i> physical properties — "
                "exploited for separation by ordinary "
                "(non-chiral) chromatography.</p>"
            ),
            "meso": (
                "<p>Contains stereocentres but is achiral "
                "overall — superimposable on its own mirror "
                "image because of an internal symmetry plane.</p>"
            ),
            "tautomer": (
                "<p>Different connectivity AND same molecular "
                "formula AND interconvert via proton transfer "
                "(plus a double-bond shift).  Tautomers are in "
                "dynamic equilibrium at ambient conditions.</p>"
            ),
            "different-molecule": (
                "<p>Different molecular formulas — these are "
                "not isomers of each other.</p>"
            ),
        }
        body += explainers.get(rel, "")
        self._cls_result.setHtml(body)

    # ---------- shared helpers ----------
    def _populate_smiles_list(
        self,
        list_widget: QListWidget,
        smiles_list: List[str],
    ) -> None:
        list_widget.clear()
        for smi in smiles_list:
            it = QListWidgetItem(smi)
            it.setData(Qt.UserRole, smi)
            list_widget.addItem(it)

    # ---------- Programmatic API for the agent action ----------
    def select_tab(self, label: str) -> bool:
        for i in range(self._tabs.count()):
            if self._tabs.tabText(i) == label:
                self._tabs.setCurrentIndex(i)
                return True
        return False

    def tab_labels(self) -> list:
        return [self._tabs.tabText(i)
                for i in range(self._tabs.count())]


def _esc(s: str) -> str:
    return ((s or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))
