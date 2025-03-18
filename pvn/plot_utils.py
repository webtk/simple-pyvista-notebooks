import matplotlib.pyplot as plt
import numpy as np

def plot_histogram(arr: np.ndarray):
    # 1) 히스토그램 그리기
    plt.figure(figsize=(10, 6))
    plt.hist(arr, bins=50, edgecolor='black', alpha=0.7)

    # 2) 그래프 꾸미기
    plt.title('Histogram of Surface Distances')
    plt.xlabel('Distance to Surface')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)

    # 3) 기본 통계 정보 표시
    mean_dist = np.mean(arr)
    std_dist = np.std(arr)
    plt.axvline(mean_dist, color='r', linestyle='dashed', linewidth=2, label=f'Mean: {mean_dist:.3f}')
    plt.axvline(mean_dist + std_dist, color='g', linestyle='dashed', linewidth=2, label=f'Std: {std_dist:.3f}')
    plt.axvline(mean_dist - std_dist, color='g', linestyle='dashed', linewidth=2)
    plt.legend()

    # 4) 그래프 표시
    plt.show()

    # 5) 기본 통계 정보 출력
    print(f"Mean distance: {mean_dist:.3f}")
    print(f"Standard deviation: {std_dist:.3f}")
    print(f"Min distance: {np.min(arr):.3f}")
    print(f"Max distance: {np.max(arr):.3f}")