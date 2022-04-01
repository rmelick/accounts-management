import json

import mongoengine as mongoengine

from accounts.documents import UserDocument
from accounts_management import settings

if __name__ == '__main__':
    mongoengine.connect(host=settings.MONGO_CONNECT_STR)
    with open("initial-data.json") as json_file:
        json_data = json.load(json_file)
        for user in json_data:
            document = UserDocument.from_json(json.dumps(user))
            document.save()
