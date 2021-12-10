import simpy
import Model
import Statistics

if __name__ == '__main__':
    time = 1000

    _lambda = 5
    mu = 4
    v = 1
    m = 2
    n = 1


    env = simpy.Environment()
    model = Model.Model(_lambda, mu, v, m, n, env)
    env.run(time)

    Statistic = Statistics.Statistics(_lambda, mu, v, m, n, model.get_data_for_statistic())
    Statistic.generate()

    _lambda = 8
    mu = 5
    v = 6
    m = 4
    n = 3

    env = simpy.Environment()
    model = Model.Model(_lambda, mu, v, m, n, env)
    env.run(time)

    Statistic = Statistics.Statistics(_lambda, mu, v, m, n, model.get_data_for_statistic())
    Statistic.generate()