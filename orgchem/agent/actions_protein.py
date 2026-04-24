"""Agent actions for Phase 24 — protein structure / ligand binding."""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="protein")
def list_seeded_proteins() -> List[Dict[str, str]]:
    """Enumerate the Phase 24a seeded teaching-protein set."""
    from orgchem.core.protein import list_seeded_proteins as _list
    return _list()


@action(category="protein")
def show_ligand_binding(pdb_id: str, ligand_name: str = "",
                        interaction_map_path: str = "",
                        ) -> Dict[str, Any]:
    """Bundled "show me <ligand> bound to <receptor>" workflow.

    One call does the three-step thing a tutor almost always wants:

    1. ``fetch_pdb(pdb_id)`` — download + cache the structure.
    2. ``analyse_binding(pdb_id, ligand_name)`` — geometric H-bond /
       salt-bridge / π-stacking / hydrophobic contacts between the
       ligand and every protein residue.
    3. *(optional)* ``export_interaction_map(...)`` — PoseView-style
       2D interaction diagram saved to ``interaction_map_path``.
    4. ``open_macromolecules_window(tab="Proteins")`` — focus the
       Proteins inner tab so the user sees the 3D viewer.

    Good starter queries:

    - ``pdb_id="2YDO", ligand_name="ADN"`` — adenosine A2A receptor
      with adenosine bound (canonical caffeine-receptor case study).
    - ``pdb_id="1EQG", ligand_name="IBP"`` — COX-1 with ibuprofen.
    - ``pdb_id="1HWK", ligand_name="115"`` — HMG-CoA reductase +
      atorvastatin.

    If ``ligand_name`` is empty, the action still fetches and shows
    the structure but skips the contact analysis.
    """
    from orgchem.sources.pdb import fetch_pdb as _fetch
    out: Dict[str, Any] = {"pdb_id": pdb_id.upper()}

    try:
        protein = _fetch(pdb_id)
    except Exception as e:  # noqa: BLE001
        return {"error": f"fetch_pdb failed: {e}"}
    out["summary"] = protein.summary()

    if ligand_name:
        try:
            from orgchem.core.binding_contacts import analyse_binding
            report = analyse_binding(protein, ligand_name)
            out["contacts"] = report.to_dict()
        except Exception as e:  # noqa: BLE001
            out["contacts_error"] = str(e)
        if interaction_map_path:
            try:
                from orgchem.render.draw_interaction_map import (
                    export_interaction_map as _render,
                )
                # `report` may not exist if the analyse_binding call
                # raised above — guard the export step accordingly.
                if out.get("contacts") is not None:
                    written = _render(report, interaction_map_path)
                    out["interaction_map_path"] = str(written)
            except Exception as e:  # noqa: BLE001
                out["interaction_map_error"] = str(e)

    # Best-effort GUI surfacing: bring up the Macromolecules
    # window's Proteins tab and populate the ID input. Deferred
    # onto the main Qt thread because the tutor panel runs agent
    # actions in a QThread worker, and macOS aborts if any
    # NSWindow is created off the main thread (reported 2026-04-23).
    try:
        from orgchem.agent.controller import main_window
        from orgchem.agent._gui_dispatch import run_on_main_thread
        win = main_window()
        if win is not None and hasattr(win, "open_macromolecules_window"):
            def _show():
                try:
                    win.open_macromolecules_window(tab_label="Proteins")
                    if hasattr(win, "proteins"):
                        win.proteins.id_input.setText(pdb_id.upper())
                except Exception:  # noqa: BLE001
                    log.exception(
                        "show_ligand_binding GUI dispatch failed")
            out["gui_shown"] = run_on_main_thread(_show)
        else:
            out["gui_shown"] = False
    except Exception:  # noqa: BLE001
        out["gui_shown"] = False
    return out


