import pygame

victory_tile = pygame.Vector2(10, 10)

def GenerateFlagText(x, y):
    key = x + y*20
    encoded = "\xa5\xb7\xbe\xb1\xbd\xbf\xb7\x8d\xa6\xbd\x8d\xe3\xe3\x92\xb4\xbe\xb3\xa0\xb7\xff\xbd\xbc\xfc\xb1\xbd\xbf"
    return ''.join([chr(ord(c) ^ key) for c in encoded])

def main():
    flag_text = GenerateFlagText(int(victory_tile.x), int(victory_tile.y))
    print(flag_text)

if __name__ == "__main__":
    main()