import math
import numpy.random as npr
import pandas as pd
import scipy.stats as stat

def test_code(annualised_mean, annualised_sd):
    working_days_per_year = 256.0
    sqrt_time = math.sqrt(working_days_per_year)
    daily_mean = annualised_mean / working_days_per_year
    daily_sd = annualised_sd / sqrt_time
    daily_sharp = daily_mean / daily_sd
    annualised_sharp = annualised_mean / annualised_sd

    n = 10000
    daily_returns = npr.normal(daily_mean, daily_sd, n)

    def norm_cdf(ret):
        if ret > 0:
            return (1 - stat.norm.cdf(ret, daily_mean, daily_sd)) * n
        else:
            return stat.norm.cdf(ret, daily_mean, daily_sd) * n

    def return_count(ret):
        if ret > 0:
            return (daily_returns > ret).sum()
        else:
            return (daily_returns <= ret).sum()

    sigmas = [-3, -2, -1, 1, 2, 3]
    expected_ret = map(lambda sigma: daily_mean + daily_sd * sigma, sigmas)
    expected_count = map(norm_cdf, expected_ret)
    actual_count = map(return_count, expected_ret)

    data = {'expected return': expected_ret,
            'expected count': expected_count,
            'actual count': actual_count}

    return pd.DataFrame(index=sigmas, data=data)
    pass



if __name__ == "__main__":
    df = test_code(2, 2)
    df.head()
