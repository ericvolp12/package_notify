import pigpio
from http.server import BaseHTTPRequestHandler, HTTPServer

# Tracks the number of packages waiting to be picked up
pending_package_count = 0

pi = pigpio.pi()
pin = {
    'red': 17,
    'green': 22,
    'blue': 24
}


def set_all_pins(val):
    pi.set_PWM_dutycycle(pin.red, val)
    pi.set_PWM_dutycycle(pin.green, val)
    pi.set_PWM_dutycycle(pin.blue, val)


# HTTPRequestHandler class
class TestHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):

        global pending_package_count
        # Return inits
        message = "That was an invalid request!"
        response_code = 404

        path = self.path[1::]

        if path == "released_package":
            print("Package was released!\n")
            response_code = 200
            pending_package_count -= 1
            message = "Package was released!<br>Total pending packages: " + str(pending_package_count)
            if pending_package_count <= 0:
                set_all_pins(0)

        elif path == "new_package":
            print("New package was received!\n")
            response_code = 200
            pending_package_count += 1
            message = "New package was received!<br>Total pending packages: " + str(pending_package_count)
            if pending_package_count == 1:
                set_all_pins(100)
            elif pending_package_count == 2:
                set_all_pins(150)
            elif pending_package_count == 3:
                set_all_pins(200)
            elif pending_package_count > 0:
                set_all_pins(255)

        self.send_response(response_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 88888)
    httpd = HTTPServer(server_address, TestHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()


