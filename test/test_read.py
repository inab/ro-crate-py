# Copyright 2019-2020 The University of Manchester, UK
# Copyright 2020 Vlaams Instituut voor Biotechnologie (VIB), BE
# Copyright 2020 Barcelona Supercomputing Center (BSC), ES
# Copyright 2020 Center for Advanced Studies, Research and Development in Sardinia (CRS4), IT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import shutil
import uuid
from pathlib import Path

from rocrate.rocrate import ROCrate
from rocrate.model.file import File
from rocrate.model.dataset import Dataset

_URL = ('https://raw.githubusercontent.com/ResearchObject/ro-crate-py/master/'
        'test/test-data/sample_file.txt')


@pytest.mark.parametrize("load_preview,from_zip", [(False, False), (True, False), (True, True)])
def test_crate_dir_loading(test_data_dir, tmpdir, helpers, load_preview, from_zip):
    # load crate
    crate_dir = test_data_dir / 'read_crate'
    if from_zip:
        zip_source = shutil.make_archive(tmpdir / "read_crate.crate", "zip", crate_dir)
        crate = ROCrate(zip_source, load_preview=load_preview)
    else:
        crate = ROCrate(crate_dir, load_preview=load_preview)

    # check loaded entities and properties
    root = crate.dereference('./')
    assert crate.root_dataset is root
    root_prop = root.properties()
    assert root_prop['@id'] == root.id
    assert root_prop['@id'] == './'
    assert root_prop['@type'] == 'Dataset'

    metadata = crate.dereference(helpers.METADATA_FILE_NAME)
    assert crate.metadata is metadata
    md_prop = metadata.properties()
    assert md_prop['@id'] == metadata.id
    assert md_prop['@id'] == helpers.METADATA_FILE_NAME
    assert md_prop['@type'] == 'CreativeWork'
    assert md_prop['about'] == {'@id': './'}
    # conformsTo is currently hardcoded in the Metadata class, not read from the crate
    assert md_prop['conformsTo'] == {'@id': helpers.PROFILE}
    assert metadata.root is root

    preview = crate.dereference(helpers.PREVIEW_FILE_NAME)
    assert preview == crate.preview
    preview_prop = preview.properties()
    assert preview_prop['@id'] == helpers.PREVIEW_FILE_NAME
    assert preview_prop['@id'] == preview.id
    assert preview_prop['@type'] == 'CreativeWork'
    assert preview_prop['about'] == {'@id': './'}
    if load_preview:
        assert Path(preview.source).name == helpers.PREVIEW_FILE_NAME
    else:
        assert not preview.source

    main_wf = crate.dereference('test_galaxy_wf.ga')
    wf_prop = main_wf.properties()
    assert wf_prop['@id'] == 'test_galaxy_wf.ga'
    assert wf_prop['@id'] == main_wf.id
    assert set(wf_prop['@type']) == helpers.WORKFLOW_TYPES
    assert wf_prop['programmingLanguage'] == {'@id': 'https://galaxyproject.org'}
    assert wf_prop['subjectOf'] == {'@id': 'abstract_wf.cwl'}

    abs_wf = crate.dereference('abstract_wf.cwl')
    abs_wf_prop = abs_wf.properties()
    assert abs_wf_prop['@id'] == 'abstract_wf.cwl'
    assert abs_wf_prop['@id'] == abs_wf.id
    assert set(abs_wf_prop['@type']) == helpers.WORKFLOW_TYPES

    wf_author = crate.dereference('#joe')
    author_prop = wf_author.properties()
    assert author_prop['@id'] == '#joe'
    assert author_prop['@id'] == wf_author.id
    assert author_prop['@type'] == 'Person'
    assert author_prop['name'] == 'Joe Bloggs'

    test_file = crate.dereference('test_file_galaxy.txt')
    test_file_prop = test_file.properties()
    assert test_file_prop['@id'] == 'test_file_galaxy.txt'
    assert test_file_prop['@id'] == test_file.id

    remote_file = crate.dereference(_URL)
    remote_file_prop = remote_file.properties()
    assert remote_file_prop['@id'] == _URL
    assert remote_file_prop['@id'] == remote_file.id

    examples_dataset = crate.dereference('examples/')
    examples_dataset_prop = examples_dataset.properties()
    assert examples_dataset_prop['@id'] == 'examples/'
    assert examples_dataset_prop['@id'] == examples_dataset.id
    assert crate.examples_dir is examples_dataset

    test_dataset = crate.dereference('test/')
    test_dataset_prop = test_dataset.properties()
    assert test_dataset_prop['@id'] == 'test/'
    assert test_dataset_prop['@id'] == test_dataset.id
    assert crate.test_dir is test_dataset

    # write the crate in a different directory
    out_path = tmpdir / 'crate_read_out'
    out_path.mkdir()
    crate.write_crate(out_path)

    metadata_path = out_path / helpers.METADATA_FILE_NAME
    assert metadata_path.exists()
    legacy_metadata_path = out_path / helpers.LEGACY_METADATA_FILE_NAME
    assert not legacy_metadata_path.exists()
    preview_path = out_path / helpers.PREVIEW_FILE_NAME
    assert preview_path.exists()
    if load_preview:
        with open(preview.source) as f1, open(preview_path) as f2:
            assert f1.read() == f2.read()

    json_entities = helpers.read_json_entities(out_path)
    data_entity_ids = [main_wf.id, abs_wf.id, test_file.id, remote_file.id]
    helpers.check_crate(json_entities, data_entity_ids=data_entity_ids)

    for e in main_wf, abs_wf, test_file:
        with open(e.source) as f1, open(out_path / e.id) as f2:
            assert f1.read() == f2.read()


