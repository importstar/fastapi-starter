from api_app import controllers


def main():
    server = controllers.create_server()
    server.run()
