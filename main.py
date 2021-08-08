
import language_model
import permutation
import simulated_annealing


def main(url = "http://www.gutenberg.org/files/76/76-0.txt ", t=100, threshold=0.001, cooling=0.9995):
    corp = language_model.CorpusReader(url)
    model = language_model.LanguageModel(corp)
    address = "problemset_07_encrypted_input.txt"
    f = open(address, 'r')
    message = f.read()
    f.close()
    chars = corp.get_chars()
    trivial_perm = {ord(char): ord(char) for char in chars}     # initial hypothesis
    perm = permutation.Permutation(trivial_perm)
    sim = simulated_annealing.SimulatedAnnealing(t, threshold, cooling)
    experiment = sim.run(perm, message, model)      # returns the matching permutation
    to_print = ["permutation: " ,experiment, "iמitial temprature: " ,t, "treshold: ",threshold,"cooling rate: ", cooling, "decryption:\n" + experiment.translate(message)]
    for i in to_print:
        print(i)

# if you wish to run the program 10 times, uncomment
#for i in range(10):
    #print("try:", i)
    #main()
main()