# according to the 1.1 spec, the legacy .jsonld file is still supported for
# crates conforming to version <= 1.0.
def test_legacy_crate(test_data_dir, tmpdir, helpers):
    crate_dir = test_data_dir / 'read_crate'
    # Remove the metadata file, leaving only the legacy one
    (crate_dir / helpers.METADATA_FILE_NAME).unlink()
    crate = ROCrate(crate_dir)
    md_prop = crate.metadata.properties()

    assert crate.dereference(helpers.LEGACY_METADATA_FILE_NAME) is crate.metadata
    assert md_prop['conformsTo'] == {'@id': helpers.LEGACY_PROFILE}

    main_wf = crate.dereference('test_galaxy_wf.ga')
    wf_prop = main_wf.properties()
    assert set(wf_prop['@type']) == helpers.LEGACY_WORKFLOW_TYPES


def test_bad_crate(test_data_dir, tmpdir):
    # nonexistent dir
    crate_dir = test_data_dir / uuid.uuid4().hex
    with pytest.raises(ValueError):
        ROCrate(crate_dir)
    with pytest.raises(ValueError):
        ROCrate(crate_dir, init=True)
    # no metadata file
    crate_dir = tmpdir / uuid.uuid4().hex
    crate_dir.mkdir()
    with pytest.raises(ValueError):
        ROCrate(crate_dir)


@pytest.mark.parametrize("override", [False, True])
def test_init(test_data_dir, tmpdir, helpers, override):
    crate_dir = test_data_dir / "ro-crate-galaxy-sortchangecase"
    if not override:
        (crate_dir / helpers.METADATA_FILE_NAME).unlink()
    crate = ROCrate(crate_dir, init=True)
    assert crate.dereference("./") is not None
    assert crate.dereference(helpers.METADATA_FILE_NAME) is not None
    fpaths = [
        "LICENSE",
        "README.md",
        "sort-and-change-case.ga",
        "test/test1/input.bed",
        "test/test1/output_exp.bed",
        "test/test1/sort-and-change-case-test.yml"
    ]
    dpaths = [
        "test/",
        "test/test1/",
    ]
    for p in fpaths:
        assert isinstance(crate.dereference(p), File)
    for p in dpaths:
        assert isinstance(crate.dereference(p), Dataset)

    out_path = tmpdir / 'ro_crate_out'
    out_path.mkdir()
    crate.write_crate(out_path)

    assert (out_path / helpers.METADATA_FILE_NAME).exists()
    json_entities = helpers.read_json_entities(out_path)
    data_entity_ids = fpaths + dpaths
    helpers.check_crate(json_entities, data_entity_ids=data_entity_ids)
    for p in fpaths:
        with open(crate_dir / p) as f1, open(out_path / p) as f2:
            assert f1.read() == f2.read()


@pytest.mark.parametrize("load_preview,preview_exists", [(False, False), (False, True), (True, False), (True, True)])
def test_init_preview(test_data_dir, tmpdir, helpers, load_preview, preview_exists):
    crate_dir = test_data_dir / "ro-crate-galaxy-sortchangecase"
    dummy_prev_content = "foo\nbar\n"
    if preview_exists:
        with open(crate_dir / helpers.PREVIEW_FILE_NAME, "wt") as f:
            f.write(dummy_prev_content)
    crate = ROCrate(crate_dir, load_preview=load_preview, init=True)
    prev = crate.dereference(helpers.PREVIEW_FILE_NAME)
    if load_preview and not preview_exists:
        assert prev is None
    else:
        assert prev is not None

    out_path = tmpdir / 'ro_crate_out'
    out_path.mkdir()
    crate.write_crate(out_path)

    out_prev_path = out_path / helpers.PREVIEW_FILE_NAME
    if load_preview and not preview_exists:
        assert not out_prev_path.exists()
    else:
        assert out_prev_path.is_file()
        if load_preview:
            assert out_prev_path.open().read() == dummy_prev_content


def test_no_parts(tmpdir):
    crate = ROCrate()

    out_path = tmpdir / 'ro_crate_out'
    out_path.mkdir()
    crate.write_crate(out_path)

    crate = ROCrate(out_path)
    assert not crate.root_dataset["hasPart"]
