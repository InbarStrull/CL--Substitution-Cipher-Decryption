import urllib.request


class CorpusReader:

    def __init__(self, url):
        self.url = url
        self.filtered_corpus = self.filter()

    def open_to_read(self):
        """ opens the file, reads its content
        with utf-8 decoding, closes the file.
        returns the decoded read fle"""
        with urllib.request.urlopen(self.url) as f:
            html = (f.read().decode('utf-8'))       # from stackoverflow
        f.close()
        return html

    def filter(self):
        """ filters the corpus so that it only
        contains characters from the English
        alphabet (a-z), spaces, and characters
        from T. returns the filtered corpus"""
        T = self.get_T_set()        # kept T's name from the instrucions
        to_filt = self.open_to_read()
        filtered = ""
        in_T =  lambda a: a in T    # if char in T
        english_up = lambda a: ord(a) >= 65 and ord(a) <= 90    # if char is an english capital letter
        english_low = lambda a: ord(a) >= 97 and ord(a)<=122    # if char is in english lowercase
        for char in to_filt:
            if in_T(char) or english_low(char) or char == " ":  # add to the filtered corpus
                filtered += char
            elif english_up(char):      # add as lowercase to the filtered corpus
                new = char.lower()
                filtered += new

        return filtered

    def get_filtered(self):
        return self.filtered_corpus

    def get_T(self):
        """ access to T """
        T = [',', '.', ':', '\n', '#', '(', ')', '!', '?', "\'", '\"']
        return T

    def get_T_set(self):
        """ quick access to elements of T """
        T = {',', '.', ':', '\n', '#', '(', ')', '!', '?', "\'", '\"'}
        return T

    def get_chars(self):
        """ access to all specified characters """
        chars = [chr(i) for i in range(97,123)] + self.get_T() + [" "]
        return chars


class LanguageModel:

    def __init__(self, CR):
        self.filtered_corpus = CR.get_filtered()    # filtered corpus
        self.chars = CR.get_chars()                 # Sigma
        self.unigram_probs = self.generate_unigram_model()          # unigram probabilities
                                                                    # unigram_probs[i] = P(w{i))
        self.bigram_probs = self.generate_bigram_model()            # bigram probabilities
                                                                    # bigram_probs[(i, j)] = P(w(i)|w(j))

    def get_chars(self):
        return self.chars

    def get_corpus(self):
        return self.filtered_corpus

    def unigram(self):
        """ counts the number of occurrences of the specified
        characters in a given filtered corpus
        returns a dictionary, where the key is the character
        and the value being the counts """
        unig_count = dict()     # using a dictionary
        for char in self.get_corpus():
            if char in unig_count:
                unig_count[char] += 1
            else:
                unig_count[char] = 1

        for i in self.get_chars():      # if a character was not counted
            if i not in unig_count:
                unig_count[i] = 0

        return unig_count

    def bigram(self):
        """ counts the number of occurrences of pairs
        of the specified characters in a given
        filtered corpus.
        returns dictionary bigram_dic
        where the bigram_dic(i,j) is the number
        of occurrences of the sequence w(i)w(j) """
        bigram_dic = dict()
        text = self.get_corpus()
        i = 0
        j = 1   # i + 1
        while j < len(text):
            cur = text[i]   # w(i)
            after = text[j] # w(i+1)
            if (cur, after) in bigram_dic:
                bigram_dic[(cur, after)] += 1
            else:
                bigram_dic[(cur, after)] = 1
            i += 1
            j += 1

        for k in self.get_chars():       # if a pair wasn't counted
            for l in self.get_chars():
                if (k,l) not in bigram_dic:
                    bigram_dic[(k,l)] = 0

        return bigram_dic

    def generate_unigram_model(self):
        """ computes MLE + Laplace from
         the dictionary created in unigram
         returns a new dictionary with computations"""
        n = len(self.get_corpus())       # corpus length
        v = len(self.get_chars())                 # vocabulary length
        counts = self.unigram()             # unigram count
        mle_laplace = {i : ((counts[i] + 1)/ (n + v)) for i in counts}

        return mle_laplace

    def generate_bigram_model(self):
        """ computes MLE + Laplace from
         the matrix created in bigram
         returns a new dictionary with computations
         where generate_bigram_model[(i,j)] = P(w(i)|w(j))"""
        counts = self.unigram()     # uingram count
        my_bigram = self.bigram()   # bigram count
        chars = self.get_chars()          # vocabulary
        v = len(chars)      # vocabulary length
        mle_laplace = {(chars[i],chars[j]): ((my_bigram[(chars[i],chars[j])] + 1) / (counts[chars[i]] + v))\
                       for i in range(len(chars)) for j in range(len(chars))}

        return mle_laplace



