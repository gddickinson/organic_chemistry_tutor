"""Correct seeded molecule rows whose structure was wrong in an earlier release.

Seeding is additive by name, so a DB created before a seed SMILES was fixed keeps the old structure forever. This
module rewrites those rows in place (matched by name AND the InChIKey of the old, wrong SMILES, so user-imported or
user-edited rows are left alone), then clears the cached 2D/3D molblocks so ``seed_coords.backfill_molblock_2d`` redraws them.

Current corrections (2026-11-12): Camphor, Codeine and Oxycodone carried stereo descriptors no 3D geometry can
satisfy (no 3D model could be built); a scan of every seeded molecule against PubChem then found 78 more rows whose
structure or stereochemistry disagreed with the name (e.g. the L-amino acids were seeded as D, Efavirenz and
Lycopene had the wrong skeleton). Replacement SMILES come from the PubChem records cited per row (stereo-only fixes
invert just the wrong centres of the seed SMILES, so a seed's chosen anomer is kept).
Idempotent: once corrected, the old InChIKeys no longer match anything.
"""
from __future__ import annotations

import json
import logging
from typing import List, Tuple

from orgchem.core.molecule import Molecule as ChemMol
from orgchem.db.models import Molecule as DBMol
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)

# (seeded name, InChIKey of the old wrong seed SMILES, corrected SMILES, source record)
CORRECTIONS: List[Tuple[str, str, str, str]] = [
    # 2026-11-12, round 1: impossible stereo (no 3D model could be built)
    ("Camphor", "DSSYKIVIOFKYAU-GMSGAONNSA-N",
     "CC1(C)[C@@H]2CC[C@@]1(C)C(=O)C2", "(+)-camphor (1R,4R), PubChem CID 159055, ChEBI:15396"),
    ("Codeine", "OROGSEYTTFOCAN-HKAKVCCISA-N",
     "CN1CC[C@]23c4c5ccc(OC)c4O[C@H]2[C@@H](O)C=C[C@H]3[C@H]1C5", "PubChem CID 5284371, ChEBI:16714"),
    ("Oxycodone (OxyContin)", "BRUQQQPBMZOVGD-BVPBIZIASA-N",
     "CN1CC[C@]23c4c5ccc(OC)c4O[C@H]2C(=O)CC[C@@]3(O)[C@H]1C5", "PubChem CID 5284603, ChEBI:7852"),
    # 2026-11-12, round 2: structure or stereo disagreed with the name (PubChem record by CID)
    ("Efavirenz", "FKENFPVUJSORLY-UHFFFAOYSA-N",
     "O=C1Nc2ccc(Cl)cc2[C@@](C#CC2CC2)(C(F)(F)F)O1", "structure: PubChem CID 64139"),
    ("Lycopene", "HMTPSOYBIKBXFY-UHFFFAOYSA-N",
     "CC(C)=CCC/C(C)=C/C=C/C(C)=C/C=C/C(C)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/C=C(\\C)CCC=C(C)C", "structure: PubChem CID 446925"),
    ("beta-Lactose", "GUBGYTABKSRVRQ-MFRLZQSSSA-N",
     "OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)[C@H](O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@H]1O", "stereo: PubChem CID 6134"),
    ("L-Alanine", "QNAYBMKLOCPYGJ-UWTATZPHSA-N",
     "C[C@H](N)C(=O)O", "stereo: PubChem CID 5950"),
    ("L-Valine", "KZSNJWFQEVHDMF-SCSAIBSYSA-N",
     "CC(C)[C@H](N)C(=O)O", "stereo: PubChem CID 6287"),
    ("L-Leucine", "ROHFNLRQFUQHCH-RXMQYKEDSA-N",
     "CC(C)C[C@H](N)C(=O)O", "stereo: PubChem CID 6106"),
    ("L-Isoleucine", "AGPKZVBTJJNPAG-CRCLSJGQSA-N",
     "CC[C@H](C)[C@H](N)C(=O)O", "stereo: PubChem CID 6306"),
    ("L-Methionine", "FFEARJCKVFRZRR-SCSAIBSYSA-N",
     "CSCC[C@H](N)C(=O)O", "stereo: PubChem CID 6137"),
    ("L-Serine", "MTCFGRXMJLQNBG-UWTATZPHSA-N",
     "N[C@@H](CO)C(=O)O", "stereo: PubChem CID 5951"),
    ("L-Threonine", "AYFVYJQAPQTCCC-STHAYSLISA-N",
     "C[C@@H](O)[C@H](N)C(=O)O", "stereo: PubChem CID 6288"),
    ("L-Asparagine", "DCXYFEDJOCDNAF-UWTATZPHSA-N",
     "NC(=O)C[C@H](N)C(=O)O", "stereo: PubChem CID 6267"),
    ("L-Glutamine", "ZDXPYRJPNDTMRX-GSVOUGTGSA-N",
     "NC(=O)CC[C@H](N)C(=O)O", "stereo: PubChem CID 5961"),
    ("L-Aspartic acid", "CKLJMWTZIZZHCS-UWTATZPHSA-N",
     "N[C@@H](CC(=O)O)C(=O)O", "stereo: PubChem CID 5960"),
    ("L-Glutamic acid", "WHUUTDBJXJRKMK-GSVOUGTGSA-N",
     "N[C@@H](CCC(=O)O)C(=O)O", "stereo: PubChem CID 33032"),
    ("L-Lysine", "KDXKERNSBIXSRK-RXMQYKEDSA-N",
     "NCCCC[C@H](N)C(=O)O", "stereo: PubChem CID 5962"),
    ("L-Arginine", "ODKSFYDXXFIFQN-SCSAIBSYSA-N",
     "NC(N)=NCCC[C@H](N)C(=O)O", "structure: PubChem CID 6322"),
    ("Amoxicillin", "LSQZJLSUYDQPKJ-BBGACYKPSA-N",
     "CC1(C)S[C@@H]2[C@H](NC(=O)[C@H](N)c3ccc(O)cc3)C(=O)N2[C@H]1C(=O)O", "stereo: PubChem CID 33613"),
    ("Oseltamivir", "VSZGPKBBMSAYNT-ILXRZTDVSA-N",
     "CCOC(=O)C1=C[C@@H](OC(CC)CC)[C@H](NC(C)=O)[C@@H](N)C1", "stereo: PubChem CID 65028"),
    ("Simvastatin", "RYMZZMVNJRMUDD-CGVMPUAYSA-N",
     "CCC(C)(C)C(=O)O[C@H]1C[C@@H](C)C=C2C=C[C@H](C)[C@H](CC[C@@H]3C[C@@H](O)CC(=O)O3)[C@H]21", "stereo: PubChem CID 54454"),
    ("Lovastatin", "PCZOHLXUXFIOCF-QQBYXSENSA-N",
     "CC[C@H](C)C(=O)O[C@H]1C[C@@H](C)C=C2C=C[C@H](C)[C@H](CC[C@@H]3C[C@@H](O)CC(=O)O3)[C@H]21", "stereo: PubChem CID 53232"),
    ("Enalapril", "GBXSMTUPTTWBMN-UAGQMJEPSA-N",
     "CCOC(=O)[C@H](CCc1ccccc1)N[C@@H](C)C(=O)N1CCC[C@H]1C(=O)O", "stereo: PubChem CID 5388962"),
    ("Quinine", "LOUPRKONTZGTKE-GEQWREAYSA-N",
     "C=C[C@H]1CN2CC[C@H]1C[C@H]2[C@H](O)c1ccnc2ccc(OC)cc12", "structure: PubChem CID 3034034"),
    ("Sucrose", "CZMRCDWAGMRECN-DJHAAKORSA-N",
     "OC[C@H]1O[C@@](CO)(O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@@H](O)[C@@H]1O", "stereo: PubChem CID 5988"),
    ("Testosterone", "MUMGGOZAMZWBJJ-VIUKOLAESA-N",
     "C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@@]43C)[C@@H]1CC[C@@H]2O", "stereo: PubChem CID 6013"),
    ("Estradiol", "VOXZDWNPVJITMN-LUWVYCGLSA-N",
     "C[C@]12CC[C@@H]3c4ccc(O)cc4CC[C@H]3[C@@H]1CC[C@@H]2O", "structure: PubChem CID 5757"),
    ("Chrysene", "TUAHORSUHVUKBD-UHFFFAOYSA-N",
     "c1ccc2c(c1)ccc1c3ccccc3ccc21", "structure: PubChem CID 9171"),
    ("Theobromine", "ZFXYFBGIUFBOJW-UHFFFAOYSA-N",
     "Cn1cnc2c1c(=O)[nH]c(=O)n2C", "structure: PubChem CID 5429"),
    ("G3P (glyceraldehyde-3-phosphate)", "LXJXRIRHZLFYRP-GSVOUGTGSA-N",
     "O=C[C@H](O)COP(=O)(O)O", "stereo: PubChem CID 439168"),
    ("Fructose-1,6-bisphosphate", "XPYBSIWDXQFNMH-PYWDMBMJSA-N",
     "O=C(COP(=O)(O)O)[C@@H](O)[C@H](O)[C@H](O)COP(=O)(O)O", "stereo: PubChem CID 84951"),
    ("2-Methyl-2-pentenal", "SHOJXDKTYKFBRD-UHFFFAOYSA-N",
     "CCC=C(C)C=O", "structure: PubChem CID 12177"),
    ("Fructose-1,6-bisphosphate (ketone form)", "GSXOAOHZAIYLCY-KVQBGUIXSA-N",
     "O=C(COP(=O)(O)O)[C@@H](O)[C@H](O)[C@H](O)COP(=O)(O)O", "structure: PubChem CID 84951"),
    ("Aspartame", "IAOZJIPTCAWIRG-WDEREUQCSA-N",
     "COC(=O)[C@H](Cc1ccccc1)NC(=O)[C@@H](N)CC(=O)O", "stereo: PubChem CID 134601"),
    ("(R)-1-Phenylethanol", "WAPNOHKVXSQRPX-ZETCQYMHSA-N",
     "C[C@@H](O)c1ccccc1", "stereo: PubChem CID 637516"),
    ("(1R,2R)-1,2-Diphenylethane-1,2-diol", "IHPDTPWNFBQHEB-OKILXGFUSA-N",
     "O[C@H](c1ccccc1)[C@H](O)c1ccccc1", "stereo: PubChem CID 853019"),
    ("(2R,3S)-2-Methyl-3-phenyloxirane", "YVCOJTATJWDGEU-APPZFPTMSA-N",
     "C[C@H]1O[C@H]1c1ccccc1", "stereo: PubChem CID 6452030"),
    ("Plastoquinone-9", "WWZGXYLOVKTWBC-UHFFFAOYSA-N",
     "CC(C)=CCC/C(C)=C/CC/C(C)=C/CC/C(C)=C/CC/C(C)=C/CC/C(C)=C/CC/C(C)=C/CC/C(C)=C/CC/C(C)=C/CC1=CC(=O)C(C)=C(C)C1=O", "structure: PubChem CID 5375177"),
    ("Fructose-1,6-bisphosphate", "RNBGYGVWRKECFJ-OMMKOOBNSA-N",
     "O=P(O)(O)OC[C@H]1O[C@](O)(COP(=O)(O)O)[C@@H](O)[C@@H]1O", "stereo: PubChem CID 10267"),
    ("Glucose-6-phosphate", "ZTHXKQRRTHGMEF-IVMDWMLBSA-N",
     "O=P(O)(O)OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O", "structure: PubChem CID 5958"),
    ("Glyceraldehyde-3-phosphate (G3P)", "LXJXRIRHZLFYRP-GSVOUGTGSA-N",
     "O=C[C@H](O)COP(=O)(O)O", "stereo: PubChem CID 439168"),
    ("L-Malate", "BJEPYKJPYRNKOW-UWTATZPHSA-N",
     "O=C(O)C[C@H](O)C(=O)O", "stereo: PubChem CID 222656"),
    ("Fructose-2,6-bisphosphate (F2,6BP)", "ARYCMVNJSWLGNH-BXKVDMCESA-N",
     "O=P(O)(O)OC[C@H]1O[C@@](CO)(OP(=O)(O)O)[C@@H](O)[C@@H]1O", "structure: PubChem CID 105021"),
    ("D-Glucose (open chain)", "GZCGUPFRVQAUEE-KVTDHHQDSA-N",
     "O=C[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO", "stereo: PubChem CID 107526"),
    ("Lactose", "GUBGYTABKSRVRQ-QRZGKKJRSA-N",
     "OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)C(O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@H]1O", "stereo: PubChem CID 440995 (reducing-end anomer unspecified)"),
    ("L-Fucose (6-deoxy-L-galactose)", "SHZGCJCMOBCMKK-DSOBHZJASA-N",
     "C[C@@H]1O[C@@H](O)[C@@H](O)[C@H](O)[C@@H]1O", "stereo: PubChem CID 439554"),
    ("L-Rhamnose (6-deoxy-L-mannose)", "SHZGCJCMOBCMKK-QYESYBIKSA-N",
     "C[C@@H]1O[C@H](O)[C@H](O)[C@H](O)[C@H]1O", "stereo: PubChem CID 439710"),
    ("Xylitol", "HEBKCHPVOIAQTA-QWWZWVQMSA-N",
     "OC[C@@H](O)C(O)[C@@H](O)CO", "stereo: PubChem CID 6912"),
    ("D-Tagatose", "RFSUNEUAIZKAJO-KVTDHHQDSA-N",
     "OC[C@H]1O[C@](O)(CO)[C@@H](O)[C@H]1O", "stereo: PubChem CID 12306013"),
    ("Trehalose (α,α-1,1 glucose dimer)", "HDTRYLNUVZCQOY-BTLHAWITSA-N",
     "OC[C@H]1O[C@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@@H]1O", "stereo: PubChem CID 7427"),
    ("Ceramide (C18)", "VODZWWMEJITOND-ZWVRRZAVSA-N",
     "CCCCCCCCCCCCC/C=C/[C@@H](O)[C@H](CO)NC(=O)CCCCCCCCCCCCCCCCC", "stereo: PubChem CID 5283565"),
    ("Sphingomyelin (C18)", "LKQLRGMMMAHREN-LPIHWRMZSA-N",
     "CCCCCCCCCCCCC/C=C/[C@@H](O)[C@H](COP(=O)([O-])OCC[N+](C)(C)C)NC(=O)CCCCCCCCCCCCCCCCC", "stereo: PubChem CID 6453725"),
    ("Ergosterol", "ODNVTOTZJCJLEO-HKQRUMOLSA-N",
     "CC(C)[C@@H](C)/C=C/[C@@H](C)[C@H]1CC[C@H]2C3=CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C", "structure: PubChem CID 444679"),
    ("Vitamin D3 (cholecalciferol)", "QYSXJUFSXHHAJI-CXXOLTCZSA-N",
     "C=C1CC[C@H](O)C/C1=C/C=C1\\CCC[C@]2(C)[C@@H]([C@H](C)CCCC(C)C)CC[C@@H]12", "structure: PubChem CID 5280795"),
    ("Thromboxane A2 (TXA2)", "NIIUUOXLHUCBIZ-OZBYHRBSSA-N",
     "CCCCC[C@H](O)/C=C/[C@H]1O[C@H]2C[C@H](O2)[C@@H]1C/C=C\\CCCC(=O)O", "structure: PubChem CID 5280497"),
    ("Cholic acid", "BHQCQFFYRZLCQQ-LWJOYLGYSA-N",
     "C[C@H](CCC(=O)O)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C[C@@H]4C[C@H](O)CC[C@]4(C)[C@H]3C[C@H](O)[C@]12C", "stereo: PubChem CID 221493"),
    ("Taurocholic acid", "WBWWGRHZICKQGZ-LQBUBELKSA-N",
     "C[C@H](CCC(=O)NCCS(=O)(=O)O)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C[C@@H]4C[C@H](O)CC[C@]4(C)[C@H]3C[C@H](O)[C@]12C", "stereo: PubChem CID 6675"),
    ("Progesterone", "RJKFOVLPORLFTN-NXMWLWCLSA-N",
     "CC(=O)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C", "stereo: PubChem CID 5994"),
    ("Cortisol", "FPKHHRWXQZCVEB-FPNKAXTOSA-N",
     "C[C@]12CCC(=O)C=C1CC[C@@H]1[C@@H]2[C@@H](O)C[C@@]2(C)[C@H]1CC[C@]2(O)C(=O)CO", "structure: PubChem CID 5754"),
    ("cAMP (3',5'-cyclic AMP)", "IVOMOUWHDPKRLL-ASCDQALMSA-N",
     "Nc1ncnc2c1ncn2[C@@H]1O[C@@H]2COP(=O)(O)O[C@H]2[C@H]1O", "stereo: PubChem CID 6076"),
    ("Pseudouridine (Ψ)", "PNOJJMHMLVSJFV-GVYWOMJSSA-N",
     "O=c1[nH]cc([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=O)[nH]1", "structure: PubChem CID 15047"),
    ("FAD", "YRXQBAXFNJPROD-DZGRYVTPSA-N",
     "Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(C[C@H](O)[C@H](O)[C@H](O)COP(=O)(O)OP(=O)(O)OC[C@H]3O[C@@H](n4cnc5c(N)ncnc54)[C@H](O)[C@@H]3O)c2cc1C", "structure: PubChem CID 643975"),
    ("Coenzyme A (CoA-SH)", "JAGCZEPMUYZZHY-IBOSZNHHSA-N",
     "CC(C)(COP(=O)(O)OP(=O)(O)OC[C@H]1O[C@@H](n2cnc3c(N)ncnc32)[C@H](O)[C@@H]1OP(=O)(O)O)[C@@H](O)C(=O)NCCC(=O)NCCS", "structure: PubChem CID 87642"),
    ("Bisoprolol", "VHCAXJLHGBTWCK-UHFFFAOYSA-N",
     "CC(C)NCC(O)COc1ccc(COCCOC(C)C)cc1", "structure: PubChem CID 2405"),
    ("Enalaprilat", "XQWYWUHFCYGKPB-NRXISQOPSA-N",
     "C[C@H](N[C@@H](CCc1ccccc1)C(=O)O)C(=O)N1CCC[C@H]1C(=O)O", "structure: PubChem CID 5462501"),
    ("Ramipril", "DIEINJZGFIAXBO-AEBFUODCSA-N",
     "CCOC(=O)[C@H](CCc1ccccc1)N[C@@H](C)C(=O)N1[C@H](C(=O)O)C[C@@H]2CCC[C@@H]21", "structure: PubChem CID 5362129"),
    ("Benazepril", "CUJKRAPUGSXKFH-IOVLZCAISA-N",
     "CCOC(=O)[C@H](CCc1ccccc1)N[C@H]1CCc2ccccc2N(CC(=O)O)C1=O", "structure: PubChem CID 5362124"),
    ("Methicillin", "RJQXTJLFIWVMTO-SLEUVZQESA-N",
     "COc1cccc(OC)c1C(=O)N[C@@H]1C(=O)N2[C@@H]1SC(C)(C)[C@@H]2C(=O)O", "stereo: PubChem CID 6087"),
    ("Cloxacillin", "LQOLIRLGBULYKD-GRDNDAEWSA-N",
     "Cc1onc(-c2ccccc2Cl)c1C(=O)N[C@@H]1C(=O)N2[C@@H]1SC(C)(C)[C@@H]2C(=O)O", "stereo: PubChem CID 6098"),
    ("Avanafil", "LJKGMIYXXGMHQZ-MRXNPFEDSA-N",
     "COc1ccc(CNc2nc(N3CCC[C@H]3CO)ncc2C(=O)NCc2ncccn2)cc1Cl", "structure: PubChem CID 9869929"),
    ("Udenafil", "LIKHKJFSKZKKEQ-UHFFFAOYSA-N",
     "CCCOc1ccc(S(=O)(=O)NCCC2CCCN2C)cc1-c1nc2c(CCC)nn(C)c2c(=O)[nH]1", "structure: PubChem CID 135413547"),
    ("Nalidixic acid", "JOFAPHUAPQVEOL-UHFFFAOYSA-N",
     "CCn1cc(C(=O)O)c(=O)c2ccc(C)nc21", "structure: PubChem CID 4421"),
    ("Saxagliptin (Onglyza)", "CMQBANQELDVBQJ-KHZSEGOJSA-N",
     "N#C[C@@H]1C[C@@H]2C[C@@H]2N1C(=O)[C@@H](N)C12CC3CC(CC(O)(C3)C1)C2", "structure: PubChem CID 11243969"),
    ("Alogliptin (Nesina)", "DJVZEAFNJOQQRN-OAHLLOKOSA-N",
     "Cn1c(=O)cc(N2CCC[C@@H](N)C2)n(Cc2ccccc2C#N)c1=O", "structure: PubChem CID 11450633"),
    ("Edoxaban (Lixiana / Savaysa)", "GNHIYJMFFUHMQO-BETUJISGSA-N",
     "CN1CCc2nc(C(=O)N[C@@H]3C[C@@H](C(=O)N(C)C)CC[C@@H]3NC(=O)C(=O)Nc3ccc(Cl)cn3)sc2C1", "structure: PubChem CID 10280735"),
    ("Chlorpheniramine (Chlor-Trimeton)", "CFWZRXFTUKZSLE-UHFFFAOYSA-N",
     "CN(C)CCC(c1ccc(Cl)cc1)c1ccccn1", "structure: PubChem CID 2725"),
    ("Cetirizine (Zyrtec)", "ZKLPARSLTMPFCP-NRFANRHFSA-N",
     "O=C(O)COCCN1CCN(C(c2ccccc2)c2ccc(Cl)cc2)CC1", "structure: PubChem CID 2678"),
    # 2026-11-12, round 2: stereo contradicted the descriptors in the molecule's own name (no PubChem record)
    ("(2R,3R)-2,3-Epoxybutan-1-ol", "QQHZNUPEBVRUFO-IMJSIDKUSA-N",
     "C[C@H]1O[C@@H]1CO", "stereo: descriptors in the name"),
    ("(R)-4-Hydroxy-4-phenylbutan-2-one (Mukaiyama aldol product)", "MUVVFSVVVHYLMQ-JTQLQIEISA-N",
     "CC(=O)C[C@@H](O)c1ccccc1", "stereo: descriptors in the name"),
    ("Evans syn-aldol (N-acyl-(2S,3R)-3-hydroxy-2-methylpentanoyl)", "JULRHESXGMBTKX-XBFCOCLRSA-N",
     "CC[C@@H](O)[C@H](C)C(=O)N1C(=O)OC[C@@H]1Cc1ccccc1", "stereo: descriptors in the name"),
]


def apply_seed_corrections() -> int:
    """Rewrite rows still holding a known-wrong seed structure. Returns the number of rows corrected."""
    fixed = 0
    with session_scope() as s:
        for name, old_key, smiles, source in CORRECTIONS:
            rows = s.query(DBMol).filter(DBMol.name == name, DBMol.inchikey == old_key).all()
            if not rows:
                continue
            m = ChemMol.from_smiles(smiles, generate_3d=False)
            m.ensure_properties()
            for row in rows:
                row.smiles, row.inchi, row.inchikey, row.formula = m.smiles, m.inchi, m.inchikey, m.formula
                row.properties_json = json.dumps(m.properties)
                row.molblock_2d = None
                row.molblock_3d = None
                fixed += 1
                log.info("Corrected seeded structure of %s (%s)", row.name, source)
    return fixed
