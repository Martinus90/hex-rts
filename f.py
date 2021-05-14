class File:
    def __init__(self, file):
        self.file = file
        self.a = None
        self.variable = None
        with open(self.file, 'r') as reader:
        # Read & print the first 5 characters of the line 5 times
            self.a = reader.readlines()
            print(self.a[0])

    def write(self, variable):
        self.variable = variable
        self.a[0] = str(self.variable)
        with open(self.file, 'w') as writer:
        # Read & print the first 5 characters of the line 5 times
            writer.writelines(self.a)
            print(self.a)

a = File('data.txt')
a.write(36)
