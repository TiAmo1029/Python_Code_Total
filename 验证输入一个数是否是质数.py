def v1(n):

    if n <= 1:
        return False
    for i in range(2,n):
        if n % i == 0:
            return False

    return True

print(f"97是质数吗？{v1(97)}")