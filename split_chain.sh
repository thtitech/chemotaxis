PDBDIR="/gs/hs0/tga-megadock/hayashi/data/Chemotaxis/structures/row/"
CHAINDIR="/gs/hs0/tga-megadock/hayashi/data/Chemotaxis/structures/chains/"

for f in `ls ${PDBDIR} | grep pdb`
do
   echo ${PDBDIR}$f
   python src/split_chain.py ${PDBDIR}$f ${CHAINDIR}
done


