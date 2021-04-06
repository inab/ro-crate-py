from rocrate import rocrate

listIO = [('fastq_files', [{'class': 'File', 'location': 'data/inputs/U5c_CCGTCC_L001_R1_001.fastq.gz'},
                           {'class': 'File', 'location': 'data/inputs/U5c_CCGTCC_L001_R2_001.fastq.gz'}]),
          ('known_sites_file', {'class': 'File', 'location': 'data/inputs/dbsnp_138.b37.vcf.gz'}),
          ('readgroup_str', '@RG\\tID:H947YADXX\\tSM:NA12878\\tPL:ILLUMINA'), ('chromosome', '1'),
          ('sample_name', 'abc2'),
          ('gvcf', [{'class': 'File', 'location': 'data/outputs/abc2.sorted.md.realigned.bqsr.vcf.gz'},
                    {'class': 'File', 'location': 'data/outputs/abc2.sorted.md.realigned.bqsr.vcf.gz.tbi'}]),
          ('metrics', [{'class': 'File', 'location': 'data/outputs/abc2.sorted.metrics.txt'}])]

# Create RO-Crate from zip file
NF_crate = rocrate.ROCrate("workflow-106-1.crate.zip")
CWL_crate = rocrate.ROCrate("workflow-107-1.crate.zip")

# Data entities
for key, value in listIO:
    if isinstance(value, dict):  # file
        if value['class'] == "File":
            NF_crate.add_file(source=value['location'])
            CWL_crate.add_file(source=value['location'])
    elif isinstance(value, list):  # list of files
        # print(key, value)
        for i in range(len(value)):
            if value[i]['class'] == "File":
                NF_crate.add_file(source=value[i]['location'])
                CWL_crate.add_file(source=value[i]['location'])

NF_crate.writeCrate("./NFcrate")
CWL_crate.writeCrate("./CWLcrate")
NF_crate.writeZip("crate")
CWL_crate.writeZip("crate")
