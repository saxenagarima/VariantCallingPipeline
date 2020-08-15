# VariantCallingPipeline

This variant calling pipeline uses Trimmomatic, BWA, samtools and bcftools to identify variants from a fastq sequencing file.

Installation:
```
bash install.sh
```
This will install all pipeline dependencies in a local environment using anaconda. The pipeline can then be activated with command vcp.

The pipeline requires an input file in fastq format (example INPUT/reference.fastq) and reference genome file in fasta format (example REFERENCE/reference.fasta). After the pipeline is completed a new window with variants pops-up.
These variants can also be visualized in IGV by clicking on IGV button.
