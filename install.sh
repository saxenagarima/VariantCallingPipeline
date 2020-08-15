path=$(pwd)
conda create -n vcp python=2.7 anaconda
conda install -c bioconda -n vcp samtools=1.6
conda install -c bioconda -n vcp trimmomatic=0.38
conda install -c bioconda -n vcp bwa=0.7
conda install -c bioconda -n vcp bcftools
conda install -c bioconda -n vcp igv

cd
echo "#" >> .bashrc
echo "#vcp" >> .bashrc
echo "alias vcp='source activate vcp;cd $path; python intf.py'" >> .bashrc
echo "alias dvcp='conda deactivate'" >> .bashrc
cd
source ~/.bashrc
source activate vcp
