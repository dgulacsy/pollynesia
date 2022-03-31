# Pollynesia

Pollynesia is a web application for creating polls of various kind. It is based on the Django framework.

## Setup
1. Clone this GitHub repository
2. Install Docker
3. Go to the cloned repository (the directory where the Dockerfile is), create a `.env` file 
4. Add your IPstack API key and save.
  ```
  IPSTACK_API_KEY=YOUR_API_KEY
  ```
5. Open a terminal and run `docker compose up`
6. Attach a shell to the created pollynesa_web container
7. Run `python manage.py makemigrations`
8. Run `python manage.py migrate`

By now your Django server should be up and running on http://0.0.0.0:8000/.
