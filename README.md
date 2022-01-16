# CMPE549-TermProjectTemplate
A template for term project 

## A tool for *de-novo* Identification of Composite Transposons



# Requirements

- Linux (not tested on Windows and MacOS)
- [Phyton](https://www.python.org/) 3.8 or later

## The required packages 

- [ISEScan](https://github.com/xiezhq/ISEScan) ISEScan-1.7.2.3
- [prokka](https://github.com/tseemann/prokka) prokka-1.14.5
- [networkx](https://github.com/networkx/networkx) networkx-2.6.3

# Installation 

We recommend to use conda but not necessary

```
conda update conda --all
conda create --name excota python=3.8
conda activate excota

```

You can use pip to install dependecies

```
pip install isescan
conda install -c conda-forge -c bioconda -c defaults prokka
pip install networkx[all]
```



### What is a Composite Tranposon?

Transposons are the DNA sequences can alter its position in genome, changing the genome size. Also, they can contribute to genome and gene evolution. Composite transposons are composed of two transposon and genetic material inside the flanking transposons. 

<p align="center">
<img src="https://www.researchgate.net/profile/Supathep-Tansirichaiya/publication/306088165/figure/fig2/AS:667817586208768@1536231528040/The-structures-of-composite-transposons-and-TUs-The-composite-transposons-consist-of-two.jpg" width="600" />
</p>

Figure from: PCR-based detection of composite transposons and translocatable units from oral metagenomic DNA

### Why Composite Transposons Are Important? 

They often carry antibiotic genes, and sometimes metabolic genes such as degradation of xenobitiotics and metal resistance. Therefore, they are crucial to find interesting metabolic functions, transfer of antibiotic resistance and 
spread them among organisms. 

<p align="center">
<img src="http://www.hammiverse.com/lectures/18/images/5-8.png" width="600" />
</p>

### What are the limitations of existing tools?

There are too many tools to find the transposons but there is a few tools related to composite transposons. One of them is [TnComp_finder](https://github.com/danillo-alvarenga/tncomp_finder). The limitation of TnComp_Finder is that it can be only used in complete genomes. For the incomplete genomes, it will probably fail because short-read sequencing (most of the time) is not able to capture composite transposons. Because the genome databases are mostly consists of incomplete genomes, a tool that can work also in incomplete genomes is essential.

<p align="center">
<img src="https://www.researchgate.net/profile/Tahir-Mehmood-14/publication/281491178/figure/fig2/AS:667643811987466@1536190097833/Number-of-completed-and-incomplete-genomes-sequencing-projects-on-Genomes-OnLine-Database.png" width="600" />
</p>

<p align="center">
<img src="figures/limitation.png" width="600" />
</p>

### Suggested Improvements

To capture the composite transposons in incomplete genomes, assembly graphs built from the raw reads can be very helpful unlike using fasta sequences (TnComp_Finder uses fasta sequences). Graph algorithms can be used to find transposon motifs and possible composite transposons can be identified even *de-novo*. Then, the candidates can be searched in existing gene databases for functional analysis. 

<p align="center">
<img src="figures/flowchart.png" width="600" />
</p>

### PIPELINE 

<p align="center">
<img src="figures/pipeline.png" width="600" />
</p>


### Outputs 

The spread of composite transposons can be searched and visuliazed for better understanding with phylogenetic trees. Spread between different species can be shown.



