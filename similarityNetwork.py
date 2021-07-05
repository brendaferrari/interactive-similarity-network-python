import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import DataStructs
import networkx as nx
import matplotlib.pyplot as plt
from pyvis import network as net

#TO VIEW DATASET
df = pd.read_csv('resources/dataset_ds.smi')
print(df)

#TO CALL DATASET AND DEFINE VARIABLES
smiles, names = [], []
with open("resources/dataset_ds.smi", 'r') as smiles_names_list:
    for smiles_names in smiles_names_list:
        smiles.append(smiles_names.rstrip().split(' ')[0])
        names.append(smiles_names.rstrip().split(' ')[1])
nodes = smiles
print(str(len(smiles))+" molecules loaded from SMILES file")
print(names)
print(nodes)

#TO STATE A INTERACTIVE GRAPH
g = net.Network(height='850px', width='100%',heading='Similarity Network')
nxg = nx.Graph()

#TO ADD NODES
for smi,nam in zip(smiles,names):
    print(smi,nam)
    g.add_node(smi, label=nam)

# TO ADD EDGE IF TC >= THRESHOLD
mols = [Chem.MolFromSmiles(x) for x in smiles]
fps = [AllChem.GetMorganFingerprintAsBitVect(x, 2, 2048) for x in mols]
for i in range(len(smiles)):
    for j in range(i):
        Tc = DataStructs.TanimotoSimilarity(fps[i], fps[j])
        if Tc >= 0.3:
            g.add_edge(smiles[i], smiles[j], length=1000)

nx.draw(nxg, node_size=100)

print(Tc)
print(mols)
fps_arr = np.asanyarray(fps, dtype=int)
print(fps_arr)

#TO GENERATE GRAPH
g.from_nx(nxg)
# g.show('similarityNetwork.html')
g.save_graph('similarityNetwork.html')