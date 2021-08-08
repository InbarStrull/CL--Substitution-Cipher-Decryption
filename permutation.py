import random
import math
import language_model


class Permutation:

    def __init__(self, perm):
        self.perm = perm    # dictionary, perm[ord(char[i])] = ord(char[j])
                            # replace char[i] with char[j]
        self.chars = [i for i in self.perm]     # Sigma

    def get_chars(self):
        return self.chars

    def get_perm(self):
        return self.perm

    def get_neighbor(self):
        """returns a random neighbor of the
        current permutation instance.
        a neighbor of a permutation is defined
        as a new permutation that simply replaces
        the mapping of two randomly chosen
        characters from Σ.
        uses the choice method from the random module."""
        choose_from = self.get_chars()                  # all characters
        char1 = random.choice(choose_from)              # choose character randomly
        char2 = random.choice(choose_from)              # choose another character randomly
        val1 = self.get_perm()[char1]
        val2 = self.get_perm()[char2]
        my_perm = self.get_perm().copy()                # new permutation
        my_perm[char1], my_perm[char2] = val2, val1     # swap
        new_perm = Permutation(my_perm)                 # new instance

        return new_perm

    def translate(self, string):
        """receives an input string,
         and returns the translation of
         that string according to the
        current permutation instance."""
        translated = string.translate(self.get_perm())
        return translated

    def get_energy(self, encrypted, model):
        """receives a data argument (= encrypted message)
        and a language model, and returns the
        energy of the current permutation"""
        n = len(encrypted)                  # length of the encrypted message
        trans = self.translate(encrypted)   # translate the message according to the permutation map
        uni = model.unigram_probs
        big = model.bigram_probs
        energy = -math.log(uni[trans[0]], 2)    # compute energy as required:
        for i in range(1,n-1):
            energy -= math.log(big[(trans[i],trans[i+1])], 2)

        return energy

    def __repr__(self):
        return str(self.perm)










