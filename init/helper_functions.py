def fixed_list(arr):
    joined_word = " ".join(arr.split())
    arr = joined_word.split(' ')
    return arr

def fix_word(word):
    w = ""
    for c in word.lower():
        if 'a' <= c <= 'z':
            w += c
    return w
