# Animal evolution + phylogenetics

Reconstructing the tree of animals — and the major
events that produced today's diversity — is a
multi-decade collaborative project involving
fossils, comparative anatomy, embryology, and (most
transformatively) molecular phylogenomics.

## The animal tree

Modern animal phylogeny in broad strokes:

```
Choanoflagellates (sister)
 └── Metazoa
      ├── Porifera (sponges)
      ├── Ctenophora (comb jellies; controversial position)
      ├── Placozoa
      └── Eumetazoa
           ├── Cnidaria (radial)
           └── Bilateria
                ├── Xenacoelomorpha
                ├── Protostomia
                │    ├── Lophotrochozoa
                │    │    ├── Mollusca
                │    │    ├── Annelida
                │    │    ├── Platyhelminthes
                │    │    ├── Rotifera
                │    │    └── Brachiopoda + others
                │    └── Ecdysozoa
                │         ├── Arthropoda
                │         ├── Onychophora
                │         ├── Tardigrada
                │         ├── Nematoda
                │         └── Priapulida + others
                └── Deuterostomia
                     ├── Echinodermata
                     ├── Hemichordata
                     └── Chordata
                          ├── Cephalochordata (lancelets)
                          ├── Urochordata (tunicates)
                          └── Vertebrata
                               ├── Cyclostomes (lamprey, hagfish)
                               └── Gnathostomes (jawed)
                                    ├── Chondrichthyes
                                    └── Osteichthyes
                                         ├── Actinopterygii (ray-fins)
                                         └── Sarcopterygii (lobe-fins)
                                              └── Tetrapoda
                                                   ├── Amphibia
                                                   └── Amniota
                                                        ├── Sauropsida
                                                        │    └── Aves (within dinosaurs)
                                                        └── Synapsida
                                                             └── Mammalia
```

## Some unresolved questions

- **Sponges vs ctenophores** — are sponges or
  ctenophores the sister to all other animals?
  Both arrangements supported by different
  datasets / methods; the field is unsettled.
- **Xenacoelomorph position** — sister to all other
  bilaterians OR derived deuterostomes (chronic
  long-branch-attraction issues).
- **Ecdysozoa monophyly** — strongly supported but
  some morphological dissent.
- **Within Lophotrochozoa** — many short branches +
  difficult relationships.
- **Within mammals** — afrotheria + xenarthra base
  positions debated.

## The Cambrian explosion

~ 540-520 Ma — most animal phyla appear in the
fossil record within ~ 20 Myr.

Likely contributors:
- **Genetic toolkit** in place (Hox + signalling
  pathways) before the explosion.
- **Oxygen rise** to enable larger body sizes +
  active metabolism.
- **Predation arms race** — burrowing, armour,
  shells, eyes.
- **Continental + ocean configurations** providing
  new shelf habitats.
- **Sediment + behavioural innovations** — bioturbation
  feedbacks.

Key fossil sites:
- **Chengjiang biota** (China, ~ 518 Ma) — exceptional
  soft-tissue preservation.
- **Burgess Shale** (Canada, ~ 508 Ma) — Walcott's
  classic site; *Anomalocaris*, *Hallucigenia*,
  *Wiwaxia*, *Marrella*, *Opabinia*.
- **Sirius Passet** (Greenland) + **Emu Bay Shale**
  (Australia) — additional Cambrian Lagerstätten.
- **Ediacaran biota** (~ 575-540 Ma) — soft-bodied,
  enigmatic; some are early animals + others
  stem-group experiments.

## Major mass extinctions

Five "big five" mass extinctions in the Phanerozoic:

| Event | Age | Cause | Casualties |
|-------|-----|-------|------------|
| End-Ordovician | 444 Ma | Glaciation | ~ 86 % marine species |
| Late Devonian | 359 Ma | Multiple — anoxia? | ~ 75 % |
| End-Permian "Great Dying" | 252 Ma | Siberian Traps volcanism + ocean anoxia | > 90 % marine + ~ 70 % terrestrial |
| End-Triassic | 201 Ma | CAMP volcanism | ~ 80 % |
| End-Cretaceous (K-Pg) | 66 Ma | Chicxulub asteroid + Deccan Traps | ~ 75 % including non-avian dinosaurs |

A "sixth extinction" — the Anthropocene defaunation
— is in progress (covered in BT-3.0 + AB-3.0
conservation lessons).

## Evo-devo + Hox

The discovery of **Hox genes** (homeobox-containing
TFs) in fly + their conservation in vertebrates
revealed the deep genetic toolkit of animal
body-plan diversity.

Key insights:
- Almost every developmental signalling pathway
  pre-dates the Cambrian (Wnt, Hedgehog, Notch,
  TGF-β, FGF, EGF, JAK-STAT, JNK, Hippo, BMP,
  ALL ancient).
