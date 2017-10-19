import csv
import glob
import os

PROTEIN_DIR = "/gs/hs0/tga-megadock/hayashi/data/structure/train_structure/BM58C_receptor/"
TARGET = "/gs/hs0/tga-megadock/hayashi/data/result/BM58C/"
DOCKING_OUTFILE = "/gs/hs0/tga-megadock/hayashi/data/result/BM58.csv"

# Output: docking
# receptor name, ligand name, receptor size, ligand size, docking score...

def get_size(filename):
    size = 0
    with open(filename, "r") as f:
        for line in f:
            size = line[23:26].strip()
    return size

def get_score(filename):
    score_list = []
    with open(filename, "r") as f:
        for line in f:
            array = line.split("\t")
            if len(array) != 7:
                continue
            score = str(float(array[6].strip()))
            score_list.append(score)
    return score_list

def main():
    # get size of protein
    print("Start get protein size")
    pdb_list = glob.glob(PROTEIN_DIR + "*.pdb")
    protein_size_dct = {}
    for pdb_file in pdb_list:
        protein_name = os.path.basename(pdb_file).split(".")[0]
        protein_size = get_size(pdb_file)
        protein_size_dct[protein_name] = protein_size

    print("Start out file parse")
    # parse out file
    result_list = []
    out_list = glob.glob(TARGET + "*.out")
    for outfile in out_list:
        print(outfile)
        file_name = os.path.basename(outfile)
        receptor = file_name.split(".")[0]
        ligand = file_name.split(".")[2][3:]
        score_list = get_score(outfile)
        score_list.insert(0, receptor)
        score_list.insert(0, ligand)
        score_list.insert(0, protein_size_dct[receptor])
        score_list.insert(0, protein_size_dct[ligand])
        result_list.append(score_list)
        
    print("Start write csv")
    # write csv
    with open(DOCKING_OUTFILE, "w") as f:
        writer = csv.writer(f)
        writer.writerows(result_list)

if __name__ == "__main__":
    main()
