import pandas as pd
import mastermind_prob as game
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
    sol = row.Solution
    sequences = row.Sequences.strip('[ ]').split(', ')
    probabilities = []
    round = game.Round(sol, dist, verbose=False)
    probabilities.append(round.solution_prediction[sol])
    print(round.solution_prediction[sol])
    for seq in sequences:
        round.next_turn(seq)
        probabilities.append(round.solution_prediction[sol])
        print(round.solution_prediction[sol])
    print("\n")

