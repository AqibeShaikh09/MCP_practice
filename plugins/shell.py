import subprocess

def run(params):
    command = params.get("command")
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return {
            "tool": "shell",
            "result": output.decode().strip()
        }
    except subprocess.CalledProcessError as e:
        return {
            "tool": "shell",
            "error": e.output.decode().strip()
        }
