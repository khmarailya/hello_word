"""
Hello, world!))
"""
import sys
import time


class HelloWorld:
    HELLO_WORD = 'Hello, word!'
    HELLO_WORLD = 'Hello, world!))'

    DRAMATIC_PAUSE = .5
    PRINT_PAUSE = .2
    CNT_TO_ERASE = 2

    @classmethod
    def print(cls, chars: str):
        for s in chars:
            sys.stdout.write(s)
            sys.stdout.flush()
            time.sleep(cls.PRINT_PAUSE)

    @classmethod
    def erase(cls, chars: str, cnt_to_erase: int):
        for i in range(cnt_to_erase + 1):
            print('\r', end='')
            print(chars[:-i], end='')
            time.sleep(cls.PRINT_PAUSE)

    @classmethod
    def main(cls):
        cls.print(cls.HELLO_WORD)
        time.sleep(cls.DRAMATIC_PAUSE)
        cls.erase(cls.HELLO_WORD, cls.CNT_TO_ERASE)
        time.sleep(cls.DRAMATIC_PAUSE)
        cls.print(cls.HELLO_WORLD[len(cls.HELLO_WORD) - cls.CNT_TO_ERASE:])


if __name__ == '__main__':
    HelloWorld.main()
