import pandas as pd
import mastermind_prob as game
import mastermind_ai_play as ai
import matplotlib.pyplot as plt
import numpy as np
from ast import literal_eval

data = pd.read_csv('mastermind_data.csv')
data.dropna(axis=1, how='all', inplace=True)
data.dropna(axis=0, how='all', inplace=True)

for index, row in data.iterrows():
    dist_marker = row.Distribution
    if dist_marker == 111:
        dist = game.normal_dist
    elif dist_marker == 321:
        dist = game.r1_2_3_dist
    else:
        dist = game.r1_1_3_dist
    sol = row.Solution.strip()
    sequences = row.Sequences.strip('[ ]').split(', ')
    player_prob = [] # Probability player has enough info to guess the correct sequence
    ai_prob = [] # Same as above but for ai bot
    player_round = game.Round(sol, dist, verbose=False)
    ai_round = game.Round(sol, dist, verbose=False)
    player_prob.append(player_round.solution_prediction[sol])
    ai_prob.append(ai_round.solution_prediction[sol])

    print('+++++++++++++++++++++++++')
    print('Player:',row.Participant)
    print(row.Round)
    print(player_round.solution_prediction[sol])
    for seq in sequences:
        player_round.next_turn(seq)
        player_prob.append(player_round.solution_prediction[sol])
        print(player_round.solution_prediction[sol])
    print('Number of turns:', len(sequences))
    print('---------------')
    print('Mastermind AI:\n')
    #print(ai_round.solution_prediction[sol])
    ai_player = ai.AIPlay(dist)
    out = (0,0)
    print("Solution:", sol)
    turns = 0
    while (out[1] != 3):
        seq = ai_player.play_turn(out)
        turns += 1
        print("Chosen sequence:",seq)
        ai_round.next_turn(seq)
        out = game.observe_sequence(seq, sol)
        print("Feedback:",out)
        ai_prob.append(ai_round.solution_prediction[sol])
        print(ai_round.solution_prediction[sol])
    print('Number of turns:', turns)
    
    # Plot performance of AI vs Human Player
    x = np.arange(max(len(sequences), turns) + 1)
    
    while (len(ai_prob) != len(player_prob)):
        if len(ai_prob) > len(player_prob):
            ai_prob.append(1.0)
        else:
            player_prob.append(1.0)
    
    plt.plot(x, player_prob)
    plt.plot(x, ai_prob)
    plt.legend(['Player probability', 'AI probability', 'y = 3x'], loc='upper left')

    plt.show()
    print("clearing figure...")
    plt.clf()
    print("\n")

