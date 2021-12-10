import math
import numpy as np
from scipy.stats import chisquare
import matplotlib.pyplot as plt
from util import show_probabilities_of_amount_of_requests

class Statistics:

    def __init__(self, _lambda, mu, v, m, n, data):
        self.__lambda = _lambda
        self.__mu = mu
        self.__v = v
        self.__m = m
        self.__n = n

        self.__stat = np.array(data[0])
        self.__queue_list = np.array(data[1])
        self.__total_request = np.array(data[2])
        self.__queue_time = np.array(data[3])
        self.__total_time = np.array(data[4])

    def show_chart(self, values, title, color):
        X = range(self.__m + self.__n + 1)
        fig, ax = plt.subplots(1, 1)
        ax.bar(X, values, width=0.1, color=color)
        ax.set_title(title)
        plt.show()

    def get_e_prob(self):
        P = [len(self.__stat[self.__stat == index]) / len(self.__stat) for index in range(self.__n + self.__m + 1)]
        for index, p in enumerate(P):
            print('p{0}: {1}'.format(index, p))
        return len(self.__stat[self.__stat == 0]) / len(self.__stat), len(
            self.__stat[self.__stat == self.__m + self.__n]) / len(self.__stat)

    def get_e(self):
        return [len(self.__stat[self.__stat == index]) / len(self.__stat) for index in range(self.__n + self.__m + 1)]

    def get_t_prob(self):
        teta = self.__lambda / self.__mu
        beta = self.__v / self.__mu
        p0 = 1 / (sum([(teta ** index) / math.factorial(index) for index in range(self.__n + 1)]) + (
                teta ** self.__n) / math.factorial(self.__n) * sum(
            [(teta ** index) / np.prod(np.array([self.__n + l * beta for l in range(1, index + 1)])) for index in
             range(1, self.__m + 1)]))
        print('\np0: {0}'.format(p0))
        for index in range(1, self.__n + 1):
            print('p{0}: {1}'.format(index, (p0 * teta ** index) / math.factorial(index)))
        pn = (p0 * teta ** self.__n) / math.factorial(self.__n)
        for index in range(1, self.__m + 1):
            print('p{0}: {1}'.format(self.__m + index - 1, pn * (teta ** index) / np.prod(
                np.array([self.__n + l * beta for l in range(1, index + 1)]))))
        pot = pn * (teta ** self.__m) / np.prod(np.array([self.__n + l * beta for l in range(1, self.__m + 1)]))
        return round(p0, 15), round(pot, 15), self.avg_gueqe_t(pn), self.avg_total_t(p0, pn)

    def get_t(self):
        teta = self.__lambda / self.__mu
        beta = self.__v / self.__mu
        p = []
        p.append(1 / (sum([(teta ** index) / math.factorial(index) for index in range(self.__n + 1)]) + (
                teta ** self.__n) / math.factorial(self.__n) * sum(
            [(teta ** index) / np.prod(np.array([self.__n + l * beta for l in range(1, index + 1)])) for index in
             range(1, self.__m + 1)])))
        for index in range(1, self.__n + 1):
            p.append((p[0] * teta ** index) / math.factorial(index))
        pn = p[-1]
        for index in range(1, self.__m + 1):
            p.append(pn * (teta ** index) / np.prod(
                np.array([self.__n + l * beta for l in range(1, index + 1)])))
        return p

    def avg_gueqe_e(self):
        return self.__queue_list.mean()

    def avg_gueqe_t(self, pn):
        teta = self.__lambda / self.__mu
        beta = self.__v / self.__mu
        return sum(
            [index * pn * (teta ** index) / np.prod(np.array([self.__n + l * beta for l in range(1, index + 1)])) for
             index in range(1, self.__m + 1)])

    def avg_total_e(self):
        return self.__total_request.mean()

    def avg_total_t(self, p0, pn):
        teta = self.__lambda / self.__mu
        beta = self.__v / self.__mu

        return sum([index * p0 * (teta ** index) / math.factorial(index) for index in range(1, self.__n + 1)]) + sum(
            [(self.__n + index) * pn * teta ** index / np.prod(
                np.array([self.__n + l * beta for l in range(1, index + 1)])) for
             index in range(1, self.__m + 1)])

    def avg_gueqe_time_e(self):
        return self.__queue_time.mean()

    def avg_total_time_e(self):
        return self.__total_time.mean()

    def generate(self):
        print('\nинтенсивность потока заявок lambda:{}'.format(self.__lambda))
        print('интенсивность потока обслуживания mu: {}'.format(self.__mu))
        print('время пребывания заявки в очереди: {}'.format(self.__v))
        print('размер очереди: {}'.format(self.__m))
        print('количество каналов:{}\n'.format(self.__n))

        e_prob = self.get_e_prob()
        print('\nЭмпирическая вероятность отказа:{0}'.format(e_prob[1]))
        print("Эмпирическая p0: {}".format(e_prob[0]))
        Q_e = 1 - e_prob[1]
        print("Эмпирическая относительная пропускная способность: {}".format(Q_e))
        A_e = Q_e * self.__lambda
        print("Эмпирическая абсолютная пропускная способность: {}".format(A_e))
        print("Эмпирическое среднее число заявок, находящихся в очереди: {}".format(self.avg_gueqe_e()))
        print("Эмпирическое среднее число заявок, обслуживаемых в СМО : {}".format(self.avg_total_e()))
        avg_off_e = Q_e * self.__lambda / self.__mu
        print("Эмпирическое среднее число занятых каналов: ", avg_off_e)
        print("Эмпирическое среднее время пребывания заявки в очереди: ", self.avg_gueqe_time_e())
        print("Эмпирическое среднее время пребывания заявки в очереди: ", self.avg_total_time_e())

        t_prob = self.get_t_prob()

        print('\nТеоретическая вероятность отказа:{0}'.format(t_prob[1]))
        print("Теоретическая p0: {}".format(t_prob[0]))
        Q_t = 1 - t_prob[1]
        print("Теоретическая относительная пропускная способность: {}".format(Q_t))
        A_t = Q_t * self.__lambda
        print("Теоретическая абсолютная пропускная способность: {}".format(A_t))
        print("Теоретическое среднее число заявок, находящихся в очереди: {}".format(t_prob[2]))
        print("Теоретическое среднее число заявок, обслуживаемых в СМО : {}".format(t_prob[3]))
        avg_off_t = Q_t * self.__lambda / self.__mu
        print("Теоретическое среднее число занятых каналов: ", avg_off_t)
        avg_queque_t = t_prob[2] / self.__lambda
        print("Теоретическое среднее время пребывания заявки в очереди: ", avg_queque_t)
        avg_SMO_t = t_prob[3] / self.__lambda
        print("Теоретическое среднее время пребывания заявки в очереди: ", avg_SMO_t)

        E_ver = self.get_e()
        self.show_chart(E_ver, 'Эмпирические финальные вероятности', 'magenta')
        P_ver = self.get_t()
        self.show_chart(E_ver, 'Теоретические финальные вероятности', 'cyan')
        show_probabilities_of_amount_of_requests(self.__total_request, P_ver)
        print(chisquare(E_ver, P_ver))
