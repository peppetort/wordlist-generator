from support.configuration import Configuration
import itertools


class Tools:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def upperize(self, word: str) -> []:
        return list(dict.fromkeys((map(''.join, itertools.product(*zip(word.upper(), word.lower()))))))

    def leetify(self, word: str) -> []:
        if self.configuration.leet is None:
            raise Exception('Leet map not set. Check configuration file')

        leet_list = []
        for l in self.configuration.leet.keys():
            if l in word or l.lower() in word:
                leet_list.append(
                    word.replace(l, str(self.configuration.leet[l])).replace(l.lower(), str(self.configuration.leet[l])))

        if any(x.lower() in word or x in word for x in self.configuration.leet.keys()):
            for w in leet_list:
                leet_list = leet_list + self.leetify(w)
                leet_list = list(dict.fromkeys(leet_list))
        return leet_list

    def mix(self, word_list: []) -> []:
        res = []
        for i in range(0, len(word_list)):
            for j in range(i + 1, len(word_list)):
                res = res + list(map(''.join, itertools.permutations(word_list[i:j + 1])))
        return res

    def add_year(self, word: str) -> []:
        if self.configuration.years is None:
            raise Exception('Years list not set. Check configuration file')
        res = []
        for y in self.configuration.years:
            res.append((word + str(y)))
            res.append(word + str(y)[2:4])
        return res

    def add_special(self, word: str) -> []:
        if self.configuration.special_chars is None:
            raise Exception('Special chars list not set. Check configuration file')
        res = []
        for s in self.configuration.special_chars:
            res.append(word + str(s))
        return res

    def create_chunks(self) -> []:
        chunk_list = []
        keyword_list = self.configuration.keywords

        reminder = len(keyword_list) % self.configuration.chunk_len
        if reminder != 0:
            master_keyword_list = keyword_list[:-reminder]
            chunk_list.append(keyword_list[-reminder:])
        else:
            master_keyword_list = keyword_list

        for i in range(0, len(master_keyword_list)):
            chunk = [master_keyword_list[i]]

            div = (len(keyword_list) // self.configuration.chunk_len)
            n = div + (div - 1) * 2 + reminder - i

            for k in range(0, n):
                index = i + k + 1
                for j in range(index, index + self.configuration.chunk_len - 1):
                    chunk.append(keyword_list[j])
                chunk_list.append(chunk.copy())
                chunk.clear()
                chunk.append(keyword_list[i])

        return chunk_list
