from bioservices import *
import csv

# output file
# "pathway", pathway id
# "keggid", kegg id, gene name
# "uniprotid", keggid, uniprot id, .... (correspond upper kegg id)
# "pdbid", keggid, pdb id, .... (correspond upper kegg id)

TARGET = "/gs/hs0/tga-megadock/hayashi/data/Chemotaxis/"
pathway_list = ["eco02030", "stm02030", "tma02030"]
species_list = ["eco", "stm", "tma"]
outfile = TARGET + "pdb_list.csv"

def get_kegg_to_uni():
    # retun dct key: species name, value: dct kegg to list of uni
    result = {}
    for s in species_list:
        k = KEGG()
        # dct kegg to uni
        kegg_to_uni_dct = {}
        # tmp is uni to kegg
        uni_to_kegg = k.conv(s, "uniprot")
        # reverse key and value
        for key in uni_to_kegg.keys():
            if uni_to_kegg[key] not in kegg_to_uni_dct:
                # print("Warning: not correspond kegg id and uniprot: " + uni_to_kegg[key])
                kegg_to_uni_dct[uni_to_kegg[key]] = []
            kegg_to_uni_dct[uni_to_kegg[key]].append(key)
        result[s] = kegg_to_uni_dct
    return result

def get_uni_to_kegg():
    # return dct key: species name, value: dct uni to kegg
    result = {}
    for s in species_list:
        k = KEGG()
        result[s] = k.conv(s, "uniprot")
    return result

def convert_uni_to_pdb(uniprot_list):
    u = UniProt()
    return u.mapping("ACC", "PDB_ID", " ".join(uniprot_list))
        
def main():
    kegg_uni_dct = get_kegg_to_uni()
    for s, pathway in zip(species_list, pathway_list):
        # for each pathway
        print(pathway)
        # get keggids in pathway
        k = KEGG()
        # kegg_dct is key: keggid value: gene name
        kegg_to_gene_name_dct = k.parse(k.get(pathway))["GENE"]
        
        # kegg_to_uni is key: keggid value: list of uniprot
        kegg_to_uni_database = kegg_uni_dct[s]
        
        # convert keggid to uniprot id
        kegg_to_uni_dct = {}
        for kegg_id in kegg_to_gene_name_dct.keys():
            # get list of keggid
            query_kegg_id = s + ":" + kegg_id
            uniprot_list = kegg_to_uni_database[query_kegg_id] if (query_kegg_id in kegg_to_uni_database) else None
            if uniprot_list is None:
                # there is not in database
                continue
            kegg_to_uni_dct[kegg_id] = list(map(lambda x: x[3:], uniprot_list))
        print(kegg_to_uni_dct)
                
        # convert form uniprot to pdb
        kegg_to_pdb_dct = {}
        for kegg_id in kegg_to_uni_dct.keys():
            kegg_to_pdb_dct[kegg_id] = convert_uni_to_pdb(kegg_to_uni_dct[kegg_id])
        print(kegg_to_pdb_dct)

        # write result
        with open(outfile, "a") as f:
            f.write("pathway," + pathway + "\n")
            for key in kegg_to_uni_dct.keys():
                # for each kegg id
                print(key)
                f.write("kegg," + key + "," + kegg_to_gene_name_dct[key] + "\n")
                for uniid in kegg_to_uni_dct[key]:
                    # for each uniprot
                    print(uniid)
                    f.write("uniprot," + uniid + "\n")
                    if uniid not in kegg_to_pdb_dct[key]:
                        f.write("pdb,\n")
                    else:
                        f.write("pdb," + ",".join(kegg_to_pdb_dct[key][uniid]) + "\n")
        
if __name__ == "__main__":
    main()
    
