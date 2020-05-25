## Please refer to www.submassive.cc for more details.

# Demo:

The command would retrieve the immediate superclass(es) of the entity.

python demo.py --input [query entity]

For example:

```
python demo.py --input http://http-server.carleton.ca/~rgarigue/ontologies/www.kayvium.com/Regional_registry#Staff
```
If a user would rather retrieve the transitive closure, simply add
```
--all
```

To plot the graph subclass relations, simply add
```
--plot
```

To switch between different knowledge graphs, please go to line 14 of demo.py and change the path to different resources.
The default output format is turtle.

## Details of the algorithms can been found in the paper at www.submassive.cc
# Data preprocessing:
generate_cycles.py : generate the subgraph of the entire LOD-a-lot. This step is for the sake of memory efficiency.
two-cycles.py : this is a Python script that allows a user to make decisions about some size-two cycles (between class A and B). The input is encoded as follows:

x : meaningless / errorneous, thus remove both.

l : the class on the left includes the class on the right. In other words, class B is a subclass of class A.

r : similar as above, but reverse order.

e : equivalent classes / same concept. In this project, the misuse of rdfs:equivalentClass and owl:sameAs as two rdfs:subClassOf statements are prohibited and thus the statements are removed.

u : unknown

<note: all the removed edge in the later stage of automated processing are labeled ‘a’>

# SubClassOf:

This refer to the main Python file: subMassive.py

It includes the functionality of HDT (interaction with a knowledge graph), and networkx (for the analysis of graphs) and Z3 (MAXSAT solver). As a result, it is heavy for the memory. Thus, the use of the output files of SUBMASSIVE will be implemented in the near future in another script.

If a user does not have a big memory, he/she can run up to step 3 and then continue from step 4 (load the results of unnecessary relations directly instead of loading the entire sameas data in the memory) for each round of evalution.

See the algorithm part of the paper for details.

# SubPropertyOf:

For relations of rdfs:subPropertyOf, the reflexive edges were removed first and the cycles were resolved by hand. The removed edges are in the file pre-subP.csv

Simply run the code by triggering the execution run.sh

And finally, the equiClass.py file is simply a file to interact with the sameas data.


## Package Dependency:
Please make sure you have
rdflib, z3, networkx, tldextract, pyHDT installed. 
