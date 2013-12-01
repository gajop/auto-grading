import subprocess

def run(image, command, *args):
    invocation = ["docker", "run", image, command]
    invocation.extend(list(args))
    return subprocess.check_output(invocation)
