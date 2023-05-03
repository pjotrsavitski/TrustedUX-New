# TrustedUX-New

## Docker

Below are a rather simplified instructions for getting the service running in Docker containers for evaluation purposes.
The solution is based on [Quickstart: Compose and Django](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django/)
tutorial with several simplifications.

1. Command `docker compose up -d` should be used to start the containers.
2. Create a superuser account by running
`docker compose exec web python manage.py createsuperuser --username admin --email admin@loclahost` and providing the
password for that `admin` user account.
3. Visit http://localhost:8000 to access the service and http://localhost:8000/admin to access the administration
interface.
  - It might be useful to replace the domain name for `example.com` site with `localhost:8000` at
http://localhost:8000/admin/sites/site/. This will allow the generated URL addresses to be correct (this affects the
survey URL and possible sent email messages).

**NB! The service will not have the email sending configured properly, which means that any self-created new local user
accounts would need to be activated manually. Authentication with Google will also not work without providing proper
configuration.**