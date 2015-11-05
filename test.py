import sys
import re


# Python test.py ratings-dataset.tsv Kluver 'The Fugitive' 10
# Python test.py ratings-dataset.tsv Kluver Twister 10
# Python collabFilter.py ratings-dataset.tsv "What makes you think I'm not?" "Schindler's List" 10

# print sys.argv




a = ['test.py', 'ratings-dataset.tsv', 'Kluver', "'The", "Fugitive'", '10']
result = []

k = 0
flag = False

for i in sys.argv:
    if re.match(r'\A\'(.*)', i):
        print i
        flag = True
        result.append(re.sub(r'\A\'', '', i))
        k = k+1
        
    elif re.match(r'(.*)\'\Z', i):
        print i
        flag = False
        result[k-1] = result[k-1] + ' ' + re.sub(r'\'\Z', '', i)

    else:
        if(flag == False):
            result.append(i)
            k = k+1
        else:
            result[k-1] = result[k-1] + ' ' + i

print result


print '-------------'
s = "'The"
t = "Fugitive'"

print re.match(r'\A\'(.*)', s)
print re.match(r'(.*)\'\Z', t)

print re.sub(r'\A\'', '', s)
print re.sub(r'\'\Z', '', t)

print '-------------'
pattern = re.compile(r'\A\'(.*)')
match = pattern.match(s)

if match:
    print match.group()
