import matplotlib.pyplot as plt
from game import Game
from ai import AI
import tqdm
def run_random_experiment(num_runs=5, max_moves=1000):
    all_scores = []  # 用于存储每次运行的得分

    for run in tqdm.tqdm(range(num_runs)):
        game = Game()
        ai = AI(game.current_state(), search_depth=3)
        run_scores = []

        for move_count in tqdm.tqdm(range(max_moves)):
            ai = AI(game.current_state(),search_depth=3)
            ai.build_tree(ai.root, ai.search_depth)
            #old
            direction, _ = ai.compute_decision()
            if direction is not None:
                game.move_and_place(direction)
                run_scores.append(game.score)
            else:
                break
        all_scores.append(run_scores)

    plot_scores(all_scores)

def plot_scores(all_scores):
    plt.figure(figsize=(10, 6))
    for i, scores in enumerate(all_scores):
        plt.plot(scores, label=f'Run {i + 1}')
    
    plt.title('Random Experiment Scores Over Time')
    plt.xlabel('Move Count')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.savefig('/root/code/257_hw/hw2/figure/q2/q2.1.png')

# 运行随机实验
run_random_experiment()