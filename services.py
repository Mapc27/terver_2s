import math
import statistics
from typing import List

from bokeh.plotting import figure
from bokeh.embed import components
from scipy import stats


def is_number(_str):
    try:
        float(_str)
        return True
    except ValueError:
        return False


class Statistics:
    instances: List = []

    def __init__(self, array: list = None):
        self.instances.append(self)

        self._list: list = array
        if not self._list:
            self._list = [1.1, 1.3, 1.5, 2, 2.2, 2.9, 3, 3.2, 3.2, 3.7, 3.9, 4, 4, 4.1, 4.5, 4.9, 5.1, 5.3, 5.9, 6,
                          6.8, 7.1, 7.9, 8.2, 8.7, 9, 9.5, 9.6, 10.3, 10.5]
        self._name: str = ''
        # проверка на название колонки
        if isinstance(self._list[0], str):
            if not is_number(self._list[0]):
                self._name = self._list[0]
                self._list = self._list[1:]

            try:
                self._list = [float(i) for i in self._list]
            except ValueError:
                self._list = None

        # self._intervals = [[1, 2.8], [2.8, 4.6], [4.6, 6.4], [6.4, 8.2], [8.2, 10.0], [10.0, 11.8]]
        # self._number_of_groups = 6
        # self._interval_step = 1.8

        if self._list:
            self._number: int = self.calculate_number()
            self._min: float = self.calculate_min()
            self._max: float = self.calculate_max()
            self._number_of_groups: int = self.calculate_number_of_groups()
            self._interval_step: float = self.calculate_interval_step()
            self._intervals: list = self.calculate_intervals()
            self._numbers_of_each_interval: list = self.calculate_numbers_of_each_interval()
            self._mean_values: list = self.calculate_mean_values()
            self._relative_frequencies: list = self.calculate_relative_frequencies()
            self._sample_mean: float = self.calculate_sample_mean()
            self._z: list = self.calculate_z()
            self._z_2: list = self.calculate_z_2()
            self._n_accumulated: list = self.calculate_n_accumulated()
            self._z_3_multiplication_relative_frequencies: list = self.calculate_z_3_multiplication_relative_frequencies()
            self._dispersion: float = self.calculate_dispersion()
            self._standard_deviation: float = self.calculate_standard_deviation()
            self._fashion: float = self.calculate_fashion()
            self._median: float = self.calculate_median()
            self._coefficient_of_asymmetry: float = self.calculate_coefficient_of_asymmetry()
            self._coefficient_of_kurtosis: float = self.calculate_coefficient_of_kurtosis()
            self._coefficient_of_variation: float = self.calculate_coefficient_of_variation()
            self._confidence_interval_of_sample_mean: tuple = self.calculate_confidence_interval_of_sample_mean()
            self._confidence_interval_of_dispersion: tuple = self.calculate_confidence_interval_of_dispersion()

    @classmethod
    def get_instance(cls, index):
        try:
            return cls.instances[index]
        except IndexError:
            return None

    def ready(self):
        return True if self._list else False

    def get_index(self):
        return self.instances.index(self)

    def calculate_min(self):
        min_value = self._list[0]
        for i in self._list:
            if i < min_value:
                min_value = i
        return min_value

    def calculate_max(self):
        max_value = self._list[0]
        for i in self._list:
            if i > max_value:
                max_value = i
        return max_value

    def calculate_number(self):
        return len(self._list)

    def calculate_number_of_groups(self):
        return math.floor(1 + 3.322 * math.log10(self._number))

    def calculate_interval_step(self):
        return (self._max - self._min) / self._number_of_groups

    def calculate_intervals(self):
        intervals = []
        for i in range(self._number_of_groups + 1):
            intervals.append(self._min + self._interval_step * i)

        tuple_intervals = []
        for i in range(len(intervals) - 1):
            tuple_intervals.append([intervals[i], intervals[i + 1]])
        return tuple_intervals

    def calculate_numbers_of_each_interval(self):
        numbers = []
        _list = self._list.copy()
        intervals = self._intervals.copy()
        intervals[-1][1] += 1

        for interval in intervals:
            number = 0
            for i in range(len(_list)):
                if interval[0] <= _list[i] < interval[1]:
                    number += 1
            numbers.append(number)
        intervals[-1][1] -= 1
        assert sum(numbers) == self._number
        return numbers

    def calculate_mean_values(self):
        values = []
        for interval in self._intervals:
            values.append((interval[0] + interval[1]) / 2)
        return values

    def calculate_relative_frequencies(self):
        return list(map(lambda x: x / self._number, self._numbers_of_each_interval))

    def calculate_sample_mean(self):
        sample_mean = 0
        for i in range(self._number_of_groups):
            sample_mean += self._mean_values[i] * self._relative_frequencies[i]
        return sample_mean

    def calculate_z(self):
        z = []
        for value in self._mean_values:
            z.append(value - self._sample_mean)
        return z

    def calculate_z_2(self):
        return list(map(lambda x: x * x, self._z))

    def calculate_n_accumulated(self):
        n_accumulated = []
        for i in range(1, self._number_of_groups + 1):
            n_accumulated.append(sum(self._numbers_of_each_interval[:i]))
        return n_accumulated

    def calculate_z_3_multiplication_relative_frequencies(self):
        value = []
        for i in range(self._number_of_groups):
            value.append(self._z[i] * self._z[i] * self._z[i] * self._relative_frequencies[i])
        return value

    def calculate_dispersion(self):
        dispersion = 0
        for i in range(self._number_of_groups):
            dispersion += self._z_2[i] * self._numbers_of_each_interval[i]
        return dispersion / self._number

    def calculate_standard_deviation(self):
        return self._dispersion ** 0.5

    def calculate_fashion(self):
        return statistics.mode(self._list)

    def calculate_median(self):
        return statistics.median(self._list)

    def calculate_coefficient_of_asymmetry(self):
        m = sum([i for i in self._z_3_multiplication_relative_frequencies])
        return m / (self._standard_deviation * self._standard_deviation * self._standard_deviation)

    def calculate_coefficient_of_kurtosis(self):
        m = sum([self._z_3_multiplication_relative_frequencies[i] * self._z[i] for i in range(self._number_of_groups)])
        coefficient_of_kurtosis = m / (self._standard_deviation ** 4) - 3
        assert coefficient_of_kurtosis >= -2
        return coefficient_of_kurtosis

    def calculate_coefficient_of_variation(self):
        return (self._standard_deviation * 100) / self._sample_mean

    def calculate_confidence_interval_of_sample_mean(self):
        a = (2.045 * self._standard_deviation) / (self._number ** 0.5)
        return self._sample_mean - a, self._sample_mean + a

    def calculate_confidence_interval_of_dispersion(self):
        chi1 = stats.chi2.ppf(0.975, self._number - 1)
        chi2 = stats.chi2.ppf(0.025, self._number - 1)

        return (
            (self._number - 1) * self._dispersion / chi1,
            (self._number - 1) * self._dispersion / chi2
        )

    def get_plot_components(self):
        x_range = [str([round(i[0], 2), round(i[1], 2)]) for i in self.intervals]
        plot = figure(x_range=x_range)

        plot.vbar(x=x_range,
                  top=self.relative_frequencies,
                  width=1,
                  bottom=0,
                  color="blue",
                  line_color='black')
        return components(plot)

    @property
    def number(self):
        return self._number

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def number_of_groups(self):
        return self._number_of_groups

    @property
    def interval_step(self):
        return self._interval_step

    @property
    def intervals(self):
        return self._intervals

    @property
    def numbers_of_each_interval(self):
        return self._numbers_of_each_interval

    @property
    def mean_values(self):
        return self._mean_values

    @property
    def relative_frequencies(self):
        return self._relative_frequencies

    @property
    def sample_mean(self):
        return self._sample_mean

    @property
    def z(self):
        return self._z

    @property
    def n_accumulated(self):
        return self._n_accumulated

    @property
    def z_3_multiplication_relative_frequencies(self):
        return self._z_3_multiplication_relative_frequencies

    @property
    def standard_deviation(self):
        return self._standard_deviation

    @property
    def dispersion(self):
        return self._dispersion

    @property
    def fashion(self):
        return self._fashion

    @property
    def median(self):
        return self._median

    @property
    def coefficient_of_asymmetry(self):
        return self._coefficient_of_asymmetry

    @property
    def coefficient_of_kurtosis(self):
        return self._coefficient_of_kurtosis

    @property
    def coefficient_of_variation(self):
        return self._coefficient_of_variation

    @property
    def confidence_interval_of_sample_mean(self):
        return self._confidence_interval_of_sample_mean

    @property
    def confidence_interval_of_dispersion(self):
        return self._confidence_interval_of_dispersion

    @property
    def list(self):
        return self._list

    @property
    def z_2(self):
        return self._z_2

    @property
    def name(self):
        return self._name


if __name__ == '__main__':
    pass
