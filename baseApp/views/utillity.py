import random, string

def randomString():
    """
    ランダムな文字列を作成
    """
    randomText = random.choice(string.ascii_letters + string.digits)
    return randomText

def randomNumver(length):
    """
    ランダムな数列を作成
    """
    digits = ''.join(random.choices(string.digits, k=length))
    return digits