from rocrate import rocrate_api

wf = "/Users/laurarodrigueznavas/BSC/ro-crate-py/laura/galaxy/data/test_wf_galaxy.ga"
files_list = ["/Users/laurarodrigueznavas/BSC/ro-crate-py/laura/galaxy/data/test_file_galaxy.txt"]

out_path = "/Users/laurarodrigueznavas/BSC/ro-crate-py/laura/galaxy"
out_path_with_filename = out_path + "/test_wf_galaxy.zip"

# Create RO-Crate
crate = rocrate_api.make_workflow_rocrate(workflow_path=wf, wf_type="Galaxy", include_files=files_list)

# Write RO-Crate
crate.write_crate(out_path)

# Compress RO-Crate
# crate.write_zip(out_path)
# crate.write_zip(out_path_with_filename)
