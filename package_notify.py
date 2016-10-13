#!/usr/bin/env python
import pigpio
from http.server import BaseHTTPRequestHandler, HTTPServer



pi = pigpio.pi()
pin = {
    'red': 17,
    'green': 22,
    'blue': 24
}

# Tracks the number of packages waiting to be picked up
pending_package_count = 0


def set_color(color):
    if color == "red":
        set_leds(255, 0, 0)
        return
    elif color == "blue":
        set_leds(0, 255, 0)
        return
    elif color == "green":
        set_leds(0, 0, 255)
        return
    elif color == "purple":
        set_leds(165, 0, 255)
        return
    elif color == "black":
        set_leds(0, 0, 0)
        return
    return


def set_leds(r, g, b):
    pi.set_PWM_dutycycle(pin['red'], r)
    pi.set_PWM_dutycycle(pin['green'], g)
    pi.set_PWM_dutycycle(pin['blue'], b)


# HTTPRequestHandler class
class TestHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):

        global pending_package_count
        # Return inits
        message = "That was an invalid request!"
        response_code = 404

        path = self.path[1::]

        if path == "":
            print("Checking the package queue.")
            response_code = 200
            message = "Pending Packages: " + str(pending_package_count)

        if path == "released_package":
            print("Package was released!\n")
            response_code = 200
            pending_package_count -= 1
            message = "Package was released!<br>Total pending packages: " + str(pending_package_count)
            if pending_package_count == 1:
                set_color("red")
            elif pending_package_count == 2:
                set_color("blue")
            elif pending_package_count == 3:
                set_color("green")
            elif pending_package_count > 3:
                set_color("purple")
            elif pending_package_count <= 0:
                set_color("black")

        elif path == "new_package":
            print("New package was received!\n")
            response_code = 200
            pending_package_count += 1
            message = "New package was received!<br>Total pending packages: " + str(pending_package_count)
            if pending_package_count == 1:
                set_color("red")
            elif pending_package_count == 2:
                set_color("blue")
            elif pending_package_count == 3:
                set_color("green")
            elif pending_package_count > 0:
                set_color("purple")

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
    server_address = ('192.168.1.47', 25500)
    httpd = HTTPServer(server_address, TestHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()


