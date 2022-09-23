from uuid import UUID, uuid4
from app.owner import Owner
import pymongo
from bson.binary import Binary


class Hive:
    def __init__(self, hive):
        if hive['station_uuid'] is None:
            print('error station_uuid')
            raise ValueError("The hive must have a station_uuid")

        if hive['owner_uuid'] is None:
            print('error owner_uuid')
            raise ValueError("The hive must have an owner_uuid")

        try:
            owner = Owner.load(hive['owner_uuid'])
        except Exception as e:
            print('error owner', str(e))
            raise e

        try:
            self.station_id = UUID(hive['station_uuid'])
        except ValueError as e:
            print('error station_id', str(e))
            raise ValueError("The hive station_uuid must be a UUID")

        self.last_temperature = 0.0
        self.last_sound_level = 0.0
        self.last_weight = 0.0
        self.last_events = []
        self.owner = owner

        self.id = uuid4()

    def __to_json__(self):
        """
        Convert the hive to json
        :return:
        """
        return {
            "id": str(self.id),
            "last_temperature": self.last_temperature,
            "last_sound_level": self.last_sound_level,
            "last_weight": self.last_weight,
            "last_events": self.last_events,
            "station_id": str(self.station_id),
            "owner": self.owner.__to_json__()
        }

    def __to_save_data__(self):
        """
        Convert the hive to json
        :return:
        """
        return {
            "uuid": Binary.from_uuid(self.id),
            "last_temperature": self.last_temperature,
            "last_sound_level": self.last_sound_level,
            "last_weight": self.last_weight,
            "last_events": self.last_events,
            "station_uuid": Binary.from_uuid(self.station_id),
            "owner": self.owner.__to_json_for_object__()
        }

    def save(self, mongo_host, mongo_port, mongo_db):
        """
        Save the hive in the database
        :return:
        """
        mongo_client = pymongo.MongoClient(mongo_host, int(mongo_port))
        db = mongo_client[mongo_db]
        coll = db['hives']
        res = coll.insert_one(self.__to_save_data__())
        if res.inserted_id is None:
            raise ValueError("The hive has not been saved")
