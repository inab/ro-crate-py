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
from click.testing import CliRunner

from rocrate.cli import cli


@pytest.mark.parametrize("cwd", [False, True])
def test_cli_init(test_data_dir, helpers, monkeypatch, cwd):
    crate_dir = test_data_dir / "ro-crate-galaxy-sortchangecase"
    metadata_path = crate_dir / helpers.METADATA_FILE_NAME
    metadata_path.unlink()

    runner = CliRunner()
    args = []
    if cwd:
        monkeypatch.chdir(str(crate_dir))
    else:
        args.extend(["-c", str(crate_dir)])
    args.append("init")
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert metadata_path.is_file()

    json_entities = helpers.read_json_entities(crate_dir)
    assert "sort-and-change-case.ga" in json_entities
    assert json_entities["sort-and-change-case.ga"]["@type"] == "File"


@pytest.mark.parametrize("cwd", [False, True])
def test_cli_add_workflow(test_data_dir, helpers, monkeypatch, cwd):
    # init
    crate_dir = test_data_dir / "ro-crate-galaxy-sortchangecase"
    runner = CliRunner()
    assert runner.invoke(cli, ["-c", str(crate_dir), "init"]).exit_code == 0
    json_entities = helpers.read_json_entities(crate_dir)
    assert "sort-and-change-case.ga" in json_entities
    assert json_entities["sort-and-change-case.ga"]["@type"] == "File"
    # add
    wf_path = crate_dir / "sort-and-change-case.ga"
    args = []
    if cwd:
        monkeypatch.chdir(str(crate_dir))
        wf_path = wf_path.relative_to(crate_dir)
    else:
        args.extend(["-c", str(crate_dir)])
    for lang in "cwl", "galaxy":
        extra_args = ["add", "workflow", "-l", lang, str(wf_path)]
        result = runner.invoke(cli, args + extra_args)
        assert result.exit_code == 0
        json_entities = helpers.read_json_entities(crate_dir)
        helpers.check_wf_crate(json_entities, wf_path.name)
        assert "sort-and-change-case.ga" in json_entities
        lang_id = f"#{lang}"
        assert lang_id in json_entities
        assert json_entities["sort-and-change-case.ga"]["programmingLanguage"]["@id"] == lang_id


@pytest.mark.parametrize("cwd", [False, True])
def test_cli_add_test_metadata(test_data_dir, helpers, monkeypatch, cwd):
    # init
    crate_dir = test_data_dir / "ro-crate-galaxy-sortchangecase"
    runner = CliRunner()
    assert runner.invoke(cli, ["-c", str(crate_dir), "init"]).exit_code == 0
    json_entities = helpers.read_json_entities(crate_dir)
    def_id = "test/test1/sort-and-change-case-test.yml"
    assert def_id in json_entities
    assert json_entities[def_id]["@type"] == "File"
    # add workflow
    wf_path = crate_dir / "sort-and-change-case.ga"
    runner.invoke(cli, ["-c", str(crate_dir), "add", "workflow", "-l", "galaxy", str(wf_path)]).exit_code == 0
    # add test suite
    result = runner.invoke(cli, ["-c", str(crate_dir), "add", "test-suite"])
    assert result.exit_code == 0
    suite_id = result.output.strip()
    json_entities = helpers.read_json_entities(crate_dir)
    assert suite_id in json_entities
    # add test instance
    result = runner.invoke(cli, ["-c", str(crate_dir), "add", "test-instance", suite_id, "http://example.com", "-r", "jobs"])
    assert result.exit_code == 0
    instance_id = result.output.strip()
    json_entities = helpers.read_json_entities(crate_dir)
    assert instance_id in json_entities
    # add test definition
    def_path = crate_dir / def_id
    args = []
    if cwd:
        monkeypatch.chdir(str(crate_dir))
        def_path = def_path.relative_to(crate_dir)
    else:
        args.extend(["-c", str(crate_dir)])
    extra_args = ["add", "test-definition", "-e", "planemo", "-v", ">=0.70", suite_id, str(def_path)]
    result = runner.invoke(cli, args + extra_args)
    assert result.exit_code == 0
    json_entities = helpers.read_json_entities(crate_dir)
    assert def_id in json_entities
    assert set(json_entities[def_id]["@type"]) == {"File", "TestDefinition"}