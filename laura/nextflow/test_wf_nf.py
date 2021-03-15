from rocrate.rocrate import ROCrate

wf = "/Users/laurarodrigueznavas/BSC/ro-crate-py/laura/nextflow/data/nextflow.nf"
files_list = "/Users/laurarodrigueznavas/BSC/ro-crate-py/laura/nextflow/test_file_nf.txt"

out_path = "/Users/laurarodrigueznavas/BSC/ro-crate-py/laura/nextflow"
out_path_with_filename = out_path + "/test_wf_nf.zip"

# Create RO-Crate
crate = ROCrate(out_path_with_filename)

lineList = [line.rstrip('\n') for line in open(files_list)]
print(lineList)

for file in lineList:
    crate.add_file(file)

# Write RO-Crate
crate.write_crate(out_path)

# Compress RO-Crate
# crate.write_zip(out_path)
# crate.write_zip(out_path_with_filename)
