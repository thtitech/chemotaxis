import sys
import os

def split_chain(inputfile, outdir):
    result_list = []
    # exclude ".pdb"
    base_file_name = os.path.basename(inputfile)[:-4]
    with open(inputfile, "r") as f:
        outfile = None
        current_chain = ""
        for line in f:
            if line[0:4] != "ATOM":
                continue
            # ATOM line
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
        
if __name__ == "__main":
    if (len(sys.argv) != 3):
        print("invalid argment")
        sys.exit()

    inputfile = sys.argv[1]
    outdir = sys.argv[2]
    
    if outdir[-1] != "/":
        outdir = outdir + "/"


