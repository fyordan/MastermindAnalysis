import copy
import mastermind_prob as tools
import operator

class AIPlay:
    def __init__(self, distribution):
        self.dist = distribution
        self.sequences = set([x+y+z for x in self.dist for y in self.dist for z in self.dist])
        self.sequences_prediction = tools.sequence_posteriors(self.sequences, self.dist)
        #print("AI Sequences to Predict:\n",self.sequences_prediction,"----------\n")
        self.seq_to_play = max(self.sequences_prediction.items(), key=operator.itemgetter(1))[0]
        self.first_turn = True

    def update_prediction(self, feedback):
        for sequence in list(self.sequences):
            if tools.observe_sequence(self.seq_to_play, sequence) != feedback:
                self.sequences.discard(sequence)
        self.sequences_prediction = tools.sequence_posteriors(self.sequences, self.dist)
        #print("AI updated sequences",self.sequences_prediction)
        self.seq_to_play = max(self.sequences_prediction.items(), key=operator.itemgetter(1))[0]
        #print('AI sequence to play:',self.seq_to_play)

    def play_turn(self, feedback=None):
        if self.first_turn:
            self.first_turn = False
            most_probable_seq = copy.copy(self.seq_to_play)
            return most_probable_seq
        self.update_prediction(feedback)
        most_probable_seq = copy.copy(self.seq_to_play)
        return most_probable_seq
    
    
        

    
    
