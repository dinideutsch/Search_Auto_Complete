from init.helper_functions import fixed_list
from collections import deque
from pathlib import Path


def tree_tour(directory, trie):
    p = Path(directory)
    queue = deque()
    queue.append(p)
    """go over the directory, if file- func(file) else insert to queue and continue moving"""
    while queue:
        p = queue.popleft()
        dirs = [x for x in p.iterdir() if x.is_dir()]
        for dr in dirs:
            queue.append(dr)
        for fle in p.iterdir():
            if fle.is_file():
                file_handler(str(fle), trie)


def file_handler(file, trie):
    lines = []
    # try:
    with open(file,encoding="utf8") as f:

            lines = f.readlines()
    # except:
    #     print("EOFException")

    for i in range(len(lines)):
        sentence_handler(lines[i].replace("\n", ""), file, i + 1, trie)


def sentence_handler(sentence, path, sentence_number, trie):
    """parse the sentence and insert every word to the trie"""
    index = 0
    parse_sen = fixed_list(sentence)
    if parse_sen != ['']:
        for word in parse_sen:
            trie.insert(fix_word(word.lower()), sentence_number, index, path)
            index += 1


def fix_word(word):
    w = ""
    for c in word.lower():
        if 'a' <= c <= 'z':
            w += c
    return w
