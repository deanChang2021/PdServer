

###
##注意，这业务实现方法，只能是方法，不能是类。因为taskQueue中的Task会将数据赋到可变参数中，类的self会接收第一个参数。
##

async def demo(triggerId, type, *args):
    print("this is demo")
    print(triggerId)
    print(type)
    print(args)