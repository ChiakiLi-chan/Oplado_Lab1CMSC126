# application_layer.py

class ApplicationLayer:
    def create_http_request(self, method, url, body=""):
        """Creates a simple HTTP-like request."""
        request = f"{method} {url} HTTP/1.1\nHost: localhost\n\n{body}"
        print(request)  # DEBUG: Show request
        return request.encode()

    def parse_http_request(self, request):
        """Parses an HTTP-like request."""
        try:
            request = request.decode()
            lines = request.split("\n")
            method, url, _ = lines[0].split()
            body = "\n".join(lines[2:])
            return method, url, body
        except Exception as e:
            print(f"[Application Layer] Error parsing request: {e}")
            return None, None, None

    def create_http_response(self, body):
        """Creates an HTTP-like response."""
        response = f"HTTP/1.1 200 OK\nContent-Length: {len(body)}\n\n{body}"
        return response.encode()

    def parse_http_response(self, response):
        """Parses an HTTP-like response."""
        try:
            response = response.decode()
            _, status, _ = response.split("\n")[0].split(" ", 2)
            body = "\n".join(response.split("\n")[2:])
            return status, body
        except Exception as e:
            print(f"[Application Layer] Error parsing response: {e}")
            return None, None
