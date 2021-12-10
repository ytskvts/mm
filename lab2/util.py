import matplotlib.pyplot as plt
from numpy import append
from numpy import array_split
from numpy import ndarray


def show_probabilities_of_amount_of_requests(
        requests_in_system_at_time: ndarray,
        theoretical_probs: ndarray):
    #
    interval_len = 100
    intervals = array_split(requests_in_system_at_time, interval_len)

    for i in range(1, len(intervals)):
        intervals[i] = append(intervals[i], intervals[i - 1])

    for i in range(len(theoretical_probs)):
        interval_probabilities = []
        for interval in intervals:
            interval_probabilities.append(len(interval[interval == i]) / len(interval))
        plt.figure(figsize=(5, 5))
        plt.bar(range(len(interval_probabilities)), interval_probabilities, color='orange')
        plt.title(f"Вероятность того что ({i}) заявок в системе")
        plt.axhline(y=theoretical_probs[i], xmin=0, xmax=len(interval_probabilities),
                    color='red')
        plt.show()
