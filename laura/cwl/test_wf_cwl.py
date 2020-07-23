from rocrate import rocrate_api

option = int(input("Enter type workflow option:\n [1]: CWL \n [2]: Galaxy\n"))

global wf, files_list, wf_type

if option == 1:
    wf = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/trans_decoder/data/workflows/TransDecoder-v5-wf-2steps.cwl"
    files_list = ["/Users/laurarodrigueznavas/BSC/ro-crate-py/test/test-data/read_crate/test_file_galaxy.txt"]
    wf_type = "CWL"

elif option == 2:
    wf = "/Users/laurarodrigueznavas/BSC/ro-crate-py/test/test-data/read_crate/test_wf_galaxy.ga"
    files_list = ["/Users/laurarodrigueznavas/BSC/ro-crate-py/test/test-data/read_crate/test_file_galaxy.txt"]
    wf_type = "Galaxy"

# Create base package
crate = rocrate_api.make_workflow_rocrate(workflow_path=wf, wf_type=wf_type, include_files=files_list)

# adding a Dataset
sample_dir = '/Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/trans_decoder/data'
dataset_entity = crate.add_directory(sample_dir, 'dataset')

# Add authors info
laura_metadata = {'name': 'Laura Rodriguez-Navas'}
crate.add_person('#laura', laura_metadata)

# write crate to local path
out_path = "/Users/laurarodrigueznavas/BSC/ro-crate-py/laura"
crate.write_crate(out_path)
