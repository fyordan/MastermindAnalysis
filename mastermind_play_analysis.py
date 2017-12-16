import pandas as pd
import mastermind_prob as game
import mastermind_ai_play as simple_ai
import matplotlib.pyplot as plt
import numpy as np
from ast import literal_eval

data = pd.read_csv('mastermind_data.csv')
data.dropna(axis=1, how='all', inplace=True)
data.dropna(axis=0, how='all', inplace=True)
data = data.sample(frac=1).reset_index(drop=True)

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
    simple_ai_prob = [] # Same as above but for simple_ai bot
    complex_ai_prob = [] # Same as above but for complex_ai bot
    player_round = game.Round(sol, dist, verbose=False)
    simple_ai_round = game.Round(sol, dist, verbose=False)
    complex_ai_round = game.Round(sol, dist, verbose=False)
    player_prob.append(player_round.solution_prediction[sol])
    simple_ai_prob.append(simple_ai_round.solution_prediction[sol])
    complex_ai_prob.append(complex_ai_round.solution_prediction[sol])

    print('+++++++++++++++++++++++++')
    print('Player:',row.Participant)
    print(row.Round)
    print(player_round.solution_prediction[sol])
    player_guesses = [0.0]
    for seq in sequences:
        player_guesses.append(player_round.solution_prediction[seq])
        player_round.next_turn(seq)
        player_prob.append(player_round.solution_prediction[sol])
        print(player_round.solution_prediction[sol])
    player_turns = len(sequences)
    print('Number of turns:', len(sequences))
    
    print('---------------')
    
    print('Simple AI:\n')
    simple_ai_player = simple_ai.AIPlay(dist)
    out = (0,0)
    print("Solution:", sol)
    simple_ai_turns = 0
    simple_ai_guesses = [0.0]
    while (out[1] != 3):
        seq = simple_ai_player.play_turn(out)
        simple_ai_guesses.append(simple_ai_round.solution_prediction[seq])
        simple_ai_turns += 1
        print("Chosen sequence:",seq)
        simple_ai_round.next_turn(seq)
        out = game.observe_sequence(seq, sol)
        print("Feedback:",out)
        simple_ai_prob.append(simple_ai_round.solution_prediction[sol])
        print(simple_ai_round.solution_prediction[sol])
    print('Number of turns:', simple_ai_turns)
    
    print('------------------')

    print('Complex AI:\n')
    complex_ai_player = game.ComplexAI(dist)
    out = (0,0)
    print("Solution:", sol)
    complex_ai_turns = 0
    complex_ai_guesses = [0.0]
    while (out[1] != 3):
        seq = complex_ai_player.get_sequence()
        complex_ai_guesses.append(complex_ai_round.solution_prediction[seq])
        complex_ai_turns += 1
        print("Chosen sequence:",seq)
        complex_ai_round.next_turn(seq)
        out = game.observe_sequence(seq, sol)
        print("Feedback:",out)
        complex_ai_player.update_belief_state(seq, out)
        complex_ai_prob.append(complex_ai_round.solution_prediction[sol])
        print(complex_ai_round.solution_prediction[sol])
    print('Number of turns:', complex_ai_turns)
    # Plot performance of AI vs Human Player
    x = np.arange(max((simple_ai_turns, player_turns, complex_ai_turns)) + 1)
    
    simple_ai_color = 'red'
    complex_ai_color = 'purple'
    player_color = 'blue'
    
    colors = np.array([player_color, simple_ai_color, complex_ai_color])
    turns = np.array([player_turns, simple_ai_turns, complex_ai_turns])
    guesses = [player_guesses, simple_ai_guesses, complex_ai_guesses]
    probs = [player_prob, simple_ai_prob, complex_ai_prob]

    win_color = colors[np.argmin(turns)]
    vline = np.min(turns)
    

    for prob in probs:
        prob.extend([1.0 for x in range(np.max(turns) + 1 - len(prob))])
    for guess in guesses:
        guess.extend([guess[-1] for x in range(np.max(turns) +1 - len(guess))])


    x = np.arange(max(turns) + 1)

    # Graph 'Percieved Probability' of Correct Solution
    plt.subplot(211)
    plt.plot(x, probs[0], color=colors[0])
    plt.plot(x, probs[1], color=colors[1])
    plt.plot(x, probs[2], color=colors[2])
    plt.axvline(x=vline, color=win_color,linestyle='dashed')
    
    plt.legend(['Player probability', 'Simple AI probability', 'Complex AI probability', \
                ('Solution: ' + sol)], loc='upper left')
    plot_title = row.Participant + ' -  Distribution: ' + str(int(row.Distribution)) \
                                 + ' - Round: ' + str(int(row.Round))
    plt.title('P(S=solution|Observations)', fontsize=10)
    
    
    # Graph Probability of Correctness of current sequence being played
    plt.subplot(212)
    
    plt.plot(x, guesses[0], color=colors[0])
    plt.plot(x, guesses[1], color=colors[1])
    plt.plot(x, guesses[2], color=colors[2])
    plt.axvline(x=vline, color=win_color,linestyle='dashed')
    
    plt.title('P(S=guess|Observations)',fontsize=10)

    plt.subplots_adjust(hspace=0.4, top=0.8)
    plt.suptitle(plot_title)
    
    #plt.show()
    plt.savefig('./player_graphs/'+ plot_title + '.png')
    print("clearing figure...")
    plt.clf()
    print("\n")

