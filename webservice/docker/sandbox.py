import subprocess

import api

class Docker:
    def __init__(self, image):
        self.image = image

    def run(self, command, *args):
        return api.run(self.image, command, *args)

if __name__== '__main__':
    docker = Docker("ubuntu")
    print(docker.run("/bin/echo", "bla bla", "bc"))
