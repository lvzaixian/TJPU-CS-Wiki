class Pet:
    nickName=''
    health=0
    def __init__(self,n,h):
        self.nickName=n
        self.health=h

    def show(self):
        print('宠物的昵称为%s,健康值为%d'%(self.nickName,self.health))

class Dog(Pet):
    color=''
    def __init__(self,n,h,c):
        Pet.__init__(self,n,h)
        self.color=c
    def show(self):
          print('宠物的昵称为%s,健康值为%d,颜色为%s'%(self.nickName,self.health,self.color))

    def feed(self):
        self.health+=5

if   __name__=='__main__':
    d=Dog('毛毛', 5, '黑色')
    d.feed()
    d.show()
