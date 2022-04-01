from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, IntField, ListField, \
    BooleanField, DateTimeField


class TrainingStatusDocument(EmbeddedDocument):
    training_uptodate = BooleanField()
    last_account_activity = DateTimeField()


class UserDocument(Document):
    uid = StringField()
    uidNumber = IntField()
    gecos = StringField()
    eppns = ListField(StringField())
    status = EmbeddedDocumentField(TrainingStatusDocument)
