import matplotlib.pyplot as plt
from game import Game
from ai import AI

def run_experiment(exp_version, num_runs=5, max_moves=1000):
    scores = []

    for run in range(num_runs):
        game = Game()
        ai = AI(game.current_state(), search_depth=3 if exp_version == 'Exp-3' else 1)
        run_scores = []

        for move_count in range(max_moves):
            if game.game_over():
                print(f"Run {run + 1}: Game over at move {move_count}")
                break

            if exp_version == 'Exp-1':
                direction = ai.compute_decision()
            else:
                direction = ai.compute_decision_ec()

            if direction is not None:
                game.move_and_place(direction)
                run_scores.append(game.score)
            else:
                print(f"Run {run + 1}: No valid move at move {move_count}")
                break

        scores.append(run_scores)

    return scores

def plot_scores(scores, exp_version):
    plt.figure(figsize=(10, 6))
    for i, run_scores in enumerate(scores):
        plt.plot(run_scores, label=f'Run {i + 1}')
    
    plt.title(f'{exp_version} Performance')
    plt.xlabel('Move Count')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.show()

# Run experiments for Exp-1 and Exp-3
exp1_scores = run_experiment('Exp-1')
exp3_scores = run_experiment('Exp-3')

# Plot the results
plot_scores(exp1_scores, 'Exp-1')
plot_scores(exp3_scores, 'Exp-3')