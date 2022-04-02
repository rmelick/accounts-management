import json
import logging

from accounts.documents import UserDocument

log = logging.getLogger(__name__)

if __name__ == '__main__':
    # force import of settings so we connect to mongo

    with open("initial-data.json") as json_file:
        json_data = json.load(json_file)
        for user in json_data:
            document = UserDocument.from_json(json.dumps(user))
            document.save(force_insert=True)
            log.info("Successfully saved user to db {}".format(user))
