class NoThisSongException(Exception):
    """
    自定义异常类 - 歌曲不存在异常
    继承自Exception类
    """
    def __init__(self, message="请求的歌曲不存在"):
        # 调用父类的构造方法
        super().__init__(message)
        self.message = message
    
    def __str__(self):
        return f"NoThisSongException: {self.message}"

class MusicPlayer:
    """
    音乐播放器类
    """
    
    def __init__(self):
        # 模拟歌曲库
        self.songs = [
            "晴天 - 周杰伦",
            "七里香 - 周杰伦", 
            "青花瓷 - 周杰伦",
            "简单爱 - 周杰伦",
            "夜曲 - 周杰伦",
            "以父之名 - 周杰伦",
            "双截棍 - 周杰伦",
            "稻香 - 周杰伦",
            "告白气球 - 周杰伦",
            "mojito - 周杰伦"
        ]
    
    def play(self, index):
        """
        播放指定索引的歌曲
        
        Args:
            index: 歌曲索引 (从1开始)
            
        Raises:
            NoThisSongException: 当索引超出范围时抛出
        """
        # 参数验证
        if not isinstance(index, int):
            raise ValueError("索引必须是整数")
        
        # 检查索引是否有效
        if index > len(self.songs) or index <= 0:
            raise NoThisSongException(f"歌曲索引 {index} 不存在，当前共有 {len(self.songs)} 首歌曲")
        
        # 模拟播放歌曲
        song_name = self.songs[index - 1]
        return f"🎵 正在播放: {song_name} 🎵"
    
    def display_playlist(self):
        """显示播放列表"""
        print("当前播放列表:")
        for i, song in enumerate(self.songs, 1):
            print(f"{i:2d}. {song}")

def main():
    player = MusicPlayer()
    
    print("🎧 欢迎使用音乐播放器 🎧")
    player.display_playlist()
    print("\n" + "="*40 + "\n")
    
    # 测试用例
    test_indices = [1, 5, 11, -1, 8, 15]
    
    for index in test_indices:
        try:
            print(f"尝试播放索引为 {index} 的歌曲...")
            result = player.play(index)
            print(result)
            
        except NoThisSongException as e:
            print(f"❌ 异常处理: {e}")
            print("💡 提示: 您播放的歌曲不存在")
            
        except ValueError as e:
            print(f"❌ 参数错误: {e}")
            
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            
        finally:
            print("-" * 30)

if __name__ == "__main__":
    main()