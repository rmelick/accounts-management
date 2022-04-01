
We are implementing a backend service that will be the source of truth for our accounts and resource management for all SLAC scientific users. As part of this project, we need to evaluate and compare some frameworks to ensure that it will ease development and reduce bugs.

It has been decided that we should utilise [GraphQL](https://graphql.org/) and [mongodb](https://www.mongodb.com) as the core parts of our technology stack. It would also be preferable to use (python)[https://www.python.org/] and (strawberry)[https://strawberry.rocks/].

Please do the following:

- write a micro service that will serve a query in graphql with the following documents from the database backend:
```
[{
  "uid": "axj",
  "gecos": "Alice Jones",
  "uidNumber" 1111,
  "eppns": [ "alice@gmail.com", "a.jones@stanford.edu" ],
  "status" {
    "training_uptodate": True,
    "last_account_activity": "2022-03-01T15:48:12Z"
  },
  {
  "uid": "wns",
  "gecos": "Ben Smith",
  "uidNumber" 1261,
  "eppns": [ "ben.smith@hotmail.com", "ben@yale.edu" ],
  "status" {
    "training_uptodate": True,
    "last_account_activity": "2022-01-01T07:12:03Z"
  },
  {
  "uid": "cjt",
  "gecos": "Clare Taylor",
  "uidNumber" 2983,
  "eppns": [ "clare.taylor@yahoo.com", "cjt@mit.edu" ],
  "status" {
    "training_uptodate": False,
    "last_account_activity": "2021-10-27T21:28:09Z"
   }
}]
```
- write a mutation that will allow arbitrary updates of any field on the above schema.

- what would the graphql statement be to update the "last_account_activity" timestamp for user "wns" to the current time.

- wrap up the micro service in a Dockerfile and upload all code to GitHub.

- describe (no code required) how we should implement authentication and authorisation with this setup.

- provide details on pros and cons to your approach using your selected technology stack. what other technologies would you have chosen and why?