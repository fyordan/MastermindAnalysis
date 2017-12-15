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
    player_guesses = []
    for seq in sequences:
        player_guesses.append(player_round.solution_prediction[seq])
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
    ai_guesses = []
    while (out[1] != 3):
        seq = ai_player.play_turn(out)
        ai_guesses.append(ai_round.solution_prediction[seq])
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
    
    ai_color = 'red'
    player_color = 'blue'
    if turns < len(sequences):
        win_color = ai_color
        vline = turns
    elif len(sequences) > turns:
        win_color = player_color
        vline = len(sequences)
    else:
        win_color = 'green'
        vline = turns

    while not (len(ai_prob) == len(player_prob)):
        if len(ai_prob) < len(player_prob):
            ai_prob.append(1.0)
        else:
            player_prob.append(1.0)

    # Graph 'Percieved Probability' of Correct Solution
    plt.figure(1)
    plt.plot(x, player_prob, color=player_color)
    plt.plot(x, ai_prob, color=ai_color)
    plt.axvline(x=vline, color=win_color,linestyle='dashed')
    
    plt.legend(['Player probability', 'AI probability', ('Solution: ' + sol)], loc='upper left')
    plt.title(row.Participant, loc='left')
    plt.title(('Distribution: ' + str(int(row.Distribution))), loc='center')
    plt.title(('Round: ' + str(int(row.Round))), loc='right')

    # Graph Probability of Correctness of current sequence being played
    plt.figure(2)

    while not (len(ai_guesses) == len(player_guesses)):
        if len(ai_guesses) < len(player_guesses):
            ai_guesses.append(1.0)
        else:
            player_guesses.append(1.0)
    x = np.arange(max(len(ai_guesses), len(player_guesses)))
    plt.plot(x, player_guesses, color=player_color)
    plt.plot(x, player_guesses, color=player_color)

    plt.show()
    print("clearing figure...")
    plt.clf()
    print("\n")

