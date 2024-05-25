import json
import subprocess


class Shortcut:
    """
    Runs a shortcut
    """

    def __init__(self, shortcut_name):
        self.shortcut_name = shortcut_name
        if self.shortcut_name not in self.__get_shortcuts():
            raise Exception("Shortcut not found")

    def __get_shortcuts(self):
        return self.__subprocess_run("shortcuts", "list", return_type="list")

    def run(self, input_data=None, return_type=None):
        return self.__subprocess_run(
            "shortcuts", "run", self.shortcut_name,
            input_data=input_data,
            return_type=return_type
        )

    @staticmethod
    def __subprocess_run(*args, input_data=None, return_type=None):
        result = subprocess.run(args, capture_output=True, text=True, input=input_data)
        if result.returncode != 0:
            print("Error:", result.stderr)
            return []
        else:
            match return_type:
                case "list":
                    return [item for item in result.stdout.split("\n") if len(item) > 0]
                case "json":
                    try:
                        return json.loads(result.stdout)
                    except json.JSONDecodeError:
                        return result.stdout
                case _:
                    data = result.stdout
                    if data == "None":
                        return None
                    return data
