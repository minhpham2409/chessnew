class aaa:
    def __init__(self):
        self.x = 3

    def __printt(self):
        print(self.x)


class xxx(aaa):
    def __init__(self):
        super().__init__()

    def h(self):
        self.__printt()


x = xxx()
x.h()
