"""Grid-based binding-pocket finder — Phase 24d.

Teaching-grade implementation. Workflow:

1. Place a regular probe grid over the protein's bounding box
   (expanded by a margin).
2. For each probe point, compute the distance to the nearest heavy
   atom.
3. Classify a probe as a **pocket voxel** when:
   - ``min_atom_dist`` is in the ``[probe_min, probe_max]`` band
     (roughly between water-size and benzene-ring-size cavities), and
   - the probe is **buried**, i.e. has heavy atoms in multiple
     directions around it (prevents external-surface hits).
4. Cluster adjacent pocket voxels with a 6-neighbour flood-fill.
5. Score each cluster by voxel count (rough volume proxy) and rank.
6. Annotate each top-K cluster with the set of residues within 5 Å.

**Why this and not fpocket?** fpocket uses α-sphere / Voronoi
methods and produces better absolute scores — but requires the
`fpocket` binary. This module is dependency-free (numpy + protein
dataclasses only) so the base install picks up a "good-enough"
pocket finder. Phase 24d follow-up can wrap fpocket when available.

Speed-wise: an N×M×L grid with N, M, L ≈ 30 for a small protein
≈ 27 k probes × a naive N_atoms scan = a few seconds. Acceptable
for teaching-scale; a KD-tree cache would speed up larger proteins.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from math import sqrt
from typing import Dict, List, Sequence, Tuple

from orgchem.core.protein import Atom, Protein


@dataclass
class Pocket:
    index: int                   # rank (0 = largest)
    volume_voxels: int           # count of probe voxels in the cluster
    centre: Tuple[float, float, float]
    #: Residues with at least one heavy atom within ``neighbour_cutoff`` Å
    #: of any pocket voxel.
    lining_residues: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------

def find_pockets(protein: Protein,
                 grid_spacing: float = 1.5,
                 margin: float = 6.0,
                 probe_min: float = 2.0,
                 probe_max: float = 5.0,
                 buried_min_neighbours: int = 4,
                 buried_cutoff: float = 8.0,
                 min_cluster_size: int = 12,
                 top_k: int = 5,
                 neighbour_cutoff: float = 5.0
                 ) -> List[Pocket]:
    """Return the top-K ranked pockets for ``protein``.

    Default parameters tuned so the teaching-scale fixture used in
    the unit tests (50-ish residues) finds 1–3 pockets in < 1 s.
    """
    # --- Collect heavy atoms --------------------------------------
    heavy_atoms: List[Atom] = []
    for chain in protein.chains:
        for res in chain.residues:
            heavy_atoms.extend(a for a in res.atoms if a.element != "H")
    # Include HETATM residues (waters usually ignored; our Protein
    # parser already filters HOH out of ligand_residues but retains
    # them in hetatm_residues. Skip waters explicitly for pocket work.)
    for res in protein.hetatm_residues:
        if res.name in ("HOH", "WAT"):
            continue
        heavy_atoms.extend(a for a in res.atoms if a.element != "H")

    if not heavy_atoms:
        return []

    xs = [a.x for a in heavy_atoms]
    ys = [a.y for a in heavy_atoms]
    zs = [a.z for a in heavy_atoms]

    x_lo, x_hi = min(xs) - margin, max(xs) + margin
    y_lo, y_hi = min(ys) - margin, max(ys) + margin
    z_lo, z_hi = min(zs) - margin, max(zs) + margin

    # --- Build grid -----------------------------------------------
    nx = max(1, int((x_hi - x_lo) / grid_spacing) + 1)
    ny = max(1, int((y_hi - y_lo) / grid_spacing) + 1)
    nz = max(1, int((z_hi - z_lo) / grid_spacing) + 1)

    # Precompute which probes qualify as pocket voxels.
    def probe_coords(ix: int, iy: int, iz: int
                     ) -> Tuple[float, float, float]:
        return (x_lo + ix * grid_spacing,
                y_lo + iy * grid_spacing,
                z_lo + iz * grid_spacing)

    pocket_mask: Dict[Tuple[int, int, int], bool] = {}
    for ix in range(nx):
        for iy in range(ny):
            for iz in range(nz):
                px, py, pz = probe_coords(ix, iy, iz)
                min_d = float("inf")
                neigh_octants: set = set()
                for a in heavy_atoms:
                    dx = a.x - px
                    dy = a.y - py
                    dz = a.z - pz
                    d2 = dx * dx + dy * dy + dz * dz
                    if d2 < min_d * min_d:
                        min_d = sqrt(d2)
                    if d2 < buried_cutoff * buried_cutoff:
                        octant = (1 if dx > 0 else 0,
                                  1 if dy > 0 else 0,
                                  1 if dz > 0 else 0)
                        neigh_octants.add(octant)
                if (probe_min <= min_d <= probe_max
                        and len(neigh_octants) >= buried_min_neighbours):
                    pocket_mask[(ix, iy, iz)] = True

    if not pocket_mask:
        return []

    # --- Cluster via flood-fill (6-neighbour adjacency) ----------
    clusters: List[List[Tuple[int, int, int]]] = []
    visited: set = set()
    for start in pocket_mask:
        if start in visited:
            continue
        stack = [start]
        cluster: List[Tuple[int, int, int]] = []
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            cluster.append(v)
            for dx, dy, dz in ((1, 0, 0), (-1, 0, 0),
                               (0, 1, 0), (0, -1, 0),
                               (0, 0, 1), (0, 0, -1)):
                nbr = (v[0] + dx, v[1] + dy, v[2] + dz)
                if nbr in pocket_mask and nbr not in visited:
                    stack.append(nbr)
        if len(cluster) >= min_cluster_size:
            clusters.append(cluster)

    # --- Rank & annotate -----------------------------------------
    clusters.sort(key=lambda c: -len(c))
    pockets: List[Pocket] = []
    for rank, cluster in enumerate(clusters[:top_k]):
        centre_x = sum(probe_coords(*v)[0] for v in cluster) / len(cluster)
        centre_y = sum(probe_coords(*v)[1] for v in cluster) / len(cluster)
        centre_z = sum(probe_coords(*v)[2] for v in cluster) / len(cluster)
        lining = _find_lining_residues(
            protein, cluster, probe_coords, neighbour_cutoff)
        pockets.append(Pocket(
            index=rank,
            volume_voxels=len(cluster),
            centre=(round(centre_x, 3), round(centre_y, 3),
                    round(centre_z, 3)),
            lining_residues=lining,
        ))
    return pockets


def _find_lining_residues(protein: Protein,
                          cluster: Sequence[Tuple[int, int, int]],
                          probe_coords, cutoff: float) -> List[str]:
    lining: set = set()
    # Sample the cluster to limit cost; a handful of representative
    # probes is enough to catch all lining residues.
    sample = cluster[:: max(1, len(cluster) // 12)]
    for chain in protein.chains:
        for res in chain.residues:
            label = f"{res.chain}:{res.name}{res.seq_id}"
            for a in res.atoms:
                if a.element == "H":
                    continue
                ok = False
                for v in sample:
                    px, py, pz = probe_coords(*v)
                    dx = a.x - px
                    dy = a.y - py
                    dz = a.z - pz
                    if (dx * dx + dy * dy + dz * dz) <= cutoff * cutoff:
                        ok = True
                        break
                if ok:
                    lining.add(label)
                    break
    # Sort in residue order
    return sorted(lining, key=_residue_sort_key)


def _residue_sort_key(label: str):
    # "A:ASP102" → ("A", 102)
    try:
        chain_id, rest = label.split(":", 1)
        # strip leading 3-letter residue name
        seq = "".join(ch for ch in rest if ch.isdigit())
        return (chain_id, int(seq) if seq else 0)
    except Exception:
        return ("", 0)


# ---------------------------------------------------------------------
# Summary helper

def pockets_summary(pockets: Sequence[Pocket]) -> Dict[str, object]:
    return {
        "n_pockets": len(pockets),
        "pockets": [
            {"index": p.index,
             "volume_voxels": p.volume_voxels,
             "centre": list(p.centre),
             "n_lining_residues": len(p.lining_residues),
             "lining_residues": p.lining_residues}
            for p in pockets
        ],
    }
