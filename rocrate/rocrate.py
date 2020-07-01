#!/usr/bin/env python

## Copyright 2019-2020 The University of Manchester, UK
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

import os
import uuid
from pathlib import Path
import zipfile
import tempfile

from .model import contextentity
from .model.root_dataset import RootDataset
from .model.file import File
from .model.person import Person
from .model.dataset import Dataset
from .model.metadata import Metadata
from .model.preview import Preview


from arcp import generate
from arcp import arcp_random

class ROCrate():

    def __init__(self):
        self.default_entities = []
        self.data_entities = []
        self.contextual_entities = []
        self.uuid = uuid.uuid4()

        #create metadata and assign it to data_entities
        self.metadata = Metadata(self)  # metadata init already includes itself into the root metadata
        self.default_entities.append(self.metadata)

        #create root entity (Dataset) with id './' and add it to the default entities
        # TODO: default_properties must inclue name, description, datePublished, license
        self.root_dataset = RootDataset(self)
        self.default_entities.append(self.root_dataset)

        #create preview entity and add it to default_entities
        self.preview = Preview(self)
        self.default_entities.append(self.preview)


    # Properties
    # missing? 
        # input
        # output
        # programmingLanguage
        # sdPublisher
        # url
        # version

    @property
    def name(self):
        return self.root_dataset['name']

    @name.setter
    def name(self, value):
        self.root_dataset['name'] = value

    # dateCreated?
    @property
    def datePublished(self):
        return self.root_dataset['datePublished']

    @datePublished.setter
    def datePublished(self, value):
        self.root_dataset['datePublished'] = value

    @property
    def creator(self):
        return self.root_dataset['creator']

    @creator.setter
    def creator(self, value):
        self.root_dataset['creator'] = value

    @property
    def license(self):
        return self.root_dataset['license']

    @license.setter
    def license(self, value):
        self.root_dataset['license'] = value

    @property
    def description(self):
        return self.root_dataset['description']

    @description.setter
    def description(self, value):
        self.root_dataset['description'] = value

    @property
    def keywords(self):
        return self.root_dataset['keywords']

    @keywords.setter
    def keywords(self, value):
        self.root_dataset['keywords'] = value

    @property
    def publisher(self):
        return self.root_dataset['publisher']

    @publisher.setter
    def publisher(self, value):
        self.root_dataset['publisher'] = value

    @property
    def image(self):
        return self.root_dataset['image']

    @image.setter
    def image(self, value):
        self.root_dataset['image'] = value

    @property
    def CreativeWorkStatus(self):
        return self.root_dataset['CreativeWorkStatus']

    @CreativeWorkStatus.setter
    def CreativeWorkStatus(self, value):
        self.root_dataset['CreativeWorkStatus'] = value

    def resolve_id(self, relative_id):
        return generate.arcp_random(relative_id.strip('./'), uuid=self.uuid)

    def get_entities(self):
        return self.default_entities + self.data_entities + self.contextual_entities

    def set_main_entity(self, main_entity):
        self.root_dataset['mainEntity'] = main_entity

    def _get_root_jsonld(self):
        self.root_dataset.properties()

    def dereference(self, entity_id):
        canonical_id = self.resolve_id(entity_id)
        for entity in self.get_entities():
            if canonical_id == entity.canonical_id():
                return entity
        return None

    # source: file object or path (str)
    def add_file(self, source, crate_path = None , properties = None):
        # print('adding file' + source)
        file_entity = File(self, source,crate_path,properties)
        self._add_data_entity(file_entity)
        return file_entity

    def remove_file(self,file_id):
        #if file in data_entities:
        self._remove_data_entity(file_id)

    def add_directory(self, source, crate_path = None , properties = None):
        dataset_entity = Dataset(self,source,crate_path,properties)
        self._add_data_entity(dataset_entity)

    def remove_directory(self,dir_id):
        #if file in data_entities:
        self._remove_data_entity(dir_id)

    def _add_data_entity(self, data_entity):
        self._remove_data_entity(data_entity)
        self.data_entities.append(data_entity)

    def _remove_data_entity(self, data_entity):
        if data_entity in self.data_entities:
            self.data_entities.remove(data_entity)



    ################################
    ##### Contextual entities ######
    ################################

    def _add_context_entity(self, entity):
        if entity in self.contextual_entities: self.contextual_entities.remove(entity)
        self.contextual_entities.append(entity)

    def add_person(self, identifier, properties = {}):
        new_person = Person(self, identifier,properties)
        self._add_context_entity(new_person)
        return new_person

    #TODO
    #def fetch_all(self):
        # fetch all files defined in the crate

    ################################
    #####  ######
    ################################

    def get_info(self):
        #return dictionary with basic info to build a preview file
        info_dict = {
            'name': self.name,
            'creator': self.creator,
            'image': self.image
        }
        return info_dict




    # write crate to local dir
    def write_crate(self, base_path):
        Path(base_path).mkdir(parents=True, exist_ok=True)
        # write data entities
        for writable_entity in self.data_entities + self.default_entities:
            writable_entity.write(base_path)

    def write_zip(self,out_zip):
        zf = zipfile.ZipFile(out_zip, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
        for writable_entity in self.data_entities + self.default_entities:
            writable_entity.write_zip(zf)
        zf.close()
        return zf.filename



