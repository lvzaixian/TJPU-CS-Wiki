class NoThisSoundException(Exception):
    pass


def play(index):
    if index > 10:
        raise NoThisSoundException
    print("正在播放歌曲")


try:
    play(122)
except NoThisSoundException:
    print("您播放的歌曲不存在")
