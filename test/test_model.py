import unittest
import os
from rocrate.rocrate import ROCrate
from rocrate.model.file import File
from rocrate.model.person import Person
from test.test_common import BaseTest

class TestAPI(BaseTest):


    def test_dereferencing(self):
        crate = ROCrate()
        # verify default entities
        root_dataset = crate.dereference('./')
        self.assertEqual(crate.root_dataset, root_dataset)

        metadata_entity = crate.dereference('./ro-crate-metadata.jsonld')
        self.assertEqual(metadata_entity, crate.metadata)

        # dereference added files
        sample_file = os.path.join(self.test_data_dir, 'sample_file.txt')
        file_returned = crate.add_file(sample_file)
        self.assertIsInstance(file_returned, File)
        dereference_file = crate.dereference("sample_file.txt")
        self.assertIsInstance(dereference_file, File)
        self.assertEqual(file_returned,dereference_file)

    def test_dereferencing_equivalent_id(self):
        crate = ROCrate()

        root_dataset = crate.dereference('./')
        self.assertEqual(crate.root_dataset, root_dataset)
        root_dataset = crate.dereference('')
        self.assertEqual(crate.root_dataset, root_dataset)

        metadata_entity = crate.dereference('./ro-crate-metadata.jsonld')
        self.assertEqual(metadata_entity, crate.metadata)
        metadata_entity = crate.dereference('ro-crate-metadata.jsonld')
        self.assertEqual(metadata_entity, crate.metadata)

    def test_contextual_entities(self):
        crate = ROCrate()
        new_person = crate.add_person('joe' , {'name': 'Joe pesci'})
        person_dereference = crate.dereference('#joe')

    def test_properties(self):
        crate = ROCrate()

        new_person = crate.add_person('001' , {'name': 'Lee Ritenour'})
        crate.author = new_person
        self.assertIsInstance(crate.author, Person)
        self.assertEqual(crate.author['name'], 'Lee Ritenour')


