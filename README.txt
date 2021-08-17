* ABOUT *

Web front-end for checking IntAct database for similar entries using UniRef sequences

Source code can be obtained here:

https://github.com/jrmango/binding-choice

* REQUIREMENTS *

HTML5 supporting browser, internet connection

Recommended memory/cpu is 1gb, 2ghz per simultaneous user.

* DETAILED USAGE *

1. Enter a UniProt accession and click Submit, leaving the second field blank. The program will scrape the UniRef and BindingDB databases.

2. The table will populate with results formatted from both. Select a ligand monomer ID from the Binding Database to use as a reference.

3. Copy the SMILES formatted entry of the monomer of interest to the second field while retaining the UniProt identifier in field 1, and click Submit.

4. The tool will search the Binding database for UniProt IDs matching this target and flag any present in the Uniref entry for the provided accession

5. After database access, The rightmost column will populate with green markers indicating that a given similar Uniref protein has a documented binding affinity

* REFERENCES *

This script depends upon the BindingDB and UniRef90 databases

Suzek BE, Huang H, McGarvey P, Mazumder R, Wu CH. UniRef: Comprehensive and Non-Redundant UniProt Reference Clusters. Bioinformatics 23:1282-1288 (2007)

Burroughs AM, Ando Y, de Hoon MJ, Tomaru Y, Nishibu T, Ukekawa R et al. (2010) A comprehensive survey of 3' animal miRNA modification events and a possible role for 3' adenylation in modulating miRNA targeting effectiveness. Genome Res 20 (10):1398-410. DOI: 10.1101/gr.106054.110 PMID: 20719920