from rocrate import rocrate
from rocrate.model import entity
from rocrate.model.computationalworkflow import Workflow
from pathlib import Path

import ssl

out_path = "/Users/laurarodrigueznavas/BSC/ro-crate-py/laura/cwl"
# out_path_with_filename = out_path + "/test_wf_cwl.zip"

# change only for OSX
ssl._create_default_https_context = ssl._create_unverified_context

# Create RO-Crate
wf_crate = rocrate.ROCrate()
wf_path = Path("https://github.com/inab/Wetlab2Variations/blob/eosc-life/cwl-workflows/workflows/workflow.cwl")

print(wf_crate.root_dataset.as_jsonld())
wf_file = Workflow(wf_crate, str(wf_path), wf_path.name)
wf_crate._add_data_entity(wf_file)
wf_crate.set_main_entity(wf_file)

programming_language_entity = entity.Entity(wf_crate, 'https://www.commonwl.org/v1.1/',)
wf_file['programmingLanguage'] = programming_language_entity

inputs = entity.Entity(wf_crate)
wf_file['inputs'].append("file1")

# Write RO-Crate
wf_crate.write_crate(out_path)
