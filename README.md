# Aggrescan3D (A3D) 2.0: tructure-based prediction tool for protein aggregation properties

<p align="center">
    <img src="https://media.springernature.com/lw685/springer-static/image/chp%3A10.1007%2F978-1-4939-7756-7_21/MediaObjects/421474_1_En_21_Fig4_HTML.gif" alt="Aggrescan figure" width="800px"/>
</p>

<p align="center">
<img src="https://user-images.githubusercontent.com/31255434/182289305-4cc620e3-86ae-480f-9b61-6ca83283caa5.jpg" alt="Latch Verified" width="100">
</p>
<p align="center">
<strong>
Latch Verified
</strong>
</p>

## Aggrescan3D

Protein aggregation is a critical issue in various human disorders and poses a significant challenge in the production of therapeutic proteins. Aggrescan3D (A3D) 2.0 addresses this need by providing an in-silico method to predict the aggregation propensities of proteins in their folded states, assisting in the engineering of soluble protein-based drugs and the study of disease-associated protein variants.

Aggrescan3D uses protein 3D-structures in PDB format as input, derived from X-ray diffraction, solution NMR, or modeling approaches. The structures are energetically minimized before analysis. The method projects an experimentally derived intrinsic aggregation propensity scale for natural amino acids onto the protein 3D structure.

A3D calculates the aggregation propensity for spherical regions centered on every residue Cα carbon, providing a unique structurally corrected aggregation value (A3D score) for each amino acid in the structure. It focuses on protein surfaces, discarding the negligible contribution of highly hydrophobic residues hidden in the core of folded proteins.

This approach allows A3D to identify aggregation patches that are typically not contiguous in sequence, outperforming linear sequence or composition-based algorithms.

### Key Features

- Structure-based prediction of protein aggregation properties
- Extension to larger and multimeric proteins
- Simultaneous prediction of changes in protein solubility and stability upon mutation
- Rapid screening for functional protein variants with improved solubility
- Virtual mutation capabilities for designing variants with increased solubility

### Applications

A3D can be used to predict aggregation propensities in folded proteins, design protein variants with increased solubility, study disease-associated protein variants, and optimize protein-based therapeutics.

## Credits

Aleksander Kuriata, Valentin Iglesias, Jordi Pujols, Mateusz Kurcinski, Sebastian Kmiecik, Salvador Ventura,
Aggrescan3D (A3D) 2.0: prediction and engineering of protein solubility,
Nucleic Acids Research, Volume 47, Issue W1, 02 July 2019, Pages W300–W307,
https://doi.org/10.1093/nar/gkz321
