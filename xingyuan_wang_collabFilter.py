import sys
import math
import operator

# read command parameter
inputfile = open(sys.argv[1], 'r')
User = sys.argv[2]
Movie = sys.argv[3]
K = int(sys.argv[4])

# construct file dictionary
users = {}
for line in inputfile:
    record = line.rstrip('\n').split('\t')
    if(users.has_key(record[0]) == False):
        users.setdefault(record[0], {})
    users.get(record[0]).setdefault(record[2], float(record[1]))


# calculate the pearson correlation between 2 users
def pearson_correlation(user1, user2):

    # average rating for 2 users, include all the user's ratings
    r1 = 0
    for i in user1:
        r1 = r1 + user1.get(i)
    r1 = r1/float(len(user1))

    r2 = 0
    for i in user2:
        r2 = r2 + user2.get(i)
    r2 = r2/float(len(user2))


    # calculate number & denominator with co-ralated items
    number = 0
    denominator1 = 0
    denominator2 = 0

    for i in user1:
        if(user2.has_key(i)):
            number = number + (user1.get(i)-r1) * (user2.get(i)-r2)
            denominator1 = denominator1 + (user1.get(i)-r1)**2
            denominator2 = denominator2 + (user2.get(i)-r2)**2

    # pearson correlation
    if((float(denominator1)==0.0) & (float(denominator2)==0.0)):
        return 0.0
    
    w = number / float(math.sqrt(denominator1) * math.sqrt(denominator2))    
    return w

#user1 = {1:1,2:2}
#user2 = {3:4,5:6}
#print pearson_correlation(user1, user2)

# calculate the k nearest neighbors of user1 based on pearson similarity
def K_nearest_neighbors(user1, k):

    # calculate all similarities
    correlation = {}    
    for u in users:
        if(cmp(user1, users.get(u)) != 0):
            correlation.setdefault(u, pearson_correlation(users.get(u), user1))

    sorted_correlation = sorted(correlation.items(), key=operator.itemgetter(0))
    sorted_correlation = sorted(correlation.items(), key=operator.itemgetter(1), reverse = True)

    # find the nearest k neighbors
    k_near = {}
    n = 0
    for i in sorted_correlation:
        if(n >= k):
            break
        k_near.setdefault(i[0], i[1])
        n = n+1

    return k_near



# calculate the final prediction for item for user1 using k nearest neighbors
def Predict(user1, item, k_nearest_neighbors):

    number = 0
    denominator = 0
    for u in k_nearest_neighbors:
        if(users.get(u).has_key(item)):
            number = number + k_nearest_neighbors.get(u)* users.get(u).get(item)
            denominator = denominator + k_nearest_neighbors.get(u)

    if(float(denominator) == 0.0):
        return 0
    rating = number / float(denominator)
    return rating


# print output
k_nearest_neighbors = K_nearest_neighbors(users.get(User), K)

sorted_neighbors = sorted(k_nearest_neighbors.items(), key=operator.itemgetter(0), reverse = True)
sorted_neighbors = sorted(k_nearest_neighbors.items(), key=operator.itemgetter(1), reverse = True)

for n in sorted_neighbors:
    print n[0] + ' ' + str(n[1])

print '\n'
print Predict(users.get(User), Movie, k_nearest_neighbors)



# Python xingyuan_wang_collabFilter.py ratings-dataset.tsv Kluver "The Fugitive" 10
# Python xingyuan_wang_collabFilter.py ratings-dataset.tsv Kluver Twister 10
# Python xingyuan_wang_collabFilter.py ratings-dataset.tsv "What makes you think I'm not?" "Schindler's List" 5
