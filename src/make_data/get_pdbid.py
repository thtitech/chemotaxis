import csv

inputfile = "/gs/hs0/tga-megadock/hayashi/data/Chemotaxis/pathway_info.csv"
outfile = "/gs/hs0/tga-megadock/hayashi/data/Chemotaxis/pdb_list.csv"

s = set()

with open(inputfile, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if (row[0] == "pathway") or (row[0] == "uniprot"):
            continue
        if row[0] == "pdb":
            for pdbid in row[1:]:
                s.add(pdbid)

with open(outfile, "w") as f:
    for pdbid in s:
        f.write(pdbid + "\n")
    

