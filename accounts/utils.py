import typing

from accounts.documents import UserDocument


def get_users_by_uid(user_uids: typing.Iterable[str]) -> typing.Iterable[UserDocument]:
    return UserDocument.objects(uid__in=user_uids)


def get_all_users() -> typing.Iterable[UserDocument]:
    return UserDocument.objects()
