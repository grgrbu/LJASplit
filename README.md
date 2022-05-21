# LJASplit
Split repeat resolution for long reads

## Introduction

When assembling the genome, de Bruijn graphs are used. These graphs are built on the basis of reading the genome. However, some of the information from the original reads remains unused in the graph.

Due to inaccuracies of readings and imperfections of genome assembler, unresolved repeats occur in the de Bruijn graph.

Different assemblers try to resolve repeats using additional information from the reads.

Widely used [_SPAdes genome assembler_]([url](https://github.com/ablab/spades/)) uses a method based on iterative expansion of paths in a graph supported by reads.

Recently, another method for resolving repeats **Multiplex de bruijn** graph in the [_LJA assembler_]([url](https://github.com/AntonBankevich/LJA)) has been proposed.

Previously, SPAdes used a different method of resolving repeats, based on the idea of **splitting vertices** (split).

Split was quite inconvenient to work with paired reads of illumina. However with long Hi-Fi reads this method seems even more powerful than Multiplex de bruijn graph.



## Objectives and purpose
**Purpose**

Implement the "Split" repeat resolution method and compare it with Multiplex de bruijn graph


**Objectives**

- Learn different different methods for repeat resolution
- Analyze LJA code
- Get list of paths from LJA assembler
- Write a prototype of the split method in Python

## Approaches
Split one-to-many

- If a vertex has one incoming edge and several outgoing edges, then it can be splitted into several, — one copy for each outgoing edge

Explicit split

- If the reads passing through the incoming and outgoing edges from the vertex can be unambiguously splitted, then a vertex should be splitted with a copy for each such path through the vertex.

## Results and futher plans

Implemented methods Split one-to-many and Explicit split.

Example of Split one-to-many:

![image](https://user-images.githubusercontent.com/41432691/169665954-093490d3-4084-441b-80cd-1502615b92b4.png)
![image](https://user-images.githubusercontent.com/41432691/169665960-cbff2438-6d83-4dcb-9875-e25dac1f5d8a.png)

Further development of the work may be the implementation of more advanced methods of vertex separation. After that, it will be possible to compare the results obtained with the Multiplex de bruijn graph method. If the results, as expected, turn out to be better, then this module can be rewritten from Python to C++ and implemented in LJA assembler.

## Literature
Bankevich, A., Bzikadze, A.V., Kolmogorov, M. et al. Multiplex de Bruijn graphs enable genome assembly from long, high-fidelity reads. Nat Biotechnol (2022).

Bankevich A, Nurk S, Antipov D, Gurevich AA, Dvorkin M, Kulikov AS, Lesin VM, Nikolenko SI, Pham S, Prjibelski AD, Pyshkin AV, Sirotkin AV, Vyahhi N, Tesler G, Alekseyev MA, Pevzner PA. SPAdes: a new genome assembly algorithm and its applications to single-cell sequencing. J Comput Biol. 2012 May;19(5):455-77.

## Launch instructions

The project is launched with `main.py`, where .gfa and .als files — graph and reads, respectively should be specified.

`graph.py`, `vertex.py`, `edge.py` contain descriptions of the main methods.

`make_short.py` can be used for quick starts with incomplete sets of reads

`analytics.py` contains several useful for getting insights about data and debagging functions that build statistics. For example, the distribution of degrees of vertices:

![image](https://user-images.githubusercontent.com/41432691/169667226-47c29171-a588-4052-b7d8-d48adf89dd96.png)

files `short.gfa` and `check_short_1.gfa` illusrate split one-to-many approach. They can be visualised through Bandage 
