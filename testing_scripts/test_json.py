#test input output Python
import json

cycle_samples = []

cycle_samples.append([(1,2), (3,4), (9,8)])
cycle_samples.append([(2,3), (4,5), (1,8), (9,4)])

with open('cycle_samples.txt', 'w') as outfile:
    json.dump(cycle_samples, outfile)

with open('cycle_samples.txt') as json_file:
    data = json.load(json_file)
    (l, r) = data[0][0]
    print (l)
    print (r)
