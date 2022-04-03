# Authentication and Authorization

## Questions

There are a few questions that will help us decide on a good approach.

### Will scientific users be allowed to access the system directly?

If a scientific user will be accessing the system directly (either reading or updating their information), we will
definitely want to authenticate on a per-user basis. This will allow us to keep detailed logs of which users are
accessing which data. It will also allow us to do very granular authorization (for example, perhaps a user can only view
their own data).

However, if this system is more of a integration service that syncs data from other services, such as the email system,
training system, etc., then we may want to authenticate on a "service" level, instead of per-user. Service
authentication would probably be through pre-shared API keys, or if all systems were running in the same kubernetes or
cloud environment, I would look at things like Service Accounts or Workload Identity for authentication. Then, we could
use an IAM tool to manage the authorization of which services are allowed to communicate with other services.

### Admin access

How do we want to give our team access to the system, to troubleshoot or correct errors? If we adopt a per-user
authentication schema, we could create special accounts for us, or give our own accounts additional
"superuser" permissions. If we do not have per-user authentication, or even if we do, we might decide that we don't want
to create special accounts with lots of permission for the public APIs. Instead, we might want to keep the public APIs
limited, and then access the system in a different way: perhaps through ssh and running python shell commands, or even
VPN and accessing the underlying databases directly. While this might seem more secure, it also comes with the downside
of our admin users having very powerful shell access or direct DB access, which will much more challenging to audit and
manage.

### Granularity of permissions

Even if we want to allow users to update some of their own data (e.x. email addresses), we probably do not want to allow
them to update all fields. For example, I assume that the training system should be responsible for pushing an update to
us when the user completes their training (or it expires). We do not want a user to be able to just mark their training
up to date through a request. Similary, we probably want fields like "last_account_activity" to be read only, and
managed by the system based on updates to other fields.

To achieve this, if allowing per-user authentication, we will need authorization to be specified very granularly at the
field level,
(e.x. Users can modify field "eppns" on their own User object), it cannot just be specified on the object (User can
modify their own User object)

### What external systems will we need to sync with

For example, will our system be responsible for managing usernames and passwords for logins to physical servers? Will we
need to implement Single Sign On, LDAP, or OAuth for other tools that the scientific user will expect to access with the
same account? If so, I would probably try to choose our internal authentication scheme to work the best with the most
complex of these integrations.

## Implementation ideas

My instinct is to support both per-user password based authentication and "system to system" authentication. This will
allow for most users to self-service manage small changes (e.x. name updates, adding an email address). It will also
allow for relatively simple integration with other services. We will need to create a fair number of authorization
helper functions / libraries for our internal code to support mixing both types.

### Per-User authentication

