for a in range(1,100//3 + 1):
     for b in range(1,100//2):
          c = 100 - (a + b)
          # 判断：总共⼀百匹⻢并且⼀百担货
          if a + b + c ==100 and 3*a + 2*b + c/2 == 100:
             print(f'大马{a}匹，中马{b}匹，小马{c}匹。')
