from uuid import UUID
from bson.binary import Binary
from os import environ as env
import pymongo


class Owner:
    def __init__(self, owner):
        if owner['uuid'] is None:
            raise ValueError("The owner must have an uuid")

        if type(owner['uuid']) is not bytes and type(owner['uuid']) is not Binary:
            raise TypeError("The owner uuid must be a UUID")

        if 'name' not in owner:
            if owner['firstname'] is None or owner['lastname'] is None:
                raise ValueError("The owner must have a name or a firstname and a lastname")
            else:
                self.name = owner['firstname'] + " " + owner['lastname']
        else:
            self.name = owner['name']

        if type(self.name) is not str:
            raise TypeError("The owner name must be a string")

        self.id = UUID(bytes=owner['uuid'])

    @staticmethod
    def load(uuid):
        """
        Load an owner from the database
        :param uuid:
        :return:
        """
        try:
            uuid = UUID(uuid)
        except ValueError as e:
            print('error uuid', str(e))
            raise ValueError("The uuid must be a UUID")

        mongo_host = env.get('MONGO_HOST', 'localhost')
        mongo_port = int(env.get('MONGO_PORT', 27017))
        mongo_db = env.get('MONGO_DB', 'mayaprotect')
        mongo_client = pymongo.MongoClient(mongo_host, int(mongo_port))
        db = mongo_client[mongo_db]
        coll = db['owners']
        owner = coll.find_one({"uuid": Binary.from_uuid(uuid)})
        if owner is None:
            print('error owner not found')
            raise ValueError("The owner does not exist")
        else:
            return Owner(owner)

    def __to_json__(self):
        """
        Convert the owner to json
        :return:
        """
        return {
            "id": str(self.id),
            "name": self.name
        }

    def __to_json_for_object__(self):
        """
        Convert the owner to json
        :return:
        """
        return {
            "uuid": Binary.from_uuid(self.id),
            "name": self.name
        }