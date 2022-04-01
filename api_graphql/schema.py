import datetime
import typing

import strawberry

import accounts.utils
from accounts.documents import UserDocument


def get_books():
    return [
        Book(
            title='The Great Gatsby',
            author='F. Scott Fitzgerald',
        ),
    ]


@strawberry.type
class Book:
    title: str
    author: str


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


def user_document_to_graphql(user_documents: typing.Iterable[UserDocument]):
    return [
        User(
            uid=document.uid,
            uidNumber=document.uidNumber,
            gecos=document.gecos,
            eppns=document.eppns,
            status=TrainingStatus(
                training_uptodate=document.status.training_uptodate,
                last_account_activity=document.status.last_account_activity,
            )
        )
        for document in user_documents
    ]


def get_all_users():
    return user_document_to_graphql(accounts.utils.get_all_users())


@strawberry.type
class Query:
    users: typing.List[User] = strawberry.field(resolver=get_all_users)
    books: typing.List[Book] = strawberry.field(resolver=get_books)


schema = strawberry.Schema(query=Query)
