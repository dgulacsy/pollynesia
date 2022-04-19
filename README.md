# Pollynesia

Pollynesia is a web application for creating polls of various kind. It is based on the Django framework.

## Setup
1. Clone this GitHub repository
2. Install Docker
3. Create a free IPstack API key at https://ipstack.com/product.
4. Go to the cloned repository (the directory where the Dockerfile is), create a `.env` file
5. Add your IPstack API key and save. (Required to fill in location form field based on the client's IP address)
  ```
  IPSTACK_API_KEY=YOUR_API_KEY
  ```
5. Open a terminal and run `docker compose up`

By now your Django server should be up and running on http://localhost:8000/.
