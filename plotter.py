import missingno as msno
import pandas as pd
from scipy.stats import normaltest
from matplotlib import pyplot
from statsmodels.graphics.gofplots import qqplot
import statsmodels.api as sm
import seaborn as sns
import numpy as np


class Plotter:
    def __init__(self, df):
        self.df = df

    # D’Agostino’s K^2 Test
    def agostino_k2_test(self, col):
        stat, p = normaltest(self.df[col], nan_policy='omit')
        print('Statistics=%.3f, p=%.3f' % (stat, p))

    # histogram
    def multi_hist_plot(self, num_cols):
        sns.set(font_scale=0.7)
        f = pd.melt(self.df, value_vars=num_cols)
        g = sns.FacetGrid(f, col="variable", col_wrap=4,
                          sharex=False, sharey=False)
        g = g.map(sns.histplot, "value", kde=True)
        pyplot.show()

    def qq_plot(self, col):
        self.df.sort_values(by=col, ascending=True)
        qq_plot = qqplot(self.df[col], scale=1, line='q')
        pyplot.show()

    # np.ravel flattens the 2d axis array, meaning that we iterate and plot on x:y axis
    def multi_qq_plot(self, cols):
        remainder = 1 if len(cols) % 4 != 0 else 0
        rows = int(len(cols) / 4 + remainder)

        fig, axes = pyplot.subplots(
            ncols=4, nrows=rows, sharex=False, figsize=(12, 6))
        for col, ax in zip(cols, np.ravel(axes)):
            sm.qqplot(self.df[col], line='s', ax=ax, fit=True)
            ax.set_title(f'{col} QQ Plot')
        pyplot.tight_layout()

    def missing_nulls_vis(self):
        msno.matrix(self.df)
        pyplot.show()

    def correlated_vars(self, cols):
        corr = self.df[cols].corr()
        mask = np.zeros_like(corr)
        mask[np.triu_indices_from(mask)] = True
        pyplot.figure(figsize=(10, 8))

        cmap = sns.diverging_palette(220, 10, as_cmap=True)

        sns.heatmap(corr, mask=mask, square=True, linewidths=5,
                    annot=False, cmap=cmap)

        # Show the plot
        pyplot.show()


if __name__ == '__main__':
    df = pd.read_csv('./dataset/formatted_loan_data.csv')
    plt = Plotter(df)

    # int rate has mostly normal distribution
    # plt.agostino_k2_test('int_rate')
    # print(df['int_rate'].median())
    # plt.histogram('int_rate')
    # plt.qq_plot('int_rate')

    plt.missing_nulls_vis()
    # small visible correlation between interest rate, term and loan
    # there is small correlation between missing numerical cols

    numerical_cols = ['loan_amount',
                      'funded_amount_inv', 'int_rate', 'instalment', 'dti', 'total_payment', 'total_accounts', 'mths_since_last_major_derog', 'collections_12_mths_ex_med', 'recoveries', 'open_accounts', 'annual_inc']

    plt.correlated_vars(numerical_cols)

    plt.multi_hist_plot(numerical_cols)