from rocrate import rocrate_api

out_path = "/Users/laurarodrigueznavas/BSC/ro-crate-py/laura/cwl"
out_path_with_filename = out_path + "/test_wf_cwl.zip"

global wf, files_list

option = int(input("Enter type workflow option:\n [1]: Basic \n"))

if option == 1:
    wf = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/basic_example.cwl"
    files_list = [
        '/Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/NA12878.bam',
        '/Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/hg38.fa'
    ]

# Create RO-Crate
crate = rocrate_api.make_workflow_rocrate(workflow_path=wf, wf_type="CWL", include_files=files_list)

# Write RO-Crate
crate.write_crate(out_path)

# Compress RO-Crate
# crate.write_zip(out_path)
# crate.write_zip(out_path_with_filename)
