names = [ "Dave", "Mark", "Ann", "Phil" ]
a = names[2]
print (a)
names[0] = "Jeff"
print (names)
print (len(names))
names.append("Kate")
print (names)
names.insert(2, "Sydney")
print (names)
print(names[0:2])
print(names[2:])
names[1] = 'Jeff'
print (names)
names[0:2] = ['Dave','Mark','Jeff'] 
print (names)
a = [1,2,3] + [4,5]
print (a)
a = [1,"Dave",3.14, ["Mark", 7, 9, [100,101]], 10]
print(a[1])
print(a[3][2])
print(a[3][3][1])