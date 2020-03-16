
import csv

# file_name = "term2id.csv"
# file_name = "term2id_0-99_1000.csv"
file_name = "term2id_0-99.csv"

def splitTermAndID(line):
    parts = line.split(" ")
    if len(parts) ==2:
        return parts
    else:
        # when an element contains an empty space
        term = ""
        for i in range(len(parts) - 1):
            term = term + parts[i]
        return [term, parts[-1]]

class equiClassManager:

    def __init__(self, path):
        # define a path to the equivalent class
        self.file_path = path
        self.class_name_to_index = {}

        with open(file_name) as f:
            line = f.readline()
            if (line == 'TERM,GROUPID\n'):
                line = f.readline()
            cnt = 0
            while line:

                splitted_line = splitTermAndID(line)
                # values
                num = int(splitted_line[1])
                # key
                class_name_string = splitted_line[0]
                self.class_name_to_index[class_name_string] = num

                line = f.readline()
                cnt += 1

    def test_equivalent (self, t1, t2):

        if t1 in self.class_name_to_index.keys() and t2 in self.class_name_to_index.keys():
            return (self.class_name_to_index[t1] == self.class_name_to_index[t2])
            return
        else:
            return False

if __name__ == "__main__":
    e = equiClassManager(file_name)
