"""Phase MB-1.0 (round 215) — 30-microbe catalogue.

Spans 5 microbial kingdoms.  Cross-references resolve to:
- ``cross_reference_cell_component_ids`` →
  ``orgchem.core.cell_components`` ids (e.g.
  "bacterial-plasma-membrane", "peptidoglycan-gram-positive",
  "archaeal-plasma-membrane", "fungal-cell-wall").
- ``cross_reference_pharm_drug_class_ids`` →
  ``pharm.core.drug_classes`` ids (e.g. "beta-lactams",
  "macrolides", "fluoroquinolones", "hiv-pis", "nrtis").
- ``cross_reference_enzyme_ids`` →
  ``biochem.core.enzymes`` ids (e.g. "hiv-protease",
  "lysozyme").
"""
from __future__ import annotations
from typing import List

from microbio.core.microbes import Microbe


# Common bacterial cell-component cross-refs reused below.
_BAC_GRAMPOS = ("bacterial-plasma-membrane",
                "peptidoglycan-gram-positive",
                "70s-ribosome",
                "bacterial-nucleoid")
_BAC_GRAMNEG = ("bacterial-plasma-membrane",
                "peptidoglycan-gram-negative",
                "outer-membrane-gram-negative",
                "70s-ribosome",
                "bacterial-nucleoid")