- Body-plan diversity arises from REGULATORY
  changes — cis-element evolution, gene-network
  rewiring, gene-duplication / loss — not from
  novel genes.
- **Deep homology** — different organs / structures
  use shared regulatory programs (limbs +
  fins, eyes across phyla, hearts).
- **Convergent evolution** of similar morphologies
  uses different cis-regulatory routes (eye
  evolution, ear evolution, wings independently
  in 4 vertebrate lineages).

## Whole-genome duplications

Two rounds (2R) of whole-genome duplication
(WGD) in the vertebrate lineage:
- **1R** — at the base of vertebrates (~ 500 Ma).
- **2R** — at the base of jawed vertebrates
  (~ 450 Ma).

Result: 4 paralog clusters of Hox + many other
key developmental genes → genetic raw material for
elaborated body-plan complexity.

Additional **3R** (teleost-specific) WGD ~ 320 Ma
explains teleost gene-family expansions.

## Phylogenomic methods

The current toolkit:
- **Multi-gene concatenation** + **coalescent**
  approaches (RAxML, IQ-TREE, ASTRAL).
- **Whole-genome data** rather than single genes
  + carefully curated orthologue selection.
- **Site- + lineage-specific** rate variation
  modelled.
- **Long-branch attraction** mitigation (heterogeneous
  models, breaking long branches).
- **Species-tree** inference accounting for gene-
  tree discordance from incomplete lineage sorting
  + horizontal-transfer events (rare in animals
  but documented).

Major published phylogenomic projects:
- **Genome 10K** (vertebrates).
- **i5K** (insects).
- **Open Tree of Life** synthesis.
- **Vertebrate Genomes Project** + similar.
- **Earth BioGenome Project** — sequence every
  named eukaryote (~ 1.8 M species; > $1 B
  initiative).

## Molecular clocks

Calibrating divergence times against fossil ages.

Approaches:
- **Strict clock** — assumes constant rate.
- **Relaxed clock** — rates vary across branches +
  through time.
- **Bayesian methods** — BEAST, MrBayes, MCMCtree.
- **Calibration uncertainty** — explicit fossil
  constraint distributions.

Limitations:
- Rate heterogeneity across genes + lineages.
- Fossil calibrations are MINIMUM dates — actual
  divergence may be earlier.
- Saturation at deep nodes obscures signal.
- Dating major animal radiations remains contentious
  (Cambrian explosion vs molecular clock estimates
  often disagree by 100+ Myr).

## Convergent evolution highlights

- **Eye** evolved > 40 times across animals (camera
  eyes in vertebrates + cephalopods + box jellyfish
  + spiders).
- **Wings / flight** in 4 vertebrate lineages
  (insects, pterosaurs, birds, bats) + winged
  insect groups multiple times independently within
  arthropods.
- **Echolocation** in bats + dolphins + some shrews
  + oilbirds.
- **Endothermy** in birds + mammals + opah + some
  sharks + tunas (regional).
- **Live birth (viviparity)** evolved > 150 times
  across vertebrates.
- **Loss of limbs** in snakes + caecilians + many
  lizards + cetaceans (hindlimbs).

Convergence reveals the limits + repeatability of
evolutionary "solutions" + the role of physical /
ecological constraints.

## Recent + ongoing evolution

Animals are not "finished evolving":
- **Industrial melanism** in peppered moth.
- **Bill-size shifts** in Galapagos finches.
- **Rapid phenology shifts** in many species
  (climate change driver).
- **Antibiotic + insecticide resistance** evolution
  in pests + pathogens.
- **Domestication** of dogs, cats, cattle, pigs, +
  recent (silver fox) experiments.
- **Anthropogenic selection on body size** —
  fishery selection for smaller sizes; trophy
  hunting selecting against large antlers / horns.
- **Urban evolution** — songbird pitch shifts,
  thicker peregrine claws, grass-tolerant
  earthworms.

## Modern paleogenomics

Ancient DNA recovery + sequencing has transformed
recent evolutionary biology:
- **Mammoth, mastodon, cave bear genomes** —
  Pleistocene megafauna.
- **Neanderthal + Denisovan genomes** (Pääbo Nobel
  2022) — interbreeding with anatomically modern
  humans.
- **Pleistocene horse, dog, cat, pig genomes** —
  domestication histories.
- **Coelacanth + lungfish + lamprey** — vertebrate
  evolution insights.
- **Dating by ancient DNA** — refining migration +
  diversification timelines.

A future **Genetics + Molecular Biology Studio**
sibling will deepen technique-level coverage of
ancient-DNA + phylogenomic methods.

## Try it in the app

- **Window → Animal Biology Studio → Animal taxa** —
  30 species across all 9 major phyla.
- **Window → Animal Biology Studio → Organ
  systems** — comparative-anatomy entries
  illustrating body-plan diversity + evolution.

Next: **Behaviour + ethology**.
