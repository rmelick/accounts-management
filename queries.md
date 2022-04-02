# Get all information from Mongo

```
{
  users {
    eppns
    gecos
    uid
    uidNumber
    status {
      trainingUptodate
      lastAccountActivity
    }
  }
}
```

# Update any field on the user, and get the resulting User object

```
mutation ModifyUser {
  __typename
  modifyUser(user: {uid: "axj", uidNumber: 1111, gecos: "Alice Jones", eppns: ["alice@gmail.com", "a.jones@stanford.edu"], status: {trainingUptodate: true, lastAccountActivity: "2022-03-01T15:48:12"}}) {
    record 
    {
      eppns
      gecos
      uid
      uidNumber
      status {
        trainingUptodate
        lastAccountActivity
      }
    }
  }
}
```

# Set `last_account_activity` to current timestamp

I decided to implement this as a separate mutation from the giant `modifyUser` that allows editing any field. This means
that the client doesn't have to fetch all the user data and then pass it back in the mutation. It also allows use to
determine the current time on the server side, so we don't have to worry about client side timezones or anything.

```
mutation UpdateAccountActivity {
  __typename
  updateAccountActivity(userUid: "wns") {
    record {
      uid
      status {
        lastAccountActivity
      }
    }
  }
}

```

The other option would have been to use the `ModifyUser` mutation above, and specify a current timestamp in the
parameters to `modifyUser`