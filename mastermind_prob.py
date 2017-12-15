from collections import Counter
from collections import defaultdict
import numpy as np

normal_dist = {"S":1./3., "C":1/3., "T":1/3.0}
r1_2_3_dist = {"S":2./6., "C":3/6., "T":1/6.0}
r1_1_3_dist = {"S":1./5., "C":1/5., "T":3/5.0}

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
    for i in range(len(sequence)):
        if sequence[i] == solution[i]:
            total_correct_pos_count += 1
            correct_color_count[sequence[i]] -= 1
    for symbol in correct_color_count:
        total_correct_color_count += correct_color_count[symbol]
    return (total_correct_color_count, total_correct_pos_count)


def update_belief_state(sequences, input_sequence, feedback, distribution):
    for sequence in list(sequences):
        if observe_sequence(input_sequence, sequence) != feedback:
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
            print("\n")
            print("New Game")
            print("Game started with solution: " + self.solution)
            print("P(solution) = " + str(self.solution_prediction[self.solution]))
            print("-------------------------------------------------------")

    def next_turn(self, sequence):
        self.points += 1
        feedback = observe_sequence(sequence, self.solution)
        if (self.verbose):
            print("Move: " + sequence)
            print("P(sequence win) = " + str(self.solution_prediction[sequence]))
            print("Out: " + str(feedback))

        self.solution_prediction = update_belief_state(
            self.sequences, sequence, feedback, self.game_dist)
        if (self.verbose):
            print("New Posteriors: ")
            print(self.solution_prediction)
            print("--------------------------------------------------------")

class ComplexAI:
    # get_sequence(belief_state, distr) -> sequence
    def __init__(self, dist):
        self.dist = dist
        self.all_sequences = set([x+y+z for x in dist for y in dist for z in dist])
        self.belief_state = sequence_posteriors(self.all_sequences, dist)
        self.possible_seqs = self.all_sequences.copy()
        
    def update_belief_state(self, played_sequence, feedback):
        self.belief_state = update_belief_state(self.possible_seqs,
                                                played_sequence,
                                                feedback,
                                                self.dist)

    def get_sequence(self):
        if (len(self.possible_seqs) == 1):
            return list(self.possible_seqs)[0]
        best_s = None
        best_val = 0.0
        for s in self.all_sequences:
            value = 0.0
            for sol in self.possible_seqs:
                feedback = observe_sequence(s, sol)
                p_feedback = self.belief_state[sol]
                pot_state = update_belief_state(self.possible_seqs.copy(),
                                                s, feedback, self.dist)
                value += p_feedback*max(pot_state.values())
            if (value > best_val):
                best_s = s
                best_val = value
        return best_s


def play_game_with_AI():
    ai = ComplexAI(normal_dist)
    sol = get_random_sequence(normal_dist, 3)
    out = (0,0)
    round = Round(sol, normal_dist, verbose=True)
    while (out[1] != 3):
        seq = ai.get_sequence()
        round.next_turn(seq)
        out = observe_sequence(seq, sol)
        ai.update_belief_state(seq, out)


if __name__ == '__main__':
    sol = get_random_sequence(r1_2_3_dist, 3)
    out = (0,0) 
    round = Round(sol, r1_2_3_dist, verbose=True)
    while (out[1] != 3):
        seq = raw_input("What's your move? ")
        round.next_turn(seq)
        out = observe_sequence(seq, sol)
        print("Out: " + str(out))
    print("Thanks For Playing! Score: " + str(round.points))
    # play_game()
