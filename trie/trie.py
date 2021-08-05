from init.helper_functions import fix_word
from trie.trie_node import TrieNode


class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        self.root = TrieNode("")

    def insert(self, word, sentence_number, index, path):
        word = fix_word(word)
        """Insert a word into the trie"""
        node = self.root
        is_exist = True
        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for char in word:
            if char in node.children:
                node = node.children[char]
                is_exist = True
            else:
                # If a character is not found,
                # create a new node in the trie
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
                is_exist = False

        # Mark the end of a word
        if is_exist:
            node.is_end.update({(path, sentence_number): index})
        else:
            node.is_end[(path, sentence_number)] = index

        # Increment the counter to indicate that we see this word once more
        node.counter += 1

    def dfs(self, node, prefix):
        """Depth-first traversal of the trie

        Args:
            - node: the node to start with
            - prefix: the current prefix, for tracing a
                word while traversing the trie
        """
        if node.is_end:
            self.output.update(node.is_end)
            # self.output.append((prefix + node.char, node.counter,node.is_end))

        for child in node.children.values():
            self.dfs(child, prefix + node.char)

    def prefix_query(self, x, flag=0, letter=""):
        """Given an input (a prefix), retrieve all words stored in
        the trie with that prefix, sort the words by the number of
        times they have been inserted
        """
        # Use a variable within the class to keep all possible outputs
        # As there can be more than one word with such prefix
        self.output = {}
        node = self.root
        # can_replace = True
        # Check if the prefix is in the trie
        for char in x:
            if char == "~" and flag != 0:
                for child in node.children:
                    if child != letter:
                        self.prefix_query(x.replace("~", child))
                        if len(self.output) >= flag:
                            return self.output
                return self.output
            if char in node.children:
                node = node.children[char]
                # cannot found the prefix, return empty list
            else:
                return {}

        # Traverse the trie to get all candidates
        self.dfs(node, x[:-1])

        # Sort the results in reverse order and return
        # return sorted(self.output, key=lambda x: x[1], reverse=True)
        return self.output

    def word_query(self, x, flag=0, letter=""):
        """Given an input (a word), retrieve the is_end dictionary"""
        node = self.root
        # Check if the prefix is in the trie
        for char in x:
            if char == "~" and flag != 0:
                ret_dict = {}
                for child in node.children:
                    ret_dict.update(self.word_query(x.replace("~", child)))
                    if len(ret_dict) >= flag:
                        return ret_dict
                return ret_dict
            if char in node.children:
                node = node.children[char]
            else:
                # cannot found the prefix, return empty list
                return {}
        if node.is_end:
            return node.is_end
        return {}

    def __str__(self):
        s = ""
        node = self.root
        for c in node.children:
            s += str(c)

        return s
