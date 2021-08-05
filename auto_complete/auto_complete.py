import pickle

from auto_complete.auto_complete_data import AutoCompleteData
from init.helper_functions import fixed_list
from trie.trie import Trie
import linecache
from init.init import tree_tour


class AutoComplete:
    """This class gets a sequence, and return five matching completions"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not AutoComplete.__instance:
            AutoComplete.__instance = object.__new__(cls)
        return AutoComplete.__instance

    def __init__(self, seq):
        self.trie = Trie()
        self.creator_options = {
            "level_1": self.get_completions,
            "level_2": self.second_level_score,
            "level_3": self.third_level_score,
            "level_4": self.fourth_level_score,
            "level_5": self.fifth_level_score,
            "level_6": self.sixth_level_score,
            "level_7": self.seventh_level_score,
            "level_8": self.eighth_level_score,
            "level_9": self.ninth_level_score

        }
        self.inter_dict = {}

    def search_seq(self, prefix, flag, letter=""):
        words = fixed_list(prefix)
        if len(words) == 1:
            self.inter_dict = self.trie.prefix_query(words[0], flag, letter)
        else:
            self.inter_dict = self.trie.word_query(words[0], flag, letter)
            for i in range(1, len(words) - 1):
                self.intersect_dictionaries(self.trie.word_query(words[i], flag, letter))
            self.intersect_dictionaries(self.trie.prefix_query(words[-1], flag, letter))

    def intersect_dictionaries(self, dict_2):
        temp_dict = {}
        if not self.inter_dict:
            return
        for key in list(self.inter_dict.keys()):
            if key in dict_2:
                if dict_2[key] == self.inter_dict[key] + 1:
                    temp_dict[key] = dict_2[key]
        self.inter_dict = temp_dict

    def get_sequences(self, prefix, score):
        counter = 0
        ret_array = []
        if not self.inter_dict:
            return []
        for key in self.inter_dict.keys():
            ret_array.append(
                AutoCompleteData(linecache.getline(key[0], key[1]).strip(" "), key[0], self.inter_dict[key],
                                 len(prefix) * 2 + score))
            counter += 1
            if counter == 5:
                break

        return ret_array

    def ingestion(self, resources, data_file):
        tree_tour(resources, self.trie)
        trie = self.trie
        with open(data_file, 'wb') as f:
            pickle.dump(trie, f)

    def get_best_k_completions(self,trie, prefix, data_file):
        self.trie = trie
        completions = self.creator_options["level_1"](prefix, 0)
        level = 2
        while len(completions) < 5 and level < 10:
            completions += self.creator_options[f"level_{level}"](prefix, 5 - len(completions))
            level += 1
        return completions

    def get_completions(self, prefix, score, flag=0, letter=""):
        self.search_seq(prefix, flag, letter)
        return self.get_sequences(prefix, score)

    def second_level_score(self, prefix, flag):
        ret_arr = []
        if len(prefix) < 5:
            for i in range(4, len(prefix)):
                ret_arr += self.get_completions(prefix[:i] + "~" + prefix[i + 1:], -1, flag, prefix[i])
        return ret_arr

    def third_level_score(self, prefix, flag):
        if len(prefix) < 4:
            return []
        ret_arr = self.get_completions(prefix[:3] + "~" + prefix[4:], -2, flag, prefix[3])
        length = len(ret_arr)
        if length < flag:
            for i in range(4, len(prefix)):
                if length < flag:
                    ret_arr += self.get_completions(prefix[:i] + prefix[i + 1:], -2, flag - length)
                    length = len(ret_arr)
                if length < flag:
                    ret_arr += self.get_completions(prefix[:i] + "~" + prefix[i:], -2, flag - length)
                else:
                    break
        return ret_arr

    def fourth_level_score(self, prefix, flag):
        ret_arr = []
        if len(prefix) >= 3:
            ret_arr += self.get_completions(prefix[:2] + "~" + prefix[3:], -3, flag, prefix[2])
        return ret_arr

    def fifth_level_score(self, prefix, flag):
        """return the sentences of fifth grade score"""
        if len(prefix) < 2:
            return []
        ret_arr = self.get_completions(prefix[:1] + "~" + prefix[2:], -4, flag, prefix[1])
        length = len(ret_arr)
        if length < flag:
            ret_arr += self.get_completions(prefix[:3] + prefix[4:], -4, flag - length)
            length = len(ret_arr)
        if length < flag:
            ret_arr += self.get_completions(prefix[:3] + "~" + prefix[3:], -4, flag - length)
        return ret_arr

    def sixth_level_score(self, prefix, flag):
        ret_arr = []
        ret_arr += self.get_completions("~" + prefix[1:], -5, flag, prefix[0])
        return ret_arr

    def seventh_level_score(self, prefix, flag):
        ret_arr = []
        if len(prefix) >= 3:
            ret_arr += self.get_completions(prefix[:2] + prefix[3:], -6, flag)
            if len(ret_arr) < flag:
                ret_arr += self.get_completions(prefix[:2] + "~" + prefix[2:], -6, flag - len(ret_arr))
        return ret_arr

    def eighth_level_score(self, prefix, flag):
        ret_arr = []
        if len(prefix) >= 2:
            ret_arr += self.get_completions(prefix[:1] + prefix[2:], -7, flag)
            if len(ret_arr) < flag:
                ret_arr += self.get_completions(prefix[:1] + "~" + prefix[1:], -7, flag - len(ret_arr))
        return ret_arr

    def ninth_level_score(self, prefix, flag):
        ret_arr = []
        ret_arr += self.get_completions(prefix[1:], -8, flag)
        if len(ret_arr) < flag:
            ret_arr += self.get_completions("~" + prefix, -8, flag - len(ret_arr))
        return ret_arr