MICROBES: List[Microbe] = [

    # ============================================================
    # Bacteria — gram-positive (6)
    # ============================================================
    Microbe(
        id="staphylococcus-aureus",
        name="Staphylococcus aureus",
        full_taxonomic_name="Staphylococcus aureus "
                            "(Rosenbach 1884)",
        kingdom="bacteria",
        gram_type="gram-positive",
        baltimore_class="",
        morphology="Spherical cocci in grape-like clusters; "
                   "1.0 µm diameter; non-motile; non-spore-"
                   "forming; catalase + coagulase positive.",
        key_metabolism_or_replication="Facultative anaerobe; "
                                       "ferments glucose, "
                                       "mannitol; produces "
                                       "haemolysins + protein A.",
        pathogenesis_summary="Skin / soft-tissue infection, "
                             "endocarditis, osteomyelitis, "
                             "pneumonia, bacteraemia, toxic "
                             "shock syndrome, food poisoning "
                             "(enterotoxins).  MRSA = "
                             "methicillin-resistant variant "
                             "(mecA gene → PBP2a).",
        antibiotic_susceptibility="MSSA: anti-staph β-lactams "
                                  "(nafcillin, cefazolin); MRSA: "
                                  "vancomycin, daptomycin, "
                                  "linezolid, ceftaroline.",
        genome_size_or_kb="2.8 Mb",
        ictv_or_bergey_reference="Bergey: Firmicutes / "
                                  "Bacilli / Staphylococcaceae.",
        cross_reference_cell_component_ids=(
            *_BAC_GRAMPOS, "bacterial-capsule"),
        cross_reference_pharm_drug_class_ids=(
            "beta-lactams", "macrolides",
            "fluoroquinolones"),
        cross_reference_enzyme_ids=("lysozyme",),
        notes="MRSA is a major nosocomial + community-acquired "
              "pathogen; CA-MRSA carries the SCCmec type IV "
              "cassette + Panton-Valentine leukocidin.",
    ),
    Microbe(
        id="streptococcus-pyogenes",
        name="Streptococcus pyogenes (Group A Strep)",
        full_taxonomic_name="Streptococcus pyogenes "
                            "(Rosenbach 1884)",
        kingdom="bacteria",
        gram_type="gram-positive",
        baltimore_class="",
        morphology="Cocci in chains; β-haemolytic on blood "
                   "agar; bacitracin-sensitive; "
                   "catalase-negative.",
        key_metabolism_or_replication="Facultative anaerobe; "
                                       "Lancefield group A "
                                       "carbohydrate antigen.",
        pathogenesis_summary="Pharyngitis ('strep throat'), "
                             "scarlet fever, impetigo, erysipelas, "
                             "necrotising fasciitis, post-"
                             "streptococcal sequelae (rheumatic "
                             "fever, glomerulonephritis).",
        antibiotic_susceptibility="Universally penicillin-"
                                  "susceptible (no β-lactam "
                                  "resistance documented); "
                                  "macrolides for penicillin-"
                                  "allergic.",
        genome_size_or_kb="1.9 Mb",
        ictv_or_bergey_reference="Bergey: Firmicutes / "
                                  "Bacilli / Streptococcaceae.",
        cross_reference_cell_component_ids=(
            *_BAC_GRAMPOS, "bacterial-capsule"),
        cross_reference_pharm_drug_class_ids=(
            "beta-lactams", "macrolides"),
        cross_reference_enzyme_ids=("lysozyme",),
        notes="M-protein is the dominant virulence factor + "
              "type-specific antigen; > 200 emm types.",
    ),
    Microbe(
        id="streptococcus-pneumoniae",
        name="Streptococcus pneumoniae (pneumococcus)",
        full_taxonomic_name="Streptococcus pneumoniae "
                            "(Klein 1884)",
        kingdom="bacteria",
        gram_type="gram-positive",
        baltimore_class="",
        morphology="Lancet-shaped diplococci; "
                   "α-haemolytic; bile-soluble; optochin-"
                   "sensitive; polysaccharide capsule (95+ "
                   "serotypes).",
        key_metabolism_or_replication="Facultative anaerobe; "
                                       "natural transformation "
                                       "competence.",
        pathogenesis_summary="Community-acquired pneumonia, "
                             "otitis media, sinusitis, "
                             "meningitis, bacteraemia.  "
                             "Capsule is the dominant "
                             "virulence factor.",
        antibiotic_susceptibility="Penicillin (susceptibility "
                                  "varies — check MIC); "
                                  "ceftriaxone for meningitis; "
                                  "macrolides + "
                                  "fluoroquinolones for "
                                  "respiratory infection.",
        genome_size_or_kb="2.2 Mb",
        ictv_or_bergey_reference="Bergey: Firmicutes / "
                                  "Bacilli / Streptococcaceae.",
        cross_reference_cell_component_ids=(
            *_BAC_GRAMPOS, "bacterial-capsule"),
        cross_reference_pharm_drug_class_ids=(
            "beta-lactams", "macrolides",
            "fluoroquinolones"),
        cross_reference_enzyme_ids=(),
        notes="PCV13 + PCV20 + PPSV23 vaccines target capsular "
              "serotypes; conjugate vaccines have dramatically "
              "reduced invasive disease in children.",
    ),
    Microbe(
        id="enterococcus-faecalis",
        name="Enterococcus faecalis",
        full_taxonomic_name="Enterococcus faecalis "
                            "(Andrewes & Horder 1906)",
        kingdom="bacteria",
        gram_type="gram-positive",
        baltimore_class="",
        morphology="Cocci in pairs / short chains; "
                   "γ-haemolytic; bile-esculin-positive; "
                   "PYR-positive; grows in 6.5 % NaCl.",
        key_metabolism_or_replication="Facultative anaerobe; "
                                       "intrinsic resistance "
                                       "to many antibiotics.",
        pathogenesis_summary="Urinary tract infection, "
                             "endocarditis, intra-abdominal "
                             "infection, nosocomial "
                             "bacteraemia.  VRE = vancomycin-"
                             "resistant variant (vanA / vanB).",
        antibiotic_susceptibility="Ampicillin (preferred); "
                                  "synergy with aminoglycoside "
                                  "for endocarditis; VRE → "
                                  "linezolid or daptomycin.",
        genome_size_or_kb="3.2 Mb",
        ictv_or_bergey_reference="Bergey: Firmicutes / "
                                  "Bacilli / Enterococcaceae.",
        cross_reference_cell_component_ids=_BAC_GRAMPOS,
        cross_reference_pharm_drug_class_ids=(
            "beta-lactams", "aminoglycosides"),
        cross_reference_enzyme_ids=(),
        notes="Resistant to cephalosporins (intrinsic) — "
              "important in third-generation-ceph treatment "
              "selection pressure.",
    ),
    Microbe(
        id="clostridium-difficile",
        name="Clostridioides difficile (C. diff)",
        full_taxonomic_name="Clostridioides difficile "
                            "(Hall & O'Toole 1935; "
                            "reclassified 2016)",
        kingdom="bacteria",
        gram_type="gram-positive",
        baltimore_class="",
        morphology="Spore-forming bacillus; obligate "
                   "anaerobe; characteristic 'tennis racquet' "
                   "spore appearance.",
        key_metabolism_or_replication="Strict anaerobe; "
                                       "produces toxins A "
                                       "(TcdA) + B (TcdB) + "
                                       "binary toxin (CDT).",
        pathogenesis_summary="Antibiotic-associated diarrhoea, "
                             "pseudomembranous colitis, toxic "
                             "megacolon.  Hypervirulent NAP1 / "
                             "027 / B1 strain.",
        antibiotic_susceptibility="Treatment: oral "
                                  "vancomycin or fidaxomicin; "
                                  "metronidazole reserved for "
                                  "mild cases; FMT for "
                                  "recurrence.",
        genome_size_or_kb="4.3 Mb",
        ictv_or_bergey_reference="Bergey: Firmicutes / "
                                  "Clostridia / "
                                  "Peptostreptococcaceae.",
        cross_reference_cell_component_ids=_BAC_GRAMPOS,
        cross_reference_pharm_drug_class_ids=("macrolides",),
        cross_reference_enzyme_ids=(),
        notes="Risk factor: prior broad-spectrum antibiotic "
              "use disrupting commensal microbiota — "
              "fluoroquinolones + clindamycin + "
              "cephalosporins highest risk.",
    ),
    Microbe(
        id="listeria-monocytogenes",
        name="Listeria monocytogenes",
        full_taxonomic_name="Listeria monocytogenes "
                            "(Pirie 1940)",
        kingdom="bacteria",
        gram_type="gram-positive",
        baltimore_class="",
        morphology="Short rod; tumbling motility at 22-25 °C "
                   "(actin-based + flagellar); "
                   "β-haemolytic; cold-tolerant.",
        key_metabolism_or_replication="Facultative anaerobe; "
                                       "intracellular pathogen "
                                       "using ActA-driven "
                                       "actin-rocket motility.",
        pathogenesis_summary="Listeriosis: meningoencephalitis "
                             "in elderly + immunocompromised, "
                             "bacteraemia, perinatal infection "
                             "(third trimester); "
                             "gastroenteritis from "
                             "contaminated dairy + deli meats.",
        antibiotic_susceptibility="Ampicillin (often + "
                                  "gentamicin) — note "
                                  "cephalosporins are "
                                  "intrinsically inactive.",
        genome_size_or_kb="2.9 Mb",
        ictv_or_bergey_reference="Bergey: Firmicutes / "
                                  "Bacilli / Listeriaceae.",
        cross_reference_cell_component_ids=(
            *_BAC_GRAMPOS,
            "bacterial-flagellum",
            "actin-microfilament"),
        cross_reference_pharm_drug_class_ids=(
            "beta-lactams", "aminoglycosides"),
        cross_reference_enzyme_ids=(),
        notes="Empirical meningitis regimens always include "
              "ampicillin in patients > 50 y or "
              "immunocompromised — third-gen ceph monotherapy "
              "misses Listeria.",
    ),

    # ============================================================
    # Bacteria — gram-negative (6)
    # ============================================================
    Microbe(
        id="escherichia-coli",
        name="Escherichia coli",
        full_taxonomic_name="Escherichia coli "
                            "(Migula 1895; Castellani & "
                            "Chalmers 1919)",
        kingdom="bacteria",
        gram_type="gram-negative",
        baltimore_class="",
        morphology="Rod-shaped (bacillus); 2-6 µm long; "
                   "motile via peritrichous flagella; "
                   "lactose-fermenter (pink on MacConkey).",
        key_metabolism_or_replication="Facultative anaerobe; "
                                       "MR+/VP-/citrate-/"
                                       "indole+ on standard "
                                       "panel.",
        pathogenesis_summary="UTI (most common cause; UPEC), "
                             "neonatal meningitis (K1), "
                             "bacteraemia, gastroenteritis "
                             "(EHEC O157:H7 → HUS; ETEC → "
                             "traveller's diarrhoea; "
                             "EPEC / EAEC / EIEC).",
        antibiotic_susceptibility="Empiric: nitrofurantoin / "
                                  "fosfomycin / TMP-SMX for "
                                  "UTI; ceftriaxone for "
                                  "bacteraemia; carbapenems "
                                  "for ESBL / AmpC.",
        genome_size_or_kb="4.6 Mb (K-12)",
        ictv_or_bergey_reference="Bergey: Proteobacteria / "
                                  "γ-proteobacteria / "
                                  "Enterobacteriaceae.",
        cross_reference_cell_component_ids=(
            *_BAC_GRAMNEG,
            "bacterial-flagellum",
            "pilus-fimbria",
            "bacterial-plasmid"),
        cross_reference_pharm_drug_class_ids=(
            "beta-lactams", "fluoroquinolones",
            "aminoglycosides"),
        cross_reference_enzyme_ids=(),
        notes="The molecular-biology workhorse; K-12 + B "
              "lab strains used for almost all of recombinant "
              "DNA technology.",
    ),
    Microbe(
        id="klebsiella-pneumoniae",
        name="Klebsiella pneumoniae",
        full_taxonomic_name="Klebsiella pneumoniae "
                            "(Trevisan 1885)",
        kingdom="bacteria",
        gram_type="gram-negative",
        baltimore_class="",
        morphology="Plump rod; non-motile; large "
                   "polysaccharide capsule (mucoid colonies).",
        key_metabolism_or_replication="Facultative anaerobe; "
                                       "lactose fermenter.",
        pathogenesis_summary="Hospital-acquired pneumonia "
                             "('currant jelly' sputum), UTI, "
                             "bacteraemia, liver abscess "
                             "(hypervirulent K1 / K2 strains).  "
                             "Nosocomial outbreaks driven by "
                             "carbapenem-resistant variants "
                             "(KPC / NDM).",
        antibiotic_susceptibility="Wild-type: cephalosporins; "
                                  "ESBL → carbapenem; CRE → "
                                  "ceftazidime-avibactam, "
                                  "meropenem-vaborbactam, or "
                                  "polymyxin combinations.",
        genome_size_or_kb="5.6 Mb",
        ictv_or_bergey_reference="Bergey: Proteobacteria / "
                                  "γ-proteobacteria / "
                                  "Enterobacteriaceae.",
        cross_reference_cell_component_ids=(
            *_BAC_GRAMNEG, "bacterial-capsule",
            "bacterial-plasmid"),
        cross_reference_pharm_drug_class_ids=(
            "beta-lactams", "fluoroquinolones",
            "aminoglycosides"),
        cross_reference_enzyme_ids=(),
        notes="One of the WHO's 'critical' priority pathogens "
              "for new antibiotic R&D — carbapenem resistance "
              "is a global health threat.",
    ),
    Microbe(
        id="pseudomonas-aeruginosa",
        name="Pseudomonas aeruginosa",
        full_taxonomic_name="Pseudomonas aeruginosa "
                            "(Schroeter 1872)",
        kingdom="bacteria",
        gram_type="gram-negative",
        baltimore_class="",
        morphology="Rod; motile (single polar flagellum); "
                   "produces blue-green pigments (pyocyanin, "
                   "pyoverdine); 'grape-like' / sweet smell.",
        key_metabolism_or_replication="Obligate aerobe; "
                                       "non-fermenter; uses "
                                       "many carbon sources "
                                       "via TCA.",
        pathogenesis_summary="Hospital-acquired pneumonia "
                             "(esp. ventilator-associated), "
                             "burn-wound infection, cystic "
                             "fibrosis lung colonisation, "
                             "necrotising otitis externa, "
                             "endocarditis (IVDU), "
                             "ecthyma gangrenosum (neutropenic).",
        antibiotic_susceptibility="Anti-pseudomonal "
                                  "β-lactams (piperacillin-"
                                  "tazobactam, ceftazidime, "
                                  "cefepime, meropenem); "
                                  "anti-pseudomonal "
                                  "fluoroquinolones "
                                  "(ciprofloxacin); "
                                  "aminoglycosides; polymyxins.",
        genome_size_or_kb="6.3 Mb (PAO1)",
        ictv_or_bergey_reference="Bergey: Proteobacteria / "
                                  "γ-proteobacteria / "
                                  "Pseudomonadaceae.",
        cross_reference_cell_component_ids=(
            *_BAC_GRAMNEG,
            "bacterial-flagellum",
            "biofilm-eps"),
        cross_reference_pharm_drug_class_ids=(
            "beta-lactams", "fluoroquinolones",
            "aminoglycosides"),
        cross_reference_enzyme_ids=(),
        notes="Type-III secretion system + quorum-sensing "
              "regulators (LasR / RhlR) drive virulence + "
              "biofilm in CF lung.",
    ),
    Microbe(
        id="neisseria-meningitidis",
        name="Neisseria meningitidis (meningococcus)",
        full_taxonomic_name="Neisseria meningitidis "
                            "(Albrecht & Ghon 1901)",
        kingdom="bacteria",
        gram_type="gram-negative",
        baltimore_class="",
        morphology="Diplococci ('coffee-bean' shape); "
                   "encapsulated; oxidase-positive; ferments "
                   "glucose + maltose.",
        key_metabolism_or_replication="Obligate aerobe; "
                                       "natural transformation "
                                       "competence.",
        pathogenesis_summary="Meningococcaemia (purpura "
                             "fulminans), bacterial meningitis "
                             "(esp. adolescents + young "
                             "adults), Waterhouse-Friderichsen "
                             "syndrome (adrenal infarction).",
        antibiotic_susceptibility="Ceftriaxone (treatment); "
                                  "ciprofloxacin or "
                                  "rifampicin for close-"
                                  "contact prophylaxis.",
        genome_size_or_kb="2.3 Mb",
        ictv_or_bergey_reference="Bergey: Proteobacteria / "
                                  "β-proteobacteria / "
                                  "Neisseriaceae.",
        cross_reference_cell_component_ids=(
            *_BAC_GRAMNEG,
            "bacterial-capsule",
            "pilus-fimbria"),
        cross_reference_pharm_drug_class_ids=(
            "beta-lactams", "fluoroquinolones"),
        cross_reference_enzyme_ids=(),
        notes="Capsular serogroups A, B, C, W, X, Y are "
              "vaccine-preventable; MenACWY conjugate + "
              "MenB protein-based vaccines.",
    ),
    Microbe(
        id="helicobacter-pylori",
        name="Helicobacter pylori",
        full_taxonomic_name="Helicobacter pylori "
                            "(Marshall & Goodwin 1989)",
        kingdom="bacteria",
        gram_type="gram-negative",
        baltimore_class="",
        morphology="Spiral / curved rod; multiple polar "
                   "flagella; urease-positive (potent).",
        key_metabolism_or_replication="Microaerophile; "
                                       "colonises gastric "
                                       "mucus layer; urease "
                                       "neutralises gastric "
                                       "acid for survival.",
        pathogenesis_summary="Chronic gastritis, peptic ulcer "
                             "disease, gastric MALT lymphoma, "
                             "gastric adenocarcinoma (WHO "
                             "Group I carcinogen).",
        antibiotic_susceptibility="Triple therapy: PPI + "
                                  "clarithromycin + amoxicillin "
                                  "(or metronidazole); "
                                  "quadruple therapy with "
                                  "bismuth where resistance is "
                                  "high.",
        genome_size_or_kb="1.7 Mb",
        ictv_or_bergey_reference="Bergey: Proteobacteria / "
                                  "ε-proteobacteria / "
                                  "Helicobacteraceae.",
        cross_reference_cell_component_ids=(
            *_BAC_GRAMNEG, "bacterial-flagellum"),
        cross_reference_pharm_drug_class_ids=(
            "ppis", "beta-lactams", "macrolides"),
        cross_reference_enzyme_ids=(),
        notes="Marshall + Warren's discovery (Nobel 2005) "
              "overturned the dogma that ulcers were caused "
              "by stress + acid alone.",
    ),
    Microbe(
        id="salmonella-typhi",
        name="Salmonella enterica serovar Typhi",
        full_taxonomic_name="Salmonella enterica subsp. "
                            "enterica serovar Typhi",
        kingdom="bacteria",
        gram_type="gram-negative",
        baltimore_class="",
        morphology="Rod; motile (peritrichous flagella); "
                   "non-lactose-fermenter; H₂S-positive on "
                   "TSI agar.",
        key_metabolism_or_replication="Facultative anaerobe; "
                                       "facultative "
                                       "intracellular "
                                       "(macrophages).",
        pathogenesis_summary="Typhoid fever — sustained "
                             "fever, abdominal pain, "
                             "rose spots, hepatosplenomegaly, "
                             "intestinal perforation in week "
                             "3.  Asymptomatic gallbladder "
                             "carriage ('Typhoid Mary').",
        antibiotic_susceptibility="Ceftriaxone or "
                                  "azithromycin first-line; "
                                  "fluoroquinolones now "
                                  "limited by widespread "
                                  "resistance in South Asia.",
        genome_size_or_kb="4.8 Mb",
        ictv_or_bergey_reference="Bergey: Proteobacteria / "
                                  "γ-proteobacteria / "
                                  "Enterobacteriaceae.",
        cross_reference_cell_component_ids=(
            *_BAC_GRAMNEG,
            "bacterial-flagellum",
            "bacterial-capsule"),
        cross_reference_pharm_drug_class_ids=(
            "beta-lactams", "macrolides",
            "fluoroquinolones"),
        cross_reference_enzyme_ids=(),
        notes="Vi-capsular polysaccharide vaccine + new "
              "TyphiBEV conjugate vaccine reduce burden in "
              "endemic regions.",
    ),

    # ============================================================
    # Atypical bacteria (3)
    # ============================================================
    Microbe(
        id="mycoplasma-pneumoniae",
        name="Mycoplasma pneumoniae",
        full_taxonomic_name="Mycoplasma pneumoniae "
                            "(Chanock et al. 1963)",
        kingdom="bacteria",
        gram_type="atypical",
        baltimore_class="",
        morphology="No cell wall (sterol-stabilised "
                   "membrane); pleomorphic; smallest free-"
                   "living organism (~ 200 nm).",
        key_metabolism_or_replication="Facultative anaerobe; "
                                       "limited biosynthetic "
                                       "capacity; requires "
                                       "host sterols.",
        pathogenesis_summary="'Walking pneumonia' (atypical "
                             "community-acquired), bullous "
                             "myringitis, post-infectious "
                             "encephalitis, Stevens-Johnson "
                             "syndrome.",
        antibiotic_susceptibility="**Intrinsically resistant** "
                                  "to β-lactams (no cell wall); "
                                  "macrolides + tetracyclines "
                                  "+ fluoroquinolones.",
        genome_size_or_kb="0.8 Mb",
        ictv_or_bergey_reference="Bergey: Tenericutes / "
                                  "Mollicutes / "
                                  "Mycoplasmataceae.",
        cross_reference_cell_component_ids=("bacterial-plasma-"
                                            "membrane",
                                            "70s-ribosome"),
        cross_reference_pharm_drug_class_ids=(
            "macrolides", "fluoroquinolones"),
        cross_reference_enzyme_ids=(),
        notes="Cold-agglutinin haemagglutination is a "
              "classical (low-sensitivity) bedside clue; "
              "modern diagnosis uses PCR.",
    ),
    Microbe(
        id="chlamydia-trachomatis",
        name="Chlamydia trachomatis",
        full_taxonomic_name="Chlamydia trachomatis "
                            "(Halberstaedter & Prowazek 1907)",
        kingdom="bacteria",
        gram_type="atypical",
        baltimore_class="",
        morphology="Obligate intracellular; biphasic "
                   "developmental cycle (elementary body → "
                   "reticulate body → elementary body); "
                   "modified peptidoglycan-light envelope.",
        key_metabolism_or_replication="Obligate intracellular "
                                       "parasite; energy "
                                       "parasite (relies on "
                                       "host ATP).",
        pathogenesis_summary="Genital tract: most common "
                             "bacterial STI globally; "
                             "asymptomatic in ~ 70 % of "
                             "women; PID, ectopic pregnancy, "
                             "tubal infertility.  Serovars "
                             "A-C: trachoma (leading "
                             "infectious cause of blindness); "
                             "L1-L3: lymphogranuloma "
                             "venereum.",
        antibiotic_susceptibility="Azithromycin single-dose "
                                  "or doxycycline 7-day "
                                  "course; β-lactams + "
                                  "aminoglycosides ineffective.",
        genome_size_or_kb="1.0 Mb",
        ictv_or_bergey_reference="Bergey: Chlamydiae / "
                                  "Chlamydiales / "
                                  "Chlamydiaceae.",
        cross_reference_cell_component_ids=("bacterial-plasma-"
                                            "membrane",
                                            "70s-ribosome"),
        cross_reference_pharm_drug_class_ids=("macrolides",),
        cross_reference_enzyme_ids=(),
        notes="Routine NAAT screening of sexually-active "
              "women < 25 y is the cornerstone of public-"
              "health control.",
    ),
    Microbe(
        id="treponema-pallidum",
        name="Treponema pallidum",
        full_taxonomic_name="Treponema pallidum subsp. "
                            "pallidum (Schaudinn & Hoffmann "
                            "1905)",
        kingdom="bacteria",
        gram_type="atypical",
        baltimore_class="",
        morphology="Slender helical spirochaete (~ 0.2 µm "
                   "wide × 6-15 µm long); endoflagella "
                   "between membrane + outer envelope; "
                   "non-cultivable in vitro.",
        key_metabolism_or_replication="Microaerophile; "
                                       "extremely slow "
                                       "doubling time (~ 33 h "
                                       "in vivo).",
        pathogenesis_summary="Syphilis: primary chancre → "
                             "secondary disseminated rash + "
                             "condyloma lata → latent → "
                             "tertiary (gummas, "
                             "cardiovascular, neurosyphilis).  "
                             "Congenital syphilis on "
                             "vertical transmission.",
        antibiotic_susceptibility="Penicillin G (benzathine "
                                  "for primary / secondary; "
                                  "aqueous IV for "
                                  "neurosyphilis).  No "
                                  "documented penicillin "
                                  "resistance after 80 + years.",
        genome_size_or_kb="1.1 Mb",
        ictv_or_bergey_reference="Bergey: Spirochaetes / "
                                  "Spirochaetia / "
                                  "Treponemataceae.",
        cross_reference_cell_component_ids=("bacterial-plasma-"
                                            "membrane",
                                            "70s-ribosome",
                                            "bacterial-flagellum"),
        cross_reference_pharm_drug_class_ids=("beta-lactams",),
        cross_reference_enzyme_ids=(),
        notes="Diagnosis is serological (RPR / VDRL non-"
              "treponemal + FTA-ABS / TP-PA treponemal) — "
              "the organism cannot be Gram-stained or grown "
              "routinely.",
    ),

    # ============================================================
    # Mycobacteria (2)
    # ============================================================
    Microbe(
        id="mycobacterium-tuberculosis",
        name="Mycobacterium tuberculosis",
        full_taxonomic_name="Mycobacterium tuberculosis "
                            "(Koch 1882)",
        kingdom="bacteria",
        gram_type="acid-fast",
        baltimore_class="",
        morphology="Slender bacillus (~ 0.5 × 3 µm); "
                   "mycolic-acid-rich waxy envelope; "
                   "acid-fast on Ziehl-Neelsen; cords on "
                   "microscopy (cord-factor).",
        key_metabolism_or_replication="Obligate aerobe; "
                                       "doubling time ~ 24 h "
                                       "(cf. ~ 30 min for "
                                       "E. coli); facultative "
                                       "intracellular "
                                       "(macrophages).",
        pathogenesis_summary="Primary pulmonary TB → latent "
                             "TB infection → reactivation "
                             "(weight loss, night sweats, "
                             "haemoptysis, cavitary disease); "
                             "extrapulmonary TB (meningitis, "
                             "Pott's spine, miliary, "
                             "scrofula).",
        antibiotic_susceptibility="Standard 6-month RIPE "
                                  "regimen: rifampicin + "
                                  "isoniazid + pyrazinamide + "
                                  "ethambutol (first 2 mo) → "
                                  "RH (4 mo continuation).  "
                                  "MDR-TB / XDR-TB → "
                                  "bedaquiline-, linezolid-, "
                                  "delamanid-based regimens.",
        genome_size_or_kb="4.4 Mb (H37Rv)",
        ictv_or_bergey_reference="Bergey: Actinobacteria / "
                                  "Corynebacteriales / "
                                  "Mycobacteriaceae.",
        cross_reference_cell_component_ids=(
            "bacterial-plasma-membrane",
            "70s-ribosome", "bacterial-nucleoid"),
        cross_reference_pharm_drug_class_ids=(
            "fluoroquinolones",),
        cross_reference_enzyme_ids=(),
        notes="Causes more deaths globally than any other "
              "single infectious pathogen (~ 1.3 M / yr).  "
              "Bedaquiline (2012) was the first new TB drug "
              "in 40 years.",
    ),
    Microbe(
        id="mycobacterium-leprae",
        name="Mycobacterium leprae",
        full_taxonomic_name="Mycobacterium leprae "
                            "(Hansen 1873)",
        kingdom="bacteria",
        gram_type="acid-fast",
        baltimore_class="",
        morphology="Acid-fast bacillus; non-cultivable in "
                   "vitro (requires armadillo or mouse "
                   "footpad); slowest-doubling known "
                   "bacterium (~ 14 d).",
        key_metabolism_or_replication="Obligate intracellular "
                                       "(macrophages, "
                                       "Schwann cells); has "
                                       "lost ~ 50 % of its "
                                       "genome via reductive "
                                       "evolution.",
        pathogenesis_summary="Leprosy / Hansen's disease: "
                             "tuberculoid (paucibacillary; "
                             "anaesthetic skin patches + "
                             "peripheral nerve damage) vs "
                             "lepromatous (multibacillary; "
                             "diffuse skin nodules, leonine "
                             "facies, glove-and-stocking "
                             "anaesthesia).",
        antibiotic_susceptibility="WHO multi-drug therapy: "
                                  "rifampicin + dapsone "
                                  "(paucibacillary) ± "
                                  "clofazimine "
                                  "(multibacillary), 6-12 "
                                  "months.",
        genome_size_or_kb="3.3 Mb (genome decay; only "
                          "~ 1600 functional genes)",
        ictv_or_bergey_reference="Bergey: Actinobacteria / "
                                  "Corynebacteriales / "
                                  "Mycobacteriaceae.",
        cross_reference_cell_component_ids=(
            "bacterial-plasma-membrane",
            "70s-ribosome", "bacterial-nucleoid"),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_enzyme_ids=(),
        notes="One of the largest documented examples of "
              "reductive genome evolution — over half the "
              "genome is pseudogenes.",
    ),

    # ============================================================
    # Archaea (2)
    # ============================================================
    Microbe(
        id="methanobrevibacter-smithii",
        name="Methanobrevibacter smithii",
        full_taxonomic_name="Methanobrevibacter smithii "
                            "(Balch et al. 1981)",
        kingdom="archaea",
        gram_type="not-applicable",
        baltimore_class="",
        morphology="Short rod / coccobacillus; "
                   "pseudopeptidoglycan-based cell wall.",
        key_metabolism_or_replication="Obligate anaerobic "
                                       "methanogen — uses CO₂ "
                                       "+ H₂ (or formate) → "
                                       "CH₄ + H₂O via the "
                                       "Wolfe cycle (MCR + "
                                       "F420 / CoB / CoM "
                                       "cofactors).",
        pathogenesis_summary="Dominant methanogen in human "
                             "gut microbiome; positive "
                             "association with constipation, "
                             "obesity, IBS-C, anorexia.  Not "
                             "a classical pathogen.",
        antibiotic_susceptibility="Resistant to most "
                                  "antibacterial agents; "
                                  "selective inhibition of "
                                  "MCR by lovastatin "
                                  "metabolites + brominated "
                                  "analogues studied in "
                                  "agriculture (cattle "
                                  "methane mitigation).",
        genome_size_or_kb="1.85 Mb",
        ictv_or_bergey_reference="Bergey: Euryarchaeota / "
                                  "Methanobacteria / "
                                  "Methanobacteriaceae.",
        cross_reference_cell_component_ids=(
            "archaeal-plasma-membrane",
            "pseudopeptidoglycan",
            "archaeal-ribosome",
            "archaeal-nucleoid"),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_enzyme_ids=(),
        notes="Lipid bilayer based on isoprenoid ether "
              "(not ester) lipids — diagnostic of archaeal "
              "membranes.",
    ),
    Microbe(
        id="sulfolobus-acidocaldarius",
        name="Sulfolobus acidocaldarius",
        full_taxonomic_name="Saccharolobus acidocaldarius "
                            "(Brock et al. 1972; "
                            "reclassified 2018)",
        kingdom="archaea",
        gram_type="not-applicable",
        baltimore_class="",
        morphology="Irregular cocci; thermoacidophile "
                   "(optimum 70-80 °C, pH 2-3); "
                   "S-layer cell envelope.",
        key_metabolism_or_replication="Aerobic facultative "
                                       "chemolithoautotroph; "
                                       "oxidises sulfur, "
                                       "iron, organic carbon.",
        pathogenesis_summary="Non-pathogenic.  Inhabits "
                             "geothermal acid-sulfide hot "
                             "springs (Yellowstone, Iceland).  "
                             "Important model organism for "
                             "archaeal chromatin + DNA "
                             "replication research.",
        antibiotic_susceptibility="Not relevant (non-"
                                  "pathogen).",
        genome_size_or_kb="2.2 Mb",
        ictv_or_bergey_reference="Bergey: Crenarchaeota / "
                                  "Thermoprotei / "
                                  "Sulfolobaceae.",
        cross_reference_cell_component_ids=(
            "archaeal-plasma-membrane",
            "s-layer", "archaeal-ribosome"),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_enzyme_ids=(),
        notes="Source of thermostable enzymes used in "
              "biotechnology (alcohol dehydrogenases, DNA "
              "polymerases) + a model organism for studying "
              "archaeal histones + Cren7 chromatin proteins.",
    ),

    # ============================================================
    # Fungi (3)
    # ============================================================
    Microbe(
        id="candida-albicans",
        name="Candida albicans",
        full_taxonomic_name="Candida albicans "
                            "(Robin 1853; Berkhout 1923)",
        kingdom="fungus",
        gram_type="not-applicable",
        baltimore_class="",
        morphology="Polymorphic yeast — budding yeast cells, "
                   "pseudohyphae, true hyphae; germ-tube "
                   "test positive in 3 h serum; chlamydospores "
                   "on cornmeal.",
        key_metabolism_or_replication="Facultative anaerobe; "
                                       "ferments + assimilates "
                                       "many sugars; commensal "
                                       "of GI + vaginal mucosa.",
        pathogenesis_summary="Mucocutaneous candidiasis "
                             "(thrush, vaginitis), invasive "
                             "candidiasis / candidemia "
                             "(immunocompromised, central "
                             "lines, post-surgical), "
                             "oesophageal candidiasis "
                             "(AIDS-defining).",
        antibiotic_susceptibility="Topical: nystatin, "
                                  "clotrimazole.  Systemic: "
                                  "fluconazole (susceptible "
                                  "C. albicans), echinocandins "
                                  "(caspofungin / micafungin / "
                                  "anidulafungin) for invasive "
                                  "or fluconazole-resistant; "
                                  "amphotericin B for "
                                  "severe / refractory.",
        genome_size_or_kb="14.3 Mb",
        ictv_or_bergey_reference="Mycology: Ascomycota / "
                                  "Saccharomycetes / "
                                  "Debaryomycetaceae.",
        cross_reference_cell_component_ids=(
            "fungal-cell-wall",
            "eukaryotic-plasma-membrane",
            "mitochondrion",
            "80s-ribosome"),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_enzyme_ids=(),
        notes="The yeast → hyphae transition is a key "
              "virulence trait + a classical study system "
              "for fungal morphogenesis.",
    ),
    Microbe(
        id="aspergillus-fumigatus",
        name="Aspergillus fumigatus",
        full_taxonomic_name="Aspergillus fumigatus "
                            "(Fresenius 1863)",
        kingdom="fungus",
        gram_type="not-applicable",
        baltimore_class="",
        morphology="Septate filamentous mould; conidiophore "
                   "with phialides + columnar conidial heads; "
                   "blue-green colonies; small (2-3 µm) "
                   "conidia readily inhaled.",
        key_metabolism_or_replication="Obligate aerobe; "
                                       "ubiquitous "
                                       "saprophyte (compost, "
                                       "soil, decaying "
                                       "vegetation).",
        pathogenesis_summary="Invasive pulmonary "
                             "aspergillosis (neutropenic "
                             "haematology patients), allergic "
                             "bronchopulmonary aspergillosis "
                             "(asthmatics + CF), aspergilloma "
                             "(fungus ball in pre-existing "
                             "cavity), chronic pulmonary "
                             "aspergillosis.",
        antibiotic_susceptibility="Voriconazole (first-line "
                                  "for invasive); "
                                  "isavuconazole; liposomal "
                                  "amphotericin B; "
                                  "echinocandins as combination "
                                  "or salvage therapy.",
        genome_size_or_kb="29.4 Mb",
        ictv_or_bergey_reference="Mycology: Ascomycota / "
                                  "Eurotiomycetes / "
                                  "Trichocomaceae.",
        cross_reference_cell_component_ids=(
            "fungal-cell-wall",
            "eukaryotic-plasma-membrane",
            "mitochondrion",
            "80s-ribosome"),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_enzyme_ids=(),
        notes="Azole resistance via TR34 / L98H promoter + "
              "cyp51A mutations is rising globally — agricultural "
              "azole use is a likely driver.",
    ),
    Microbe(
        id="cryptococcus-neoformans",
        name="Cryptococcus neoformans",
        full_taxonomic_name="Cryptococcus neoformans "
                            "(Sanfelice 1894; Vuillemin "
                            "1901)",
        kingdom="fungus",
        gram_type="not-applicable",
        baltimore_class="",
        morphology="Encapsulated yeast (5-10 µm); "
                   "polysaccharide capsule (glucuronoxylo-"
                   "mannan) visible on India-ink prep; "
                   "urease + melanin (laccase) positive.",
        key_metabolism_or_replication="Obligate aerobe; "
                                       "environmental reservoir "
                                       "in pigeon guano + soil.",
        pathogenesis_summary="Cryptococcal meningitis (AIDS-"
                             "defining; ~ 200 000 cases / yr); "
                             "pulmonary cryptococcosis; "
                             "disseminated disease in "
                             "immunocompromised.",
        antibiotic_susceptibility="Induction: amphotericin B "
                                  "+ flucytosine 2 weeks → "
                                  "consolidation: fluconazole "
                                  "8 weeks → maintenance "
                                  "fluconazole until immune "
                                  "recovery.",
        genome_size_or_kb="19 Mb (var. grubii H99)",
        ictv_or_bergey_reference="Mycology: Basidiomycota / "
                                  "Tremellomycetes / "
                                  "Tremellaceae.",
        cross_reference_cell_component_ids=(
            "fungal-cell-wall",
            "eukaryotic-plasma-membrane",
            "mitochondrion",
            "80s-ribosome",
            "bacterial-capsule"),
        # ↑ analogous capsule structure (the bacterial
        #   capsule entry is the closest match in the seeded
        #   cell-component catalogue)
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_enzyme_ids=(),
        notes="Capsule + melanin together drive pathogenicity; "
              "screening + pre-emptive fluconazole for HIV+ "
              "patients with CD4 < 100 dramatically reduces "
              "mortality.",
    ),

    # ============================================================
    # Viruses (6)
    # ============================================================
    Microbe(
        id="sars-cov-2",
        name="SARS-CoV-2",
        full_taxonomic_name="Severe acute respiratory "
                            "syndrome-related coronavirus 2 "
                            "(Coronaviridae)",
        kingdom="virus",
        gram_type="not-applicable",
        baltimore_class="IV",
        morphology="Enveloped, single-stranded positive-"
                   "sense RNA virus; club-shaped spike (S) "
                   "glycoprotein gives the 'corona' "
                   "appearance; ~ 100 nm diameter.",
        key_metabolism_or_replication="+ssRNA → translates "
                                       "directly to viral "
                                       "polyproteins → cleaved "
                                       "by Mpro / PLpro → RdRp "
                                       "produces -ssRNA "
                                       "template + sub-"
                                       "genomic mRNAs.  ACE2 "
                                       "+ TMPRSS2 host entry.",
        pathogenesis_summary="COVID-19: asymptomatic to "
                             "severe pneumonia; ARDS, "
                             "thromboembolic disease, "
                             "myocarditis, multisystem "
                             "inflammatory syndrome (MIS-C); "
                             "post-acute sequelae ('long "
                             "COVID').",
        antibiotic_susceptibility="Antivirals: nirmatrelvir-"
                                  "ritonavir (Mpro inhibitor + "
                                  "CYP3A4 booster), remdesivir "
                                  "(RdRp), molnupiravir "
                                  "(error catastrophe).  "
                                  "Vaccines: mRNA, viral "
                                  "vector, protein subunit, "
                                  "inactivated.",
        genome_size_or_kb="29.9 kb (+ssRNA)",
        ictv_or_bergey_reference="ICTV: Riboviria / Nidovirales / "
                                  "Coronaviridae / "
                                  "Betacoronavirus.",
        cross_reference_cell_component_ids=(),
        cross_reference_pharm_drug_class_ids=("hiv-pis",),
        # ↑ nirmatrelvir is structurally analogous to HIV PIs;
        #   ritonavir is from the HIV-PI class
        cross_reference_enzyme_ids=("cyp3a4",),
        # ↑ ritonavir boosts via CYP3A4 inhibition
        notes="2019-2020 outbreak in Wuhan led to the first "
              "true global pandemic since 1918 influenza.  "
              "mRNA vaccine technology (Pfizer-BioNTech / "
              "Moderna) reached emergency-use authorisation "
              "in < 1 year.",
    ),
    Microbe(
        id="hiv-1",
        name="HIV-1 (Human Immunodeficiency Virus 1)",
        full_taxonomic_name="Human immunodeficiency virus 1 "
                            "(Retroviridae / Lentivirus)",
        kingdom="virus",
        gram_type="not-applicable",
        baltimore_class="VI",
        morphology="Enveloped retrovirus; cone-shaped capsid "
                   "(HIV is one of the few viruses with a "
                   "non-icosahedral capsid); two copies of "
                   "ssRNA genome packaged with reverse "
                   "transcriptase + integrase.",
        key_metabolism_or_replication="+ssRNA → reverse-"
                                       "transcribed to "
                                       "dsDNA → integrated "
                                       "into host genome "
                                       "(provirus) by viral "
                                       "integrase → "
                                       "transcribed by host "
                                       "RNA Pol II → "
                                       "translated → "
                                       "polyproteins cleaved "
                                       "by HIV protease → "
                                       "mature virion "
                                       "assembly + budding.",
        pathogenesis_summary="Acute retroviral syndrome → "
                             "asymptomatic chronic phase "
                             "(years) → AIDS (CD4 < 200): "
                             "opportunistic infections "
                             "(PCP, TB, cryptococcal "
                             "meningitis), Kaposi's sarcoma, "
                             "wasting syndrome.",
        antibiotic_susceptibility="Combination ART: NRTI "
                                  "backbone (TDF/TAF + FTC or "
                                  "ABC + 3TC) + INSTI "
                                  "(dolutegravir / "
                                  "bictegravir) or PI "
                                  "(darunavir / ritonavir).  "
                                  "PrEP: TDF/FTC or "
                                  "cabotegravir LA.",
        genome_size_or_kb="9.7 kb (ssRNA-RT)",
        ictv_or_bergey_reference="ICTV: Riboviria / Ortervirales / "
                                  "Retroviridae / Lentivirus.",
        cross_reference_cell_component_ids=(),
        cross_reference_pharm_drug_class_ids=(
            "hiv-pis", "nrtis"),
        cross_reference_enzyme_ids=("hiv-protease",),
        notes="CD4 + CCR5 (or CXCR4) host entry receptors.  "
              "ΔCCR5-32 homozygotes are largely resistant to "
              "infection — the basis of the 'Berlin' + "
              "'London' patient HSCT cures.",
    ),
    Microbe(
        id="influenza-a",
        name="Influenza A virus",
        full_taxonomic_name="Influenza A virus "
                            "(Orthomyxoviridae / "
                            "Alphainfluenzavirus)",
        kingdom="virus",
        gram_type="not-applicable",
        baltimore_class="V",
        morphology="Enveloped pleomorphic; segmented "
                   "negative-sense ssRNA genome (8 "
                   "segments); spike glycoproteins HA + NA "
                   "(HxNy subtype designation).",
        key_metabolism_or_replication="-ssRNA → host-nucleus "
                                       "import → viral RdRp "
                                       "transcribes mRNAs + "
                                       "replicates genome → "
                                       "segments package → "
                                       "bud at plasma "
                                       "membrane.",
        pathogenesis_summary="Seasonal influenza "
                             "(fever, myalgia, cough, "
                             "respiratory distress), "
                             "secondary bacterial "
                             "pneumonia (S. pneumoniae, "
                             "S. aureus), pandemic "
                             "influenza (1918 H1N1 'Spanish "
                             "flu', 1957 H2N2, 1968 H3N2, "
                             "2009 pdm09 H1N1).",
        antibiotic_susceptibility="Neuraminidase inhibitors "
                                  "(oseltamivir, zanamivir, "
                                  "peramivir).  Endonuclease "
                                  "inhibitor: baloxavir "
                                  "marboxil.  Annual "
                                  "vaccines reformulated "
                                  "based on circulating "
                                  "strains.",
        genome_size_or_kb="13.6 kb total across 8 segments",
        ictv_or_bergey_reference="ICTV: Riboviria / Articulavirales "
                                  "/ Orthomyxoviridae.",
        cross_reference_cell_component_ids=(),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_enzyme_ids=(),
        notes="Antigenic shift (segment reassortment) drives "
              "pandemics; antigenic drift (point mutations) "
              "drives seasonal epidemics.",
    ),
    Microbe(
        id="hepatitis-b",
        name="Hepatitis B virus",
        full_taxonomic_name="Hepatitis B virus "
                            "(Hepadnaviridae / "
                            "Orthohepadnavirus)",
        kingdom="virus",
        gram_type="not-applicable",
        baltimore_class="VII",
        morphology="Enveloped; partially double-stranded "
                   "circular DNA genome (~ 3.2 kb); "
                   "Dane particle (42 nm) + filamentous + "
                   "spherical sub-viral particles "
                   "(non-infectious, HBsAg only).",
        key_metabolism_or_replication="dsDNA → covalently "
                                       "closed circular DNA "
                                       "(cccDNA) in nucleus → "
                                       "pregenomic RNA → "
                                       "reverse-transcribed "
                                       "by viral polymerase "
                                       "back to DNA → "
                                       "encapsidation.",
        pathogenesis_summary="Acute hepatitis (often "
                             "subclinical) → chronic carrier "
                             "(↑ in perinatal infection) → "
                             "cirrhosis → hepatocellular "
                             "carcinoma.  HDV co- or super-"
                             "infection accelerates disease.",
        antibiotic_susceptibility="NRTIs with anti-HBV "
                                  "activity: tenofovir "
                                  "(TDF/TAF), entecavir.  "
                                  "Pegylated interferon-α "
                                  "in selected patients.  "
                                  "Vaccine: HBsAg subunit "
                                  "(universal infant + "
                                  "adolescent immunisation).",
        genome_size_or_kb="3.2 kb (partial dsDNA-RT)",
        ictv_or_bergey_reference="ICTV: Riboviria / Blubervirales / "
                                  "Hepadnaviridae.",
        cross_reference_cell_component_ids=(),
        cross_reference_pharm_drug_class_ids=("nrtis",),
        cross_reference_enzyme_ids=(),
        notes="cccDNA persistence in hepatocyte nuclei is "
              "the reason current NRTIs suppress but rarely "
              "cure chronic HBV; functional cure remains an "
              "active drug-development goal.",
    ),
    Microbe(
        id="herpes-simplex-1",
        name="Herpes simplex virus 1 (HSV-1)",
        full_taxonomic_name="Human alphaherpesvirus 1 "
                            "(Herpesviridae / "
                            "Simplexvirus)",
        kingdom="virus",
        gram_type="not-applicable",
        baltimore_class="I",
        morphology="Enveloped icosahedral capsid; large "
                   "linear dsDNA genome; tegument layer "
                   "between capsid + envelope.",
        key_metabolism_or_replication="dsDNA → nuclear "
                                       "replication via viral "
                                       "DNA polymerase + "
                                       "thymidine kinase → "
                                       "lifelong latency in "
                                       "trigeminal sensory "
                                       "ganglia (LAT "
                                       "transcripts).",
        pathogenesis_summary="Orolabial herpes ('cold sores'), "
                             "herpetic gingivostomatitis, "
                             "herpetic whitlow, herpetic "
                             "keratitis (a leading cause of "
                             "infectious blindness), "
                             "encephalitis (temporal-lobe "
                             "predilection).",
        antibiotic_susceptibility="Aciclovir, valaciclovir, "
                                  "famciclovir — all activated "
                                  "by viral thymidine kinase + "
                                  "selective for HSV.  "
                                  "Foscarnet for aciclovir-"
                                  "resistant disease.",
        genome_size_or_kb="152 kb (linear dsDNA)",
        ictv_or_bergey_reference="ICTV: Duplodnaviria / "
                                  "Herpesvirales / "
                                  "Herpesviridae.",
        cross_reference_cell_component_ids=(),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_enzyme_ids=(),
        notes="Reactivation triggered by stress / UV / "
              "fever / immunosuppression; serological "
              "prevalence > 60 % globally in adults.",
    ),
    Microbe(
        id="norovirus",
        name="Norovirus (genogroups GI + GII)",
        full_taxonomic_name="Norwalk virus / Norovirus "
                            "(Caliciviridae / Norovirus)",
        kingdom="virus",
        gram_type="not-applicable",
        baltimore_class="IV",
        morphology="Non-enveloped icosahedral; 27-32 nm "
                   "diameter; +ssRNA genome (~ 7.5 kb); "
                   "VP1 capsid forms 90 dimers.",
        key_metabolism_or_replication="+ssRNA directly "
                                       "translated → "
                                       "polyprotein cleaved → "
                                       "RdRp replicates "
                                       "genome via -ssRNA "
                                       "intermediate.",
        pathogenesis_summary="Acute gastroenteritis (the "
                             "single most common cause "
                             "globally); explosive vomiting "
                             "+ diarrhoea; cruise-ship + "
                             "care-home + school outbreaks; "
                             "highly contagious "
                             "(< 100 viral particles "
                             "infectious).",
        antibiotic_susceptibility="No specific antiviral "
                                  "approved; supportive care "
                                  "(rehydration); strict "
                                  "infection-control "
                                  "(bleach decontamination — "
                                  "alcohol gels are "
                                  "ineffective).",
        genome_size_or_kb="7.5 kb (+ssRNA)",
        ictv_or_bergey_reference="ICTV: Riboviria / "
                                  "Picornavirales (close) / "
                                  "Caliciviridae.",
        cross_reference_cell_component_ids=(),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_enzyme_ids=(),
        notes="Histo-blood group antigens are the cellular "
              "receptors — secretor-negative individuals "
              "(non-secretor FUT2 genotype) are largely "
              "resistant to GII.4 strains.",
    ),

    # ============================================================
    # Protists (2)
    # ============================================================
    Microbe(
        id="plasmodium-falciparum",
        name="Plasmodium falciparum",
        full_taxonomic_name="Plasmodium falciparum "
                            "(Welch 1897)",
        kingdom="protist",
        gram_type="not-applicable",
        baltimore_class="",
        morphology="Apicomplexan; multiple life-cycle "
                   "stages — sporozoite, liver schizont, "
                   "erythrocytic ring / trophozoite / "
                   "schizont / gametocyte; 'banana-shaped' "
                   "gametocytes diagnostic.",
        key_metabolism_or_replication="Apicomplexan asexual "
                                       "replication in human "
                                       "hepatocytes + "
                                       "erythrocytes; sexual "
                                       "stages in Anopheles "
                                       "mosquito mid-gut.",
        pathogenesis_summary="Severe malaria: cerebral "
                             "malaria, severe anaemia, "
                             "respiratory distress, "
                             "hypoglycaemia, blackwater "
                             "fever.  ~ 600 000 deaths / yr "
                             "(mostly African children "
                             "< 5 y).",
        antibiotic_susceptibility="Artemisinin-based "
                                  "combination therapy (ACT) "
                                  "first-line: artemether-"
                                  "lumefantrine, "
                                  "artesunate-amodiaquine, "
                                  "etc.  IV artesunate for "
                                  "severe.  Atovaquone-"
                                  "proguanil for prophylaxis.  "
                                  "Chloroquine resistance "
                                  "now widespread.",
        genome_size_or_kb="23 Mb",
        ictv_or_bergey_reference="Apicomplexa / Aconoidasida "
                                  "/ Plasmodiidae.",
        cross_reference_cell_component_ids=(
            "eukaryotic-plasma-membrane",
            "mitochondrion",
            "80s-ribosome"),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_enzyme_ids=(),
        notes="Sickle-cell trait + thalassaemia + G6PD "
              "deficiency + Duffy-null all confer partial "
              "protection — driving the evolutionary "
              "geography of these haematological traits.",
    ),
    Microbe(
        id="toxoplasma-gondii",
        name="Toxoplasma gondii",
        full_taxonomic_name="Toxoplasma gondii "
                            "(Nicolle & Manceaux 1908)",
        kingdom="protist",
        gram_type="not-applicable",
        baltimore_class="",
        morphology="Apicomplexan; tachyzoite (rapid "
                   "replication, acute infection), "
                   "bradyzoite (latent tissue cysts), "
                   "oocyst (cat-shed environmental form).",
        key_metabolism_or_replication="Definitive host = "
                                       "felids (sexual cycle "
                                       "in cat intestine); "
                                       "intermediate hosts = "
                                       "warm-blooded animals "
                                       "(asexual cysts in "
                                       "muscle + brain).",
        pathogenesis_summary="Mostly asymptomatic in "
                             "immunocompetent (~ 30 % global "
                             "seroprevalence).  Reactivated "
                             "encephalitis in advanced HIV; "
                             "congenital toxoplasmosis "
                             "(chorioretinitis, "
                             "intracranial calcifications, "
                             "hydrocephalus); "
                             "ophthalmic toxoplasmosis.",
        antibiotic_susceptibility="Pyrimethamine + "
                                  "sulfadiazine + folinic "
                                  "acid (standard); "
                                  "trimethoprim-"
                                  "sulfamethoxazole "
                                  "(prophylaxis in HIV "
                                  "CD4 < 100); "
                                  "spiramycin in pregnancy.",
        genome_size_or_kb="65 Mb",
        ictv_or_bergey_reference="Apicomplexa / Conoidasida "
                                  "/ Sarcocystidae.",
        cross_reference_cell_component_ids=(
            "eukaryotic-plasma-membrane",
            "mitochondrion",
            "80s-ribosome"),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_enzyme_ids=(),
        notes="Behavioural manipulation of rodent hosts "
              "(loss of fear of cats) is one of the most-"
              "studied parasite-mediated host manipulations.",
    ),
]
