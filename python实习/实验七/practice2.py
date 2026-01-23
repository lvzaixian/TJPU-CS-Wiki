class Pet:
    def __init__(self, nickName, health):
        self.nickName = nickName
        self.health = health

    def show(self):
        print(f"宠物昵称：{self.nickName}，健康值：{self.health}")


class Dog(Pet):
    def __init__(self, nickName, health, color):
        super().__init__(nickName, health)
        self.color = color

    def show(self):
        print(f"宠物昵称：{self.nickName}，健康值：{self.health}，颜色：{self.color}")

    def feed(self):
        self.health += 5
        print(f"{self.nickName} 被喂食，健康值+5，当前健康值：{self.health}")


# 测试代码
if __name__ == "__main__":
    d = Dog("毛毛", 5, "黑色")
    d.feed()
    d.show()