A simple way to manage per-user authentication could be the User management built into
Django (https://docs.djangoproject.com/en/4.0/topics/auth/). While this defaults to session based authentication, we
could modify it to use a different approach such as JWTs.

Some pros with this approach:

- A good selection of libraries to enable additional security functionality - session timeout, etc.
- I think we could migrate to using an LDAP as the source of truth for user
  accounts (https://django-auth-ldap.readthedocs.io/en/latest/) if needed without needing our downstream clients to make
  significant changes

A few downsides to this approach:

- Since we are not currently using the django Model framework (instead using mongoengine Documents), we won't be able to
  fully take advantage of the granular authorization permissions available with that framework

### System to System authentication

I would first try to use something with as few managed keys as possible. For example, if all systems were running inside
of Google Cloud, we could use their Workload Identity, Service Accounts, and IAM systems to identify which service is
calling the other service.

If we are not all within a single system, we might need to do something more basic like shared API keys. If we did this,
I would try to find a solution that allowed for easy auditing of key usage, and easy key rotation. For example, we might
be able to store the keys inside of a Vault (https://www.vaultproject.io/), if we are able to modify all the clients to
fetch their keys from Vault first.

We may however, have some legacy clients where we have little control of how they can call our system. We might have to
use a basic key as part of the HTTP headers, or even the URL to authenticate.

### Authorization

Once we know who is making the request, determining whether the user is allowed to make the change or access the data
will still be very complex. It would be advantageous for us if we could be very consistent at a high level. For example,
if a user is allowed to modify all of the data in their User object in the database, we only need to check whether they
are attempting to modify their object, we don't need to verify which fields they are trying to modify.

To achieve this simpler approach, we would probably need to split our user information up into multiple objects in the
database/datastore. In this example, we might store the training status separately from the user profile (emails and
names). We could then allow users to modify their profile but not their training status. And, we could allow the
training system
"system to system" api key to modify user training statuses for all users.

I would love for there to be easy libraries to implement this granular authorization, but from some brief research, I
believe this would require custom integration with our data objects, through Mongoengine, or Django models, etc.

When implementing this custom work, we should definitely try to build a system based on Role Based Access Control (RBAC)
. By implementing a hierarchy / grouping of users into roles, and then only assigning permissions to the role, we
simplify the work we need to do verifying user permissions and access levels. We also hopefully simplify our code, as
the role assignment may be able to handle some complex permission hierarchies.

# Thoughts on my approach

## python

I stuck with python as I've been working with it almost exclusively for the past few years. For GraphQL, I might look at
implementing the backend with NodeJS / Typescript instead, as the official GraphQL documentation seems to prefer that.

## Django as the python framework

I chose Django as my python framework because I'm familiar with it and it seemed to be strongly supported by Strawberry.

Cons:

- This current example is hardly using any Django features, especially because we chose Mongoengine instead of Djongo.
  If we end up using this service to manage our user accounts, I think Django will be very helpful. If we instead
  delegate the user accounts to an external service like Okta, we might find that most of the Django tooling is
  unecessary.

## Which mongo library to use?

I chose MongoEngine because it had more stars/follows on github, and seemed to more directly map to Mongo without Django
getting in the way. However, it might not be the best choice in a Django app, as their own docs seem to actually suggest
using Djongo (see http://docs.mongoengine.org/django.html and https://github.com/MongoEngine/django-mongoengine). From
my brief time working with Mongoengine, I feel it met my expectations, and documentation and StackOverflow support was
fairly good.

## Using Mongo as the database

I'm not sure we are really taking advantage of Mongo with this use case. Something simpler and more integrated with
Django might give us more benefits, for example field level authorization, and better integration with a Django admin
page if we need admin accounts.

On the other hand, I didn't run into any issues caused by the choice of Mongo. Since I had never used Mongo before,
there was definitely a learning curve to initial set up, but I think coming into an existing codebase with it working
with Mongoengine, it would be pretty fast to get up to speed.

I think there will be less documentation and self-help support (StackOverflow) for any python mongo integration than
there would be for a regular database with Django.

If we stuck with python and Django, I would probably prefer a Postgres or MySQL database over Mongo, as I feel it should
be simpler to manage and maintain than a Mongo deployment. However, if we ended up going with a different python
framework such as flask, I know that the database integration needs much more hand holding, so I would see more benefit
from Mongo. If we went with NodeJS instead of python, I wouldn't be surprised to find that Mongo was actually a much
easier choice than a traditional SQL database.

## Which Graphql library to use

After working with Strawberry, I observed the following

Pros:

- I really enjoyed the fact that the python code looks fairly similar to the GraphQL schema. I think leveraging python
  type hints helps simplify things.

Cons:

- The documentation is fairly limited and simplistic. For example, they do not have any resolvers showing how to link
  objects to other objects. Their Mutations example is also very limited. Since these are really core concepts to
  GraphQL, I would have liked to see more thorough examples. I felt this slowed me down when trying to use the framework
  the first time
- Autocomplete for the strawberry libraries was not working nicely in my PyCharm, I'm not sure why.

## GraphQL

If our service is the source of truth for accounts and resource management, I think it will probably need to be
integrated with many other systems. This means we probably will not be able to only support GraphQL, we'll also have to
support more traditional REST apis, and will likely need to support some standard protocols (e.x. LDAP).

I definitely question whether the additional learning curve of GraphQL is worth it for this service. Will our clients be
different enough from each other that they want different fields from the same Query, or would they be better served by
having different REST APIs?

Pros:

- I like that you are forced to define your api schema. If we used a statically typed language like Typescript or Java
  for this system, we might even get additional benefits from build time checking of our implementation code against the
  schema. There are REST frameworks that also require defining an api schema (e.x. OpenAPI spec), so I don't see this as
  a huge win for GraphQL

Cons:

- It will be harder for a teammate who has not used GraphQL before to onboard, and it will be easier for them to
  accidentally write suboptimal code
- Since GraphQL is not core to Django, we are reliant on a third party library (like Strawberry) that may lose activity
  and support over time

Neutrals:

- While I think there has been some attempt at establishing GraphQL api
  guidelines (https://graphql-rules.com/rules/mutation-business-operations), it has the same struggles as REST, where
  different groups will utimately have their own guidelines.

## Code style choices

### Having a separate mongo document definition from the graphql schema?

In general, I prefer to keep a layer between the API and the database, so that we can do things like deprecate API
fields without removing them from the database, or add new DB fields without exposing them in the API.  
Pros

- Updating graphql doesn't affect MongoDB schema
- Updating MongoDB doesn't affect GraphQL schema
- If we changed our mind about MongoDB, or moved some components out of Mongo, we wouldn't need to update GraphQL

Cons

- There is definitely some duplication between `accounts/documents.py` and `api_graphql/schema.py`, and the opportunity
  for typos
- It will make it more challenging to reap all the benefits of graphql, such as only fetching the fields asked for in
  the query. While I think it would be possible, (we could pass the subset of fields to
  Mongo http://docs.mongoengine.org/guide/querying.html#retrieving-a-subset-of-fields, probably using the "Info" from
  strawberry https://strawberry.rocks/docs/types/resolvers#api), it would require some complicated plumbing code

## Problem statement

- A giant mutation that is able to edit any of the fields on User might be an antipattern
  https://graphql-rules.com/rules/mutation-business-operations
  (this guide was linked from strawberry docs)
- It seems weird that we would want to allow updates to *any* field, we probably don't want to allow updates to
  the `uid` or `uidNumber` fields, if they are our unique identifiers.

# Todos

To actually be ready for production deployment, there are a bunch of further steps that I didn't have time for,
including

* separate settings.py into development and production files
* add unit tests
* cleanup repository to have a cleaner application added to Docker image without readmes, initial data, etc.
* cleanup lots of blank files from the Django template
* gunicorn strongly suggests running behind a load balancer like nginx


