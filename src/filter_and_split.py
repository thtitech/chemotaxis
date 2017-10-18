import sys
import glob
import os

# Usage: python filter_and_split.py (target dir) (outputdir)

CUTOFF = 3.25
# CUTOFF = 2.5
MIN_ATOM = 30
MAX_ATOM = 100000

def split_chain(inputfile, outdir, exclude_h = True):
    result_list = []
    # exclude ".pdb"
    base_file_name = os.path.basename(inputfile)[:-4]
    with open(inputfile, "r") as f:
        outfile = None
        current_chain = ""
        for line in f:
            if line[0:4] != "ATOM":
                continue
            # ATOM type
            if exclude_h and (line[77] == "H"):
                continue
            # get chain
            chain = line[21]
            # set init chain
            if current_chain != chain:
                current_chain = chain
                if outfile is not None:
                    outfile.close()
                write_file =  base_file_name + "_" + chain + ".pdb"
                print("write " + write_file + "\n")
                result_list.append(write_file)
                outfile = open(outdir + write_file, "w")
            outfile.write(line.strip() + "\n")
        if outfile is not None:
            outfile.close()
    return result_list

def filter_pdb_with_resolution(pdb_file):
    with open(pdb_file, "r") as f:
        for line in f:
            if line[11:21] == "RESOLUTION":
                f.close()
                return (CUTOFF > float(line[22:].strip().split(" ")[0]))

def get_residue_number(pdb_file):
    cnt = 0
    with open(pdb_file, "r") as f:
        for line in f:
           if (line[0:4] == "ATOM") and (line[13:15] == "CA") :
               cnt += 1
    return cnt

def main():
    if len(sys.argv) != 3:
        print("Warning: invalid argment")
        sys.exit()
    # set dir
    target_dir = sys.argv[1]
    if target_dir[-1] != "/":
        target_dir += "/"
    output_dir = sys.argv[2]
    if output_dir[-1] != "/":
        output_dir += "/"

    # sech pdb files
    pdb_list = glob.glob(target_dir + "*.pdb")
    # filter resolusion
    pdb_list = list(filter(lambda filename: filter_pdb_with_resolution(filename), pdb_list))
    print("----- filter resolution -----")
    print(pdb_list)
    print("----- split chain -----")

    chain_list = []
    # split chain
    for pdb_file_name in pdb_list:
        chain_pdbs = split_chain(pdb_file_name, output_dir)
        chain_list.extend(chain_pdbs)

    # filter number of chain
    print("----- filter number of chain -----")
    result_list = []
    for chain_file in chain_list:
        atom_num = get_residue_number(chain_file)
        if (atom_num < MAX_ATOM) and (atom_num > MIN_ATOM):
            result_list.append(chain_file)
    for file_name in result_list:
        print(file_name)

if __name__ == "__main__":
    main()
    
