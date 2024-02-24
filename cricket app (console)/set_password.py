class Password:
    def __init__(self):
        self.code = None

    def set_code(self, code):
        self.code = code

    def get_code(self):
        return self.code

file_path = "password.txt"

with open(file_path, 'r') as file:
    # Read the first line from the file and remove any leading or trailing whitespace
    line = file.readline().strip()

# Create an instance of the Password class
code = Password()

# Set the code using the value read from the file
code.set_code(line)

