import subprocess
import csv
from time import sleep

inputfile = "/gs/hs0/tga-megadock/hayashi/data/Chemotaxis/pdb_list.csv"
outdir = "/gs/hs0/tga-megadock/hayashi/data/Chemotaxis/structures/"

with open(inputfile, "r") as f:
    for line in f:
        subprocess.call(["wget", "https://files.rcsb.org/download/" + line.strip() + ".pdb", "-P", outdir])
        sleep(1)
