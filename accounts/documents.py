import datetime

from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, IntField, ListField, \
    BooleanField, DateTimeField
from mongoengine.errors import DoesNotExist
from mongoengine.queryset.visitor import Q


class TrainingStatusDocument(EmbeddedDocument):
    training_uptodate = BooleanField()
    last_account_activity = DateTimeField()


class UserDocument(Document):
    uid = StringField(unique=True)
    uidNumber = IntField(unique=True)
    gecos = StringField()
    eppns = ListField(StringField())
    status = EmbeddedDocumentField(TrainingStatusDocument)

    @staticmethod
    def get_or_create(uid: str, uid_number: int = None):
        """
        Find the document with the uid OR uidNumber, or create a brand new one.
        You must still call .save() on the newly created document in order to persist it
        to Mongo
        :param uid:
        :param uid_number:
        :return:
        """
        try:
            if uid_number is not None:
                return UserDocument.objects(Q(uid=uid) | Q(uidNumber=uid_number)).get()
            else:
                return UserDocument.objects(uid=uid).get()
        except DoesNotExist:
            return UserDocument()

    def update_account_activity(self):
        # mongo uses "naive" datetimes, so use utcnow instead of now(tz=utc)
        self.status.last_account_activity = datetime.datetime.utcnow()
        self.save()
