import matplotlib.pyplot as plt
import tqdm
from game import Game
from ai import AI

def run_experiment_with_comparison(num_runs=1, max_moves=2000):
    original_scores = []  # 原始算法的得分
    improved_scores = []  # 改进算法的得分

    # 运行原始算法
    for run in tqdm.tqdm(range(num_runs), desc="Original Exp-3"):
        game = Game()
        ai = AI(game.current_state(), search_depth=3)
        run_scores = []

        for move_count in tqdm.tqdm(range(max_moves), desc="Moves", leave=False):
            ai = AI(game.current_state(),search_depth=3)
            ai.build_tree(ai.root, ai.search_depth)
            direction, _ = ai.compute_decision()  # 使用原始评估函数
            if direction is not None:
                game.move_and_place(direction)
                run_scores.append(game.score)
            else:
                break
        original_scores.append(run_scores)

    # 运行改进算法
    for run in tqdm.tqdm(range(num_runs), desc="Improved Exp-3"):
        game = Game()
        ai = AI(game.current_state(), search_depth=3)
        run_scores = []

        for move_count in tqdm.tqdm(range(max_moves), desc="Moves", leave=False):
            ai = AI(game.current_state(),search_depth=3)
            ai.build_tree(ai.root, ai.search_depth)
            direction, _ = ai.compute_decision()  # 使用改进的评估函数
            if direction is not None:
                game.move_and_place(direction)
                run_scores.append(game.score)
            else:
                break
        improved_scores.append(run_scores)

    plot_comparison(original_scores, improved_scores)

def plot_comparison(original_scores, improved_scores):
    plt.figure(figsize=(12, 8))
    
    # 绘制原始算法的得分
    for i, scores in enumerate(original_scores):
        plt.plot(scores, label=f'Original Run {i + 1}', linestyle='--', alpha=0.7)
    
    # 绘制改进算法的得分
    for i, scores in enumerate(improved_scores):
        plt.plot(scores, label=f'Improved Run {i + 1}', linestyle='-', alpha=0.7)
    
    plt.title('Comparison of Original and Improved Exp-3 Performance')
    plt.xlabel('Move Count')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.savefig('/root/code/257_hw/hw2/figure/q2/q2.2.png')
    plt.show()

# 运行实验并绘制图表
run_experiment_with_comparison()