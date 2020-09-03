import subprocess

cmd = "ascp -l 1000m -P33001 -i /home/kevin/.aspera/cli/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/SRR726/004/SRR7265524/SRR7265524_1.fastq.gz /tmp/GSM3176759.fastq.gz"
process = subprocess.check_call(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)

