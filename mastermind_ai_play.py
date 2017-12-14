import mastermind_prob as tools
import operator

class AIPlay:
    def __init__(self, distribution):
        self.dist = distribution
        self.sequences = set([x+y+z for x in self.dist for y in self.dist for z in self.dist])
        self.solution_prediction = tools.sequence_posteriors(self.sequences, self.dist)
        self.seq_to_play = max(self.solution_prediction.iteritems(), key=operator.itemgetter(1))[0]
        self.first_turn = False

    def update_prediction(self, feedback):
        for sequence in list(self.sequences):
            if tools.observe_sequence(self.seq_to_play, sequence) != feedback:
                self.sequences.discard(sequence)
        self.solution_prediction = tools.sequence_posteriors(self.sequences, self.dist)
        self.seq_to_play = max(self.solution_prediction.iteritems(), key=operator.itemgetter(1))[0]

    def play_turn(self, feedback):
        if !self.fisrt_turn:
            most_probable_seq = copy.copy(self.seq_to_play)
            self.first_turn = True
            return most_probable_seq
        update_prediction(feedback)
        most_probable_seq = copy.copy(self.seq_to_play)
        return most_probable_seq
    
    
        

    
    
