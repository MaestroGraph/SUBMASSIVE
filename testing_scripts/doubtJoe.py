# this file is to test that there are nested equivalence classes in Joe's file.

import csv
import time
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
        self.index_to_list = {}
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
                if '^^' in class_name_string:
                    class_name_string = class_name_string.split('^^')
                    class_name_string = str(class_name_string[0][1:-1])

                # print(line)
                # print('name:', class_name_string, '\nindex:', num, '\n')

                # print ('type',type(class_name_string))
                if class_name_string in self.class_name_to_index.keys():
                    self.class_name_to_index[class_name_string].append(num)
                else:
                    self.class_name_to_index[class_name_string] = [num]
                # print (self.class_name_to_index)
                if (num in self.index_to_list.keys()):
                    self.index_to_list[num].append(class_name_string)
                else:
                    self.index_to_list[num] = [class_name_string]
                # print ('index to list = ', self.index_to_list[num])
                # print(class_name_string, num)
                line = f.readline()
                cnt += 1
        print ('There are in total {:,} groups'.format(len(self.index_to_list.keys())))
        # print (self.class_name_to_index.keys())
        print ('There are in total {:,} classes'.format(len(self.class_name_to_index.keys())))

            # print("DONE! Finished reading file TERM2ID. There is a total of ", "{:,}".format(cnt), "terms")

    def obtain_group_id (self, t):
        if t in self.class_name_to_index.keys():
            return self.class_name_to_index[t]
        else:
            return -1

if __name__ == "__main__":

    start = time.time()
    # ==============

    e = equiClassManager(file_name)
    # for i in range(100):
    #     k = list(e.index_to_list.keys())[i]
    #     print ('for group index ', k, ' its members are: ', e.index_to_list[k])
    #     for m in  e.index_to_list[k]:
    #         print ('the index is ', e.class_name_to_index[m])

    # print ('TEST: ', e.class_name_to_index['ttp://hub.culturegraph.org/about/BVB-BV00573755'])
    count = 0
    for n in e.class_name_to_index.keys():
        # print all those who appear in multiple equivalence classes.
        if (len(e.class_name_to_index[n]) > 1):
            count +=1
            # if count %10 == 0:
            #     print (n, '\n\t has index: ', e.class_name_to_index[n])
            #     for i in e.class_name_to_index[n]:
            #         print('equivalence group', i, 'has classes', e.index_to_list[i])

    print ('there are in total {} classes that appear in multiple equivalence (nested) classes.'.format(count))

    # ===============
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Time taken: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
