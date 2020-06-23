from rocrate import rocrate_api

wf_path = "test/test-data/test_galaxy_wf.ga"
files_list = ["test/test-data/test_file_galaxy.txt"]

# Create base package
wf_crate = rocrate_api.make_workflow_rocrate(workflow_path=wf_path, wf_type="Galaxy", include_files=files_list)

# Write to zip file
# out_path = "/home/test_user/wf_crate"
# wf_crate.write_zip(out_path)

# Add authors info
#joe_metadata = {'name': 'Joe Bloggs'}
#wf_crate.add_person('joe', joe_metadata)

# write crate to disk
out_path = "/Users/laurarodrigueznavas/BSC/ro-crate-py/tests"
wf_crate.write_crate(out_path)
