import datetime
import typing

import strawberry

import accounts.utils
from accounts.documents import UserDocument, TrainingStatusDocument


@strawberry.type
class TrainingStatus:
    training_uptodate: bool
    last_account_activity: datetime.datetime


@strawberry.type
class User:
    uid: strawberry.ID
    uidNumber: int
    gecos: str
    eppns: typing.List[str]
    status: TrainingStatus

    @classmethod
    def from_mongo_document(cls, document: UserDocument):
        return cls(
            uid=document.uid,
            uidNumber=document.uidNumber,
            gecos=document.gecos,
            eppns=document.eppns,
            status=TrainingStatus(
                training_uptodate=document.status.training_uptodate,
                last_account_activity=document.status.last_account_activity,
            )
        )


@strawberry.input
class TrainingStatusMutation:
    training_uptodate: bool
    last_account_activity: datetime.datetime


@strawberry.input
class UserMutation:
    """
    Best practice for mutations is a single object
    https://graphql-rules.com/rules/mutation-input-arg
    """
    uid: strawberry.ID
    uidNumber: int
    gecos: str
    eppns: typing.List[str]
    status: TrainingStatusMutation

    def overwrite_mongo_document(self, document):
        document.uid = self.uid
        document.uidNumber = self.uidNumber
        document.gecos = self.gecos
        document.eppns = self.eppns
        document.status = TrainingStatusDocument(
            training_uptodate=self.status.training_uptodate,
            last_account_activity=self.status.last_account_activity
        )
        document.save()


@strawberry.type
class UserMutationPayload:
    record: User


@strawberry.type
class UpdateAccountActivityPayload:
    record: User


def user_document_to_graphql(user_documents: typing.Iterable[UserDocument]):
    return [
        User.from_mongo_document(document)
        for document in user_documents
    ]


def get_all_users():
    return user_document_to_graphql(accounts.utils.get_all_users())


@strawberry.type
class Query:
    users: typing.List[User] = strawberry.field(resolver=get_all_users)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def modify_user(self, user: UserMutation) -> UserMutationPayload:
        document = UserDocument.get_or_create(user.uid, user.uidNumber)
        user.overwrite_mongo_document(document)
        user_response = User.from_mongo_document(document)
        return UserMutationPayload(
            record=user_response
        )

    @strawberry.mutation
    def update_account_activity(self, user_uid: str) -> UpdateAccountActivityPayload:
        user_document = UserDocument.objects.get(uid=user_uid)
        user_document.update_account_activity()
        user_response = User.from_mongo_document(user_document)
        return UpdateAccountActivityPayload(record=user_response)


schema = strawberry.Schema(query=Query, mutation=Mutation)
