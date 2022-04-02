### Which mongo library to use?

Chose MongoEngine because it had more stars/follows on github, and seemed the more directly map to Mongo without Django
getting in the way.

Might not be the best choice though http://docs.mongoengine.org/faq.html

### Separate mongo document definition from graphql schema?

In general, I prefer to keep a layer between the API and the database, so that we can do things like deprecate API
fields without removing them from the database, or add new DB fields without exposing them in the API.

### Strawberry

- Autocomplete on strawberry not working nicely, not sure why
- Examples in documentation a little simplistic. For example, no resolvers showing how to link objects to other objects
-

### Problem statement

- A giant mutation to edit any of the fields on User might be an antipattern
  https://graphql-rules.com/rules/mutation-business-operations
  (this guide was linked from strawberry docs)
- It seems weird that we would want to allow updates to *any* field, we probably don't want to allow updates to
  the `uid` or `uidNumber` fields, if they are our unique identifiers.
-

### Todos

To actually be ready for production deployment

* separate settings.py into development and production files
* add unit tests
* cleanup repository to have a cleaner application added to Docker image without readmes, initial data, etc.
* gunicorn strongly suggests running behind a load balancer like nginx

To improve code quality

* Pass subset of fields to Mongo http://docs.mongoengine.org/guide/querying.html#retrieving-a-subset-of-fields, probably
  using the "Info" from strawberry https://strawberry.rocks/docs/types/resolvers#api

