### Which mongo library to use?

Chose MongoEngine because it had more stars/follows on github, and seemed the more directly map to Mongo without Django
getting in the way.

Might not be the best choice though http://docs.mongoengine.org/faq.html

### Separate mongo document definition from graphql schema?

In general, I prefer to keep a layer between the API and the database, so that we can do things like deprecate API
fields without removing them from the database, or add new DB fields without exposing them in the API.

### Strawberry

Autocomplete on strawberry not working nicely, not sure why

### Todos

Pass subset of fields to Mongo http://docs.mongoengine.org/guide/querying.html#retrieving-a-subset-of-fields
