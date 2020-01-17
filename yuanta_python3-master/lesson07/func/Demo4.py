def make_pretty(func):
    def inner():
        print("穿鞋子")
        func()
    return inner

def make_pretty2(func):
    def inner():
        print("戴帽子")
        func()
    return inner

# @make_pretty
# @make_pretty2
def ordinary():
    print("John 出門了")

ordinary() #無裝飾
print()
pretty = make_pretty(ordinary) #裝飾
pretty()

def div_args_confirm(func):
    def inner(a,b):
        if b == 0:
            return
        return func(a,b)
    return inner

@div_args_confirm
def div(a,b):
    return a/b

print(div(2,5))
print(div(2,0))