@action(category="protein")
def fetch_pdb(pdb_id: str) -> Dict[str, Any]:
    """Fetch a PDB structure from RCSB (cached locally).

    Returns a summary ``{"pdb_id", "title", "n_chains", "chain_ids",
    "n_residues", "n_atoms", "ligands", "has_water"}``. On first call
    the file lands in the OrgChem cache under ``pdb/``; subsequent
    calls are instant.
    """
    from orgchem.sources.pdb import fetch_pdb as _fetch
    try:
        protein = _fetch(pdb_id)
    except FileNotFoundError as e:
        return {"error": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:  # noqa: BLE001
        return {"error": f"Fetch failed: {e}"}
    return protein.summary()


@action(category="protein")
def get_protein_info(pdb_id: str) -> Dict[str, Any]:
    """Return a summary for a **cached** PDB entry (no network I/O)."""
    from orgchem.sources.pdb import parse_from_cache_or_string
    protein = parse_from_cache_or_string(pdb_id)
    if protein is None:
        return {"error": f"No cached entry for {pdb_id!r}. "
                         "Call fetch_pdb first."}
    return protein.summary()


@action(category="protein")
def fetch_alphafold(uniprot_id: str, version: int = 4) -> Dict[str, Any]:
    """Fetch an AlphaFold-predicted structure from EBI (AlphaFold DB).

    Returns a summary including mean pLDDT + confidence bucket (very
    high / confident / low / very low, matching the AlphaFold DB colour
    convention). The PDB is cached under
    ``~/Library/Caches/OrgChem/alphafold/``.
    """
    from orgchem.sources.alphafold import fetch_alphafold as _fetch
    try:
        r = _fetch(uniprot_id, version=version)
    except FileNotFoundError as e:
        return {"error": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:  # noqa: BLE001
        return {"error": f"AlphaFold fetch failed: {e}"}
    return r.summary()


@action(category="protein")
def get_alphafold_info(uniprot_id: str) -> Dict[str, Any]:
    """Summarise a **cached** AlphaFold model (no network I/O)."""
    from orgchem.sources.alphafold import parse_from_cache_or_string
    r = parse_from_cache_or_string(uniprot_id)
    if r is None:
        return {"error": f"No cached AlphaFold entry for {uniprot_id!r}. "
                         "Call fetch_alphafold first."}
    return r.summary()


@action(category="protein")
def find_binding_sites(pdb_id: str, top_k: int = 5) -> Dict[str, Any]:
    """Enumerate ranked binding pockets via the grid-based finder
    (Phase 24d). Uses the cached PDB — no network. Returns the top-K
    pockets with volume-voxel count, centroid, and the residues that
    line them.
    """
    from orgchem.sources.pdb import parse_from_cache_or_string
    from orgchem.core.pockets import find_pockets, pockets_summary
    protein = parse_from_cache_or_string(pdb_id)
    if protein is None:
        return {"error": f"No cached entry for {pdb_id!r}. "
                         "Call fetch_pdb first."}
    pockets = find_pockets(protein, top_k=top_k)
    summary = pockets_summary(pockets)
    summary["pdb_id"] = pdb_id.upper()
    return summary


@action(category="protein")
def analyse_binding(pdb_id: str, ligand_name: str) -> Dict[str, Any]:
    """Enumerate ligand-residue contacts (Phase 24e).

    Uses only cached PDB data — no network. Returns per-contact
    records classified as h-bond / salt-bridge / pi-stacking /
    hydrophobic, plus summary counts.
    """
    from orgchem.sources.pdb import parse_from_cache_or_string
    from orgchem.core.binding_contacts import analyse_binding as _analyse
    protein = parse_from_cache_or_string(pdb_id)
    if protein is None:
        return {"error": f"No cached entry for {pdb_id!r}. "
                         "Call fetch_pdb first."}
    report = _analyse(protein, ligand_name)
    return report.summary()


@action(category="protein")
def export_interaction_map(pdb_id: str, ligand_name: str,
                           path: str) -> Dict[str, Any]:
    """Render a 2D protein-ligand interaction map (Phase 24c).

    Uses the Phase 24e `analyse_binding` contacts and draws a
    PoseView-style radial diagram colour-coded by interaction type
    (H-bond blue, salt-bridge red, π-stacking purple, hydrophobic
    green). PNG or SVG by file extension.
    """
    from orgchem.sources.pdb import parse_from_cache_or_string
    from orgchem.core.binding_contacts import analyse_binding as _analyse
    from orgchem.render.draw_interaction_map import (
        export_interaction_map as _export,
    )
    from orgchem.messaging.errors import RenderError
    from pathlib import Path as _P

    protein = parse_from_cache_or_string(pdb_id)
    if protein is None:
        return {"error": f"No cached entry for {pdb_id!r}. "
                         "Call fetch_pdb first."}
    report = _analyse(protein, ligand_name)
    if report.n_contacts == 0:
        return {"error": f"No contacts found for ligand {ligand_name!r} "
                         f"in {pdb_id!r}."}
    try:
        out = _export(report, path)
    except RenderError as e:
        return {"error": str(e)}
    return {"path": str(out), "pdb_id": pdb_id.upper(),
            "ligand": report.ligand_name,
            "n_contacts": report.n_contacts,
            "format": _P(out).suffix.lstrip(".").lower(),
            "size_bytes": out.stat().st_size}


@action(category="protein")
def analyse_ppi(pdb_id: str) -> Dict[str, Any]:
    """Enumerate protein-protein interface contacts (Phase 24j).

    For every pair of chains with at least one non-covalent contact,
    classify each contact as h-bond / salt-bridge / pi-stacking /
    hydrophobic and list the interface residues on both sides.
    """
    from orgchem.sources.pdb import parse_from_cache_or_string
    from orgchem.core.ppi import analyse_ppi as _analyse, ppi_summary
    protein = parse_from_cache_or_string(pdb_id)
    if protein is None:
        return {"error": f"No cached entry for {pdb_id!r}. "
                         "Call fetch_pdb first."}
    interfaces = _analyse(protein)
    summary = ppi_summary(interfaces)
    summary["pdb_id"] = pdb_id.upper()
    return summary


@action(category="protein")
def analyse_ppi_pair(pdb_id: str, chain_a: str,
                     chain_b: str) -> Dict[str, Any]:
    """Analyse a specific chain pair's PPI contacts (Phase 24j)."""
    from orgchem.sources.pdb import parse_from_cache_or_string
    from orgchem.core.ppi import analyse_ppi_pair as _analyse_pair
    protein = parse_from_cache_or_string(pdb_id)
    if protein is None:
        return {"error": f"No cached entry for {pdb_id!r}. "
                         "Call fetch_pdb first."}
    iface = _analyse_pair(protein, chain_a, chain_b)
    summary = iface.summary()
    summary["pdb_id"] = pdb_id.upper()
    return summary


@action(category="protein")
def plip_capabilities() -> Dict[str, Any]:
    """Report whether PLIP is installed (Phase 24i)."""
    from orgchem.core.plip_bridge import capabilities
    return capabilities()


@action(category="protein")
def analyse_binding_plip(pdb_id: str, ligand_name: str,
                         require_plip: bool = False) -> Dict[str, Any]:
    """PLIP-enhanced binding analysis with graceful fallback (Phase 24i).

    Delegates to PLIP (Python API or CLI) when available; otherwise
    falls back to the built-in geometric analyser from Phase 24e. The
    ``engine`` key in the response tells you which code path ran.
    """
    from orgchem.sources.pdb import cached_pdb_path, parse_from_cache_or_string
    from orgchem.core.plip_bridge import analyse_binding_plip as _analyse
    protein = parse_from_cache_or_string(pdb_id)
    if protein is None:
        return {"error": f"No cached entry for {pdb_id!r}. "
                         "Call fetch_pdb first."}
    pdb_path = cached_pdb_path(pdb_id)
    result = _analyse(protein, ligand_name,
                      pdb_path=pdb_path if pdb_path.exists() else None,
                      require_plip=require_plip)
    summary = result.summary()
    summary["pdb_id"] = pdb_id.upper()
    return summary


@action(category="protein")
def export_protein_3d_html(pdb_id: str, path: str,
                           protein_style: str = "cartoon",
                           ligand_style: str = "ball-and-stick",
                           show_waters: bool = False,
                           show_ligand_surface: bool = False,
                           colour_mode: str = "chain",
                           spin: bool = False,
                           spin_axis: str = "y",
                           spin_speed: float = 1.0,
                           ) -> Dict[str, Any]:
    """Save an interactive 3D protein viewer HTML page (Phase 24l).

    Uses the cached PDB text (no network). Styles default to cartoon
    protein + ball-and-stick ligand; pass ``show_ligand_surface=True``
    for a pocket-view look, or ``show_waters=True`` to keep the water
    oxygens visible. ``colour_mode="plddt"`` reads the B-factor as
    AlphaFold pLDDT and applies the AlphaFold DB gradient.
    ``spin=True`` auto-rotates the scene — great for exporting a
    self-contained rotation-animation HTML.
    """
    from orgchem.sources.pdb import cached_pdb_path
    from orgchem.render.draw_protein_3d import build_protein_html_from_file
    p = cached_pdb_path(pdb_id)
    if not p.exists():
        return {"error": f"No cached PDB for {pdb_id!r}. "
                         "Call fetch_pdb first."}
    try:
        html = build_protein_html_from_file(
            p, protein_style=protein_style,
            ligand_style=ligand_style,
            show_waters=show_waters,
            show_ligand_surface=show_ligand_surface,
            colour_mode=colour_mode,
            spin=spin, spin_axis=spin_axis, spin_speed=spin_speed,
        )
    except FileNotFoundError as e:
        return {"error": str(e)}
    from pathlib import Path as _P
    out = _P(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return {"path": str(out.resolve()), "pdb_id": pdb_id.upper(),
            "size_bytes": out.stat().st_size,
            "protein_style": protein_style,
            "ligand_style": ligand_style,
            "colour_mode": colour_mode,
            "spin": spin}


@action(category="protein")
def analyse_na_binding(pdb_id: str, ligand_name: str) -> Dict[str, Any]:
    """Analyse ligand-nucleic-acid interactions (Phase 24k).

    Classifies contacts as intercalation, major-groove H-bond,
    minor-groove H-bond, or phosphate-backbone contact. Uses only the
    cached PDB — no network. Returns an empty report if the target
    isn't a DNA / RNA structure or the ligand isn't present.
    """
    from orgchem.sources.pdb import parse_from_cache_or_string
    from orgchem.core.na_interactions import analyse_na_binding as _analyse
    protein = parse_from_cache_or_string(pdb_id)
    if protein is None:
        return {"error": f"No cached entry for {pdb_id!r}. "
                         "Call fetch_pdb first."}
    report = _analyse(protein, ligand_name)
    return report.summary()


@action(category="protein")
def get_protein_chain_sequence(pdb_id: str, chain_id: str) -> Dict[str, Any]:
    """Return the 1-letter amino-acid sequence of one chain in a
    cached PDB entry."""
    from orgchem.sources.pdb import parse_from_cache_or_string
    protein = parse_from_cache_or_string(pdb_id)
    if protein is None:
        return {"error": f"No cached entry for {pdb_id!r}."}
    chain = protein.get_chain(chain_id)
    if chain is None:
        return {"error": f"Chain {chain_id!r} not in {pdb_id!r}. "
                         f"Available: {protein.chain_ids}"}
    return {"pdb_id": pdb_id.upper(), "chain_id": chain_id,
            "sequence": chain.sequence,
            "n_residues": len(chain.residues)}


def _get_sequence_panel():
    """Phase 34f — locate the live `SequenceBarPanel` on the
    Proteins tab, or return None if the GUI isn't up / the
    tab hasn't been instantiated.  Callers route all Qt
    state changes through this helper."""
    from orgchem.agent.controller import main_window
    win = main_window()
    if win is None:
        return None
    proteins = getattr(win, "proteins", None)
    if proteins is None:
        return None
    return getattr(proteins, "sequence_panel", None)


@action(category="protein")
def select_residues(pdb_id: str, chain_id: str,
                    start: int, end: int) -> Dict[str, Any]:
    """Phase 34f — programmatic sequence-bar selection.

    Sets the selection on the Proteins-tab sequence bar to
    ``chain_id:start-end`` (PDB-native residue numbering) and
    forwards the span to the live 3D viewer via the existing
    round-117 `orgchemHighlight` JS helper.  A single-residue
    selection passes ``start == end``.

    The ``pdb_id`` argument is advisory — the call operates on
    whatever structure is currently loaded in the Proteins tab.
    Returns ``{"status": "ok", "chain_id", "start", "end"}`` on
    success or ``{"error": ...}`` if the GUI isn't up or the
    bounds are invalid.
    """
    if start > end:
        start, end = end, start
    panel = _get_sequence_panel()
    if panel is None:
        return {"error": "Proteins sequence panel unavailable "
                         "(GUI not running or Proteins tab not open)."}
    from orgchem.agent._gui_dispatch import run_on_main_thread

    def _apply():
        panel.set_selection(str(chain_id), int(start), int(end))
        # set_selection on the bar doesn't fire selection_changed
        # (only user-driven gestures do), so push the highlight
        # to 3D directly here.
        from orgchem.agent.controller import main_window
        win = main_window()
        proteins = getattr(win, "proteins", None) if win else None
        if proteins is not None:
            proteins._on_sequence_selection(
                str(chain_id), int(start), int(end))

    ok = run_on_main_thread(_apply)
    if not ok:
        return {"error": "Failed to dispatch selection to the "
                         "GUI thread."}
    return {"status": "ok",
            "pdb_id": (pdb_id or "").upper(),
            "chain_id": str(chain_id),
            "start": int(start),
            "end": int(end)}


@action(category="protein")
def get_selection(pdb_id: str = "") -> Dict[str, Any]:
    """Phase 34f — current sequence-bar selection as
    ``{"chain_id", "start", "end"}`` or ``{"error": ...}`` when
    no selection exists / GUI unavailable.  Headless-safe."""
    panel = _get_sequence_panel()
    if panel is None:
        return {"error": "Proteins sequence panel unavailable."}
    sel = panel.bar.selection()
    if sel is None:
        return {"error": "No active selection."}
    chain_id, start, end = sel
    return {"pdb_id": (pdb_id or "").upper(),
            "chain_id": chain_id,
            "start": int(start),
            "end": int(end)}


@action(category="protein")
def clear_selection(pdb_id: str = "") -> Dict[str, Any]:
    """Phase 34f — clear the sequence-bar selection.  Also
    triggers `orgchemClearHighlight` on the live 3D viewer via
    the `ProteinPanel._on_sequence_cleared` handler."""
    panel = _get_sequence_panel()
    if panel is None:
        return {"error": "Proteins sequence panel unavailable."}
    from orgchem.agent._gui_dispatch import run_on_main_thread

    def _apply():
        panel.bar.clear_selection()

    ok = run_on_main_thread(_apply)
    if not ok:
        return {"error": "Failed to dispatch clear to the GUI thread."}
    return {"status": "ok", "pdb_id": (pdb_id or "").upper()}


@action(category="protein")
def get_sequence_view(pdb_id: str,
                      include_contacts: bool = False,
                      ligand_name: str = "") -> Dict[str, Any]:
    """Phase 34a — return the full :class:`SequenceView` for a
    cached PDB entry as a JSON-serialisable dict.

    Feeds the Phase 34b SequenceBar Qt widget + anyone driving
    structure browsing headlessly (tutor, scripting editor).
    Separates chains into ``protein_chains`` and ``dna_chains``
    by majority residue kind; each carries 1-letter code + per-
    residue seq_id list (PDB-native numbering).

    When ``include_contacts=True`` and ``ligand_name`` is given,
    also stamps a :class:`HighlightSpan` per contact residue
    (Phase 24e contact-kind colours) onto the returned
    ``highlights`` list — the same data the 3D viewer picks up.
    """
    from orgchem.sources.pdb import parse_from_cache_or_string
    from orgchem.core.sequence_view import (
        build_sequence_view, attach_contact_highlights,
    )
    protein = parse_from_cache_or_string(pdb_id)
    if protein is None:
        return {"error": f"No cached entry for {pdb_id!r}. "
                         "Call fetch_pdb first."}
    view = build_sequence_view(protein)
    if include_contacts and ligand_name:
        try:
            from orgchem.core.binding_contacts import analyse_binding
            report = analyse_binding(protein, ligand_name)
            attach_contact_highlights(view, report)
        except Exception as e:  # noqa: BLE001
            log.warning("contact overlay failed: %s", e)
    return view.to_dict()
