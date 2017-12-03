from collections import Counter
from collections import defaultdict
import numpy as np

normal_dist = {"S":1./3., "C":1/3., "T":1/3.0}
r1_2_3_dist = {"S":2./6., "C":3/6., "T":1/6.0}
r1_1_3_dist = {"S":2./5., "C":1/5., "T":3/5.0}

def get_random_sequence(dist, length):
    return ''.join(np.random.choice([x for x in dist], length, p=[dist[x] for x in dist]))


def sequence_prior(sequence, distribution):
    prob = 1.0
    for symbol in sequence:
        prob *= distribution[symbol]
    return prob


def sequence_posteriors(sequences, distribution):
    out = defaultdict(float)
    norm_factor = 0.0
    for sequence in sequences:
        prob = sequence_prior(sequence, distribution)
        out[sequence] = prob
        norm_factor += prob
    for sequence in sequences:
        out[sequence] /= norm_factor
    return out


def observe_sequence(sequence, solution):
    correct_color_count = {}
    total_correct_color_count = 0
    total_correct_pos_count = 0
    sequence_cnt = Counter(sequence)
    solution_cnt = Counter(solution)
    for symbol in sequence:
        correct_color_count[symbol] = min(sequence_cnt[symbol], solution_cnt[symbol])
    for i in xrange(len(sequence)):
        if sequence[i] == solution[i]:
            total_correct_pos_count += 1
            correct_color_count[sequence[i]] -= 1
    for symbol in correct_color_count:
        total_correct_color_count += correct_color_count[symbol]
    return (total_correct_color_count, total_correct_pos_count)


def update_belief_state(sequences, input_sequence, solution, distribution):
    observed_outcome = observe_sequence(input_sequence, solution)
    for sequence in list(sequences):
        if observe_sequence(input_sequence, sequence) != observed_outcome:
            sequences.discard(sequence)
    return sequence_posteriors(sequences, distribution)



class Round:
    def __init__(self, solution, dist, verbose=False):
        self.game_dist = dist
        self.solution = solution
        self.points = 0
        self.sequences = set([x+y+z for x in dist for y in dist for z in dist])
        self.solution_prediction = sequence_posteriors(self.sequences, dist)
        self.verbose = verbose
        if (verbose):
            print "\n"
            print "New Game"
            print "Game started with solution: " + self.solution
            print "P(solution) = " + str(self.solution_prediction[self.solution])
            print "-------------------------------------------------------"

    def next_turn(self, sequence):
        self.points += 1
        if (self.verbose):
            print "Move: " + sequence
            print "P(sequence win) = " + str(self.solution_prediction[sequence])
            print "Out: " + str(observe_sequence(sequence, self.solution))

        self.solution_prediction = update_belief_state(
            self.sequences, sequence, self.solution, self.game_dist)
        if (self.verbose):
            print "New Posteriors: "
            print self.solution_prediction
            print "--------------------------------------------------------"


# round = Round("CTC", normal_dist, verbose=True)
# round.next_turn("TCS")
# round.next_turn("TCC")
# round.next_turn("CTC")

if __name__ == '__main__':
    sol = get_random_sequence(r1_2_3_dist, 3)
    out = (0,0)
    round = Round(sol, r1_2_3_dist, verbose=False)
    while (out[1] != 3):
        seq = raw_input("What's your move? ")
        round.next_turn(seq)
        out = observe_sequence(seq, sol)
        print "Out: " + str(out)
    print "Thanks For Playing! Score: " + str(round.points) 
