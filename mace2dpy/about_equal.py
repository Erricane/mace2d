
def about_equal(a ,b):
    eps = 2.0 ** -50  # 50 bits of precision
    eps = eps * abs(a) if abs(a) > abs(b) else eps * abs(b)
    return abs(a-b) <= eps
    