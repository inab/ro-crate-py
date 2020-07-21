from rocrate import rocrate_api

option = int(input("Enter type workflow option:\n [1]: CWL \n [2]: Galaxy\n"))

global wf, files_list, wf_type

if option == 1:
    wf = "https://raw.githubusercontent.com/kids-first/kf-alignment-workflow/dm-ipc-fixes/workflows/kfdrc_alignment_wf_cyoa.cwl"
    files_list = ["/Users/laurarodrigueznavas/BSC/ro-crate-py/laura/sample_file.txt"]
    wf_type = "CWL"

elif option == 2:
    wf = "/Users/laurarodrigueznavas/BSC/ro-crate-py/test/test-data/read_crate/test_galaxy_wf.ga"
    files_list = ["/Users/laurarodrigueznavas/BSC/ro-crate-py/test/test-data/read_crate/test_file_galaxy.txt"]
    wf_type = "Galaxy"

# Create base package
crate = rocrate_api.make_workflow_rocrate(workflow_path=wf, wf_type=wf_type, include_files=files_list)

# Add authors info
laura_metadata = {'name': 'Laura Rodriguez-Navas'}
crate.add_person('#laura', laura_metadata)

# write crate to local path
out_path = "/Users/laurarodrigueznavas/BSC/ro-crate-py/laura"
crate.write_crate(out_path)
