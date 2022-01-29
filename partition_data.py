import os
import random
import pprint as pprint

dir = './data/'

data_dir = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

random.shuffle(data_dir)

size = len(data_dir)

test_set = data_dir[size-(size//10)*2:size-(size//10)]
val_set = data_dir[size-(size//10):]
data_dir = data_dir[:size-(size//10)*2]

print(size)
print(len(data_dir))
print(len(test_set))
print(len(val_set))

for match in data_dir:
    os.rename(dir+match, dir+'training/'+match)

for match in test_set:
    os.rename(dir+match, dir+'test/'+match)

for match in val_set:
    os.rename(dir+match, dir+'validation/'+match)
