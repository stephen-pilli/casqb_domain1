import numpy as np
from scipy.stats import norm
from scipy.stats import fisher_exact
from scipy.stats import chi2_contingency
from statsmodels.stats.contingency_tables import Table2x2

def chi_squared_test(data):
    """
    Perform a chi-squared test on a 2x2 contingency table and calculate sample estimates.

    Parameters:
    data (np.array): 2x2 numpy array representing the observed frequencies.

    Returns:
    dict: A dictionary containing chi-squared statistic, p-value, degrees of freedom,
          expected frequencies, and sample estimates for the two proportions.
    """
    chi2, p, dof, expected = chi2_contingency(data, correction=False)
    
    # Calculate sample estimates (proportions)
    proportion1 = data[0, 0] / (data[0, 0] + data[1, 0])
    proportion2 = data[0, 1] / (data[0, 1] + data[1, 1])
    
    return {
        "chi-squared statistic": np.round(chi2, 2),
        "p-value": 0.001 if p < .001 else np.round(p, 3) ,
        "degrees of freedom": np.round(dof, 2),
        "expected frequencies": np.round(expected, 2),
        "sample estimate for group 1": np.round(proportion1, 2),
        "sample estimate for group 2": np.round(proportion2, 2)
    }

def fisher_exact_test(data):
    """
    Perform Fisher's exact test and calculate the odds ratio and its confidence interval.

    Parameters:
    data (numpy array): A 2x2 contingency table.

    Returns:
    dict: A dictionary containing the odds ratio, p-value, and the 95% confidence interval for the odds ratio.
    """
    # Perform Fisher's exact test to get the odds ratio and p-value
    oddsratio, p_value = fisher_exact(data, alternative='two-sided')
    
    # Calculate the confidence interval for the odds ratio
    table = Table2x2(data)
    ci_low, ci_upp = table.oddsratio_confint()
    
    return {
        'odds_ratio': np.round(oddsratio, 2),
        'p_value': np.round(p_value, 5),
        'ci_95': (np.round(ci_low, 2), np.round(ci_upp, 2))
    }

def cohens_h(x1, x2, n1, n2, ci=0.95):
    """
    Calculate Cohen's h and its confidence interval for the difference between two proportions.

    Parameters:
    x1 (int): Count of successes in the first sample.
    x2 (int): Count of successes in the second sample.
    n1 (int): Size of the first sample.
    n2 (int): Size of the second sample.
    ci (float): Confidence level for the confidence interval (default is 0.95).

    Returns:
    dict: A dictionary with the keys 'h', 'h_low', and 'h_upp' representing
          Cohen's h and the lower and upper bounds of the confidence interval.
    """
    # Calculate the arcsine transformations of the proportions
    arc1 = np.arcsin(np.sqrt(x1 / n1))
    arc2 = np.arcsin(np.sqrt(x2 / n2))
    
    # Calculate the effect size (Cohen's h)
    es = arc1 - arc2
    
    # Calculate the standard error
    se = np.sqrt(0.25 * (1 / n1 + 1 / n2))
    
    # Calculate the critical value for the given confidence interval
    ci_diff = norm.ppf(1 - (1 - ci) / 2) * se
    
    # Return Cohen's h and its confidence interval rounded to 2 decimal places
    return {
        "h": np.round(es * 2, 2),
        "h_low": np.round((es - ci_diff) * 2, 2),
        "h_upp": np.round((es + ci_diff) * 2, 2)
    }


# # Example usage
# observed = np.array([[11, 11],
#                      [18 - 11, 24 - 11]])

# results = chi_squared_test(observed)

# for key, value in results.items():
#     print(f"{key}: {value}")

# # Example usage
# data = np.array([[18, 20],
#                  [63 - 18, 188 - 20]])

# result = fisher_exact_test(data)
# print(f"Odds ratio: {result['odds_ratio']}")
# print(f"P-value: {result['p_value']}")
# print(f"95% CI for the odds ratio: {result['ci_95']}")

# # Example usage:
# result = cohens_h(18, 20, 63, 188)
# print(result)