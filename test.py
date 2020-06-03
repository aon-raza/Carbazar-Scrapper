import random
universalset = []
setA = []
setB = []
union = []
intersection = []
# 1- create universal set.
for j in range(100):
    rand = random.randint(4, 100)
    if rand not in universalset : universalset.append(rand)
    if len(universalset) == 15:
        break
print("Universal Set:")
print(universalset)

# 2- create set A from universal set.
for j in range(100):
    rand = random.randint(0, 14)
    if universalset[rand] not in setA : setA.append(universalset[rand]);
    if len(setA) == 15:
        break

print("Set A:")
print(setA)

# 3- create set B from universal set.
for j in range(100):
    rand = random.randint(0, 14)
    if universalset[rand] not in setB : setB.append(universalset[rand])
    if len(setB) == 15:
        break

print("Set B:")
print(setB)

# 4- union
for j in range(15):
    union.append(setA[j])
print("union before: ")
print(union)

for x in range(len(setB)):
    rand = setB[x]
    if rand not in union:
        union.append(rand)

print("union after: ")
print(union)

