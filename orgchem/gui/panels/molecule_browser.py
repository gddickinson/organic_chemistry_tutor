"""Left dock: searchable list of molecules in the local database."""
from __future__ import annotations
import logging

from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QMimeData, QByteArray
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListView, QLineEdit, QHBoxLayout, QLabel, QPushButton,
    QAbstractItemView, QComboBox,
)

from orgchem.messaging.bus import bus
from orgchem.db.queries import (
    list_molecules, query_by_tags, list_molecule_category_values,
)

log = logging.getLogger(__name__)


#: Must match the constant in orgchem.gui.panels.compare_panel — kept in sync
#: by convention, not a shared import (the two panels don't depend on each
#: other otherwise).
_MIME_MOLECULE_ID = "application/x-orgchem-molecule-id"


class _MolListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self._rows: list = []

    def reload(self, query: str = "",
               axis_a: str = "", value_a: str = "",
               axis_b: str = "", value_b: str = "") -> None:
        """Reload rows, optionally constrained by tag axes."""
        self.beginResetModel()
        if axis_a or axis_b:
            self._rows = query_by_tags(
                axis_a=axis_a or None, value_a=value_a or None,
                axis_b=axis_b or None, value_b=value_b or None,
                text_query=query or None,
            )
        else:
            self._rows = list_molecules(query=query or None)
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._rows)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row = self._rows[index.row()]
        if role == Qt.DisplayRole:
            return f"{row.name}   [{row.formula or '?'}]"
        if role == Qt.UserRole:
            return row.id
        if role == Qt.ToolTipRole:
            return row.smiles
        return None

    # ---- drag support ------------------------------------------------

    def flags(self, index):
        base = super().flags(index)
        if index.isValid():
            return base | Qt.ItemIsDragEnabled
        return base

    def mimeTypes(self):   # noqa: N802 — Qt override signature
        return [_MIME_MOLECULE_ID]

    def mimeData(self, indexes):   # noqa: N802
        md = QMimeData()
        for idx in indexes:
            if idx.isValid():
                row = self._rows[idx.row()]
                md.setData(_MIME_MOLECULE_ID,
                           QByteArray(str(row.id).encode()))
                break   # single-row drag is enough
        return md


class MoleculeBrowserPanel(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 4, 4, 4)

        top = QHBoxLayout()
        self.filter = QLineEdit()
        self.filter.setPlaceholderText("Filter by name, formula, SMILES…")
        self.filter.textChanged.connect(self._on_filter)
        refresh = QPushButton("↻")
        refresh.setFixedWidth(28)
        refresh.clicked.connect(self._reload)
        top.addWidget(QLabel("Filter:"))
        top.addWidget(self.filter)
        top.addWidget(refresh)
        lay.addLayout(top)

        # Phase 28d — two rolling axis/value combos + result-count label.
        self._axis_values: dict = list_molecule_category_values()
        self.axis_a = QComboBox()
        self.value_a = QComboBox()
        self.axis_b = QComboBox()
        self.value_b = QComboBox()
        for combo in (self.axis_a, self.axis_b):
            combo.addItem("(none)", "")
            for ax in self._axis_values.keys():
                combo.addItem(ax, ax)
            combo.currentIndexChanged.connect(self._on_axis_changed)
        for combo in (self.value_a, self.value_b):
            combo.addItem("(any)", "")
            combo.currentIndexChanged.connect(self._on_filter)
        self.axis_a.currentIndexChanged.connect(
            lambda _=0: self._refill_value(self.axis_a, self.value_a))
        self.axis_b.currentIndexChanged.connect(
            lambda _=0: self._refill_value(self.axis_b, self.value_b))

        filter_row1 = QHBoxLayout()
        filter_row1.addWidget(QLabel("A:"))
        filter_row1.addWidget(self.axis_a)
        filter_row1.addWidget(self.value_a, 1)
        lay.addLayout(filter_row1)
        filter_row2 = QHBoxLayout()
        filter_row2.addWidget(QLabel("B:"))
        filter_row2.addWidget(self.axis_b)
        filter_row2.addWidget(self.value_b, 1)
        self.clear_btn = QPushButton("Clear filters")
        self.clear_btn.clicked.connect(self._on_clear_filters)
        filter_row2.addWidget(self.clear_btn)
        lay.addLayout(filter_row2)

        self.count_label = QLabel("")
        self.count_label.setStyleSheet(
            "color:#555; font-size:11px; padding:2px;")
        lay.addWidget(self.count_label)

        self.model = _MolListModel()
        self.view = QListView()
        self.view.setModel(self.model)
        self.view.clicked.connect(self._on_clicked)
        self.view.setDragEnabled(True)
        self.view.setDragDropMode(QAbstractItemView.DragOnly)
        self.view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.view.setToolTip(
            "Drag a molecule into a Compare slot, or click to display."
        )
        lay.addWidget(self.view)

        bus().database_changed.connect(self._reload)
        self._reload()

    def _reload(self) -> None:
        self.model.reload(
            self.filter.text(),
            axis_a=self.axis_a.currentData() or "",
            value_a=self.value_a.currentData() or "",
            axis_b=self.axis_b.currentData() or "",
            value_b=self.value_b.currentData() or "",
        )
        self._update_count()

    def _on_filter(self, *_) -> None:
        self._reload()

    def _on_axis_changed(self, *_) -> None:
        self._reload()

    def _refill_value(self, axis_combo: QComboBox,
                      value_combo: QComboBox) -> None:
        """Swap the value-combo contents to match the selected axis."""
        axis = axis_combo.currentData() or ""
        value_combo.blockSignals(True)
        value_combo.clear()
        value_combo.addItem("(any)", "")
        for v in self._axis_values.get(axis, []):
            value_combo.addItem(v, v)
        value_combo.blockSignals(False)
        self._reload()

    def _on_clear_filters(self) -> None:
        self.filter.clear()
        self.axis_a.setCurrentIndex(0)
        self.axis_b.setCurrentIndex(0)
        self.value_a.clear()
        self.value_a.addItem("(any)", "")
        self.value_b.clear()
        self.value_b.addItem("(any)", "")
        self._reload()

    def _update_count(self) -> None:
        self.count_label.setText(f"{self.model.rowCount()} molecule(s)")

    def _on_clicked(self, idx) -> None:
        mol_id = self.model.data(idx, Qt.UserRole)
        if mol_id is not None:
            bus().molecule_selected.emit(int(mol_id))
