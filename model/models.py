from collections import Counter
import numpy as np
import pandas as pd



class Corrector():    
    
    def __init__(self, corpus: pd.DataFrame, suggestion_limit: int =3, verbose=False):
        '''
        - corpus: the corpus dataframe
        - suggestion_limit: the suggestion limit 
        
        '''
        self.verbose= verbose
        self.corpus = corpus
        self.suggestion_limit = suggestion_limit
        self.vocab, self.word_count_dict = self.__get_words()
        self.log_probs = self.get_log_probs()

    def __get_words(self) :
        """
        return a list of existing words in the corpus
        """
        return list(self.corpus["word"]), Counter(dict(zip(self.corpus["word"], self.corpus["count"])))
    
    def get_log_probs(self):
        '''
        Input:
            word_count_dict: The wordcount dictionary where key is the word and value is its frequency.
        Output:
            log_probs: A dictionary where keys are the words and the values are the log-probability that a word will occur. 
        '''
        log_probs = {}  # return this variable correctly
        
        m = sum(self.word_count_dict.values())
        for key in self.word_count_dict.keys():
            log_probs[key] = np.log(self.word_count_dict[key] / m)
        return log_probs
        
    def __delete_letter(self, word):
        '''
        Input:
            word: the string/word for which you will generate all possible words 
                    in the vocabulary which have 1 missing character
        Output:
            delete_l: a list of all possible strings obtained by deleting 1 character from word
        '''
        
        delete_l = []
        split_l = []

        for c in range(len(word)):
            split_l.append((word[:c],word[c:]))
        for a,b in split_l:
            delete_l.append(a+b[1:])

        if self.verbose: print(f"input word {word}, \nsplit_l = {split_l}, \ndelete_l = {delete_l}")

        return delete_l
        
    def __switch_letter(self, word):
        '''
        Input:
            word: input string
        Output:
            switches: a list of all possible strings with one adjacent charater switched
        ''' 
        
        switch_l = []
        split_l = []
        
        len_word=len(word)
        for c in range(len_word):
            split_l.append((word[:c],word[c:]))
        switch_l = [a + b[1] + b[0] + b[2:] for a,b in split_l if len(b) >= 2]
        
        if self.verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nswitch_l = {switch_l}") 

        return switch_l
    
    def __replace_letter(self, word):
        '''
        Input:
            word: the input string/word 
        Output:
            replaces: a list of all possible strings where we replaced one letter from the original word. 
        ''' 
        
        letters = 'abcdefghijklmnopqrstuvwxyz'
        replace_l = []
        split_l = []
        
        for c in range(len(word)):
            split_l.append((word[0:c],word[c:]))
        replace_l = [a + l + (b[1:] if len(b)> 1 else '') for a,b in split_l if b for l in letters]
        replace_set=set(replace_l)    
        replace_set.remove(word)
        
        # turn the set back into a list and sort it, for easier viewing
        replace_l = sorted(list(replace_set))
        
        if self.verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nreplace_l {replace_l}")   
        
        return replace_l
    
    def __insert_letter(self, word):
        '''
        Input:
            word: the input string/word 
        Output:
            inserts: a set of all possible strings with one new letter inserted at every offset
        ''' 
        letters = 'abcdefghijklmnopqrstuvwxyz'
        insert_l = []
        split_l = []
        
        for c in range(len(word)+1):
            split_l.append((word[0:c],word[c:]))
        insert_l = [ a + l + b for a,b in split_l for l in letters]

        if self.verbose: print(f"Input word {word} \nsplit_l = {split_l} \ninsert_l = {insert_l}")
        
        return insert_l
    
    def __edit_one_letter(self, word, allow_switches = True):
        """
        Input:
            word: the string/word for which we will generate all possible wordsthat are one edit away.
        Output:
            edit_one_set: a set of words with one possible edit. Please return a set. and not a list.
        """

        edit_one_set = set()

        edit_one_set.update(self.__delete_letter(word))
        if allow_switches:
            edit_one_set.update(self.__switch_letter(word))
        edit_one_set.update(self.__replace_letter(word))
        edit_one_set.update(self.__insert_letter(word))

        return edit_one_set
        
    def __edit_two_letters(self, word, allow_switches = True):
        '''
        Input:
            word: the input string/word 
        Output:
            edit_two_set: a set of strings with all possible two edits
        '''
        
        edit_two_set = set()
        
        edit_one = self.__edit_one_letter(word,allow_switches=allow_switches)
        for w in edit_one:
            if w:
                edit_two = self.__edit_one_letter(w,allow_switches=allow_switches)
                edit_two_set.update(edit_two)
        
        return edit_two_set
    
    
    def correct(self, word):
        
        '''
        Input: 
            word: a user entered string to check for suggestions
        Output: 
            n_best: a list of tuples with the most probable n corrected words and their probabilities.
        '''
        
        suggestions = []
        n_best = []
        
        suggestions = list((word in self.vocab and word) or self.__edit_one_letter(word).intersection(self.vocab) or self.__edit_two_letters(word).intersection(self.vocab))[:self.suggestion_limit]
        n_best = [[s, np.exp(self.log_probs[s])] for s in list(reversed(suggestions))]
        
        if self.verbose: print("suggestions = ", [ sugg_cap.capitalize() for sugg_cap in suggestions])
        
        return ", ".join([w[0] for w in n_best])

        