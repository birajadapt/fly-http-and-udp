# HTTP and UDP Server running on same port on Fly.io

We've written a Python file that runs a HTTP server and a UDP server both on the same port (`8080`).

For UDP server on fly.io, there are two important things to note:

1. We need to bind it to `fly-global-services`, NOT localhost. See line 50 in the main.py file.
2. We need to **allocate a dedicated ipv4 address** for the app.

## Steps

1. I've created a fly.toml file in the root directory with the following content:

   ```
   [http_service]
   internal_port = 8080
   force_https = true
   auto_stop_machines = 'suspend'
   auto_start_machines = true
   min_machines_running = 1
   processes = ['app']

   [[services]]
   protocol = 'udp'
   internal_port = 8080

   [[services.ports]]
   port = 8080
   ```

2. Launch the app on Fly.io

   ```
   fly launch --org sahil-manocha-115
   ```

   Note: `fly launch` = Create a new app on Fly.io. Use `fly deploy` to update an existing app.

3. It will ask

   ```
   An existing fly.toml file was found
   ? Would you like to copy its configuration to the new app? (y/N)
   ```

   Type `y` and press enter.

4. It will ask for app's configuration (region, name, etc.). Then it will build the image & push it to the registry.

5. _IMPORTANT_: Then it will ask if we want to allocate a dedicated ipv4 address for the app. **SAY YES**.

   ```
   ? Would you like to allocate a dedicated ipv4 address now? Y
   ```

6. Once it's done, it will show the app's URL.

   ```
   Visit your newly deployed app at https://fly-http-and-udp.fly.dev/
   ```

7. Send HTTP requests to the app's URL.

   ```
   $ curl https://fly-http-and-udp.fly.dev/
   Hello from HTTP server!
   ```

8. Send UDP requests to the app's URL.
   ```
   $ echo "biraj rocks" | nc -u -w 1 fly-http-and-udp.fly.dev 8080
   Received UDP: biraj rocks
   ```
