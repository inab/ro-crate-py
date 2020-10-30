from rocrate.rocrate import ROCrate
from rocrate.model.file import File
from rocrate.model.person import Person
from test.test_common import BaseTest
import uuid

class TestAPI(BaseTest):

    def test_dereferencing(self):
        crate = ROCrate()
        # verify default entities
        root_dataset = crate.dereference('./')
        self.assertEqual(crate.root_dataset, root_dataset)

        metadata_entity = crate.dereference('./ro-crate-metadata.json')
        self.assertEqual(metadata_entity, crate.metadata)

        # dereference added files
        sample_file = self.test_data_dir / 'sample_file.txt'
        file_returned = crate.add_file(sample_file)
        self.assertIsInstance(file_returned, File)
        dereference_file = crate.dereference("sample_file.txt")
        self.assertIsInstance(dereference_file, File)
        self.assertEqual(file_returned, dereference_file)

    def test_dereferencing_equivalent_id(self):
        crate = ROCrate()

        root_dataset = crate.dereference('./')
        self.assertEqual(crate.root_dataset, root_dataset)
        root_dataset = crate.dereference('')
        self.assertEqual(crate.root_dataset, root_dataset)

        metadata_entity = crate.dereference('./ro-crate-metadata.json')
        self.assertEqual(metadata_entity, crate.metadata)
        metadata_entity = crate.dereference('ro-crate-metadata.json')
        self.assertEqual(metadata_entity, crate.metadata)

    def test_contextual_entities(self):
        crate = ROCrate()
        new_person = crate.add_person('#joe', {'name': 'Joe Pesci'})
        person_dereference = crate.dereference('#joe')
        person_prop = person_dereference.properties()
        self.assertEqual(person_prop['@type'], 'Person')
        self.assertEqual(person_prop['name'], 'Joe Pesci')
        self.assertEqual(new_person.properties(), person_prop)

    def test_properties(self):
        crate = ROCrate()

        new_person = crate.add_person('#001', {'name': 'Lee Ritenour'})
        crate.creator = new_person
        self.assertIsInstance(crate.creator, Person)
        self.assertEqual(crate.creator['name'], 'Lee Ritenour')

        new_person2 = crate.add_person('#002', {'name': 'Lee Ritenour'})

        crate.creator = [new_person, new_person2]
        self.assertIsInstance(crate.creator, list)

    def test_uuid(self):
        crate = ROCrate()
        new_person = crate.add_person(name="No Identifier")
        jsonld = new_person.as_jsonld()
        self.assertEqual("Person", jsonld["@type"])
        self.assertTrue(jsonld["@id"].startswith("#"))
        # Check it made a valid UUIDv4
        u = uuid.UUID(jsonld["@id"][1:])
        self.assertEqual(4, u.version)
    
