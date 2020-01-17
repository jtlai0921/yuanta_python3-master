str = 'w=60.0,h=170.0'
print(str)
list = str.split(',')
print(list[0])
print(list[0].split('=')[0])
print(list[0].split('=')[1])
print(list[1])
print(list[1].split('=')[0])
print(list[1].split('=')[1])

x = 'blue,red,green'
a, b, c = x.split(',')
print(a)
print(b)
print(c)

score = "chinese=100;math=90"
score_dict = dict( item.split("=") for item in score.split(";"))
print(score_dict)

