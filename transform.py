import pandas as pd
from format import DataFormat
from plotter import Plotter
import seaborn as sns
import numpy as np
from scipy import stats


class DataFrameTransform:
    def __init__(self, df):
        self.df = df

    def impute_zeros(self, cols):
        for col in cols:
            self.df[col] = self.df[col].fillna(0)

    def impute_median(self, cols):
        for col in cols:
            self.df[col] = self.df[col].fillna(self.df[col].median())

    def impute_mean(self, cols):
        for col in cols:
            self.df[col] = self.df[col].fillna(self.df[col].mean())

    def drop_null_rows(self, cols):
        self.df.dropna(subset=cols, inplace=True)

    def log_transform(self, cols):
        """
        Apply a natural logarithm transformation to specified columns.

        Parameters:
        - cols (list): A list of column names to undergo the logarithmic transformation.

        Returns:
        None
        """
        for col in cols:
            self.df[col] = self.df[col].map(
                lambda x: np.log(x) if x > 0 else 0)

    def box_cox_transform(self, cols):
        """
        Apply the Box-Cox transformation to specified columns.

        The Box-Cox transformation is a family of power transformations that are useful
        when dealing with non-constant variance and non-normality in statistical data.

        Parameters:
        - cols (list): A list of column names to undergo the Box-Cox transformation.

        Returns:
        None
        """
        for col in cols:
            # Adding a small constant (e.g., 0.01) to ensure all values are positive
            transformed_col = self.df[col] + 0.01
            a, b = stats.boxcox(transformed_col)
            self.df[col] = a


if __name__ == "__main__":
    df = pd.read_csv('./dataset/formatted_loan_data.csv')
    format = DataFormat(df)
    t_form = DataFrameTransform(format.df)
    plotter = Plotter(t_form.df)

    # NMAR
    # missing employment length likely means unemployed so impute 0
    t_form.impute_zeros(['employment_length'])

    # mean interest rate since its within normal dist
    t_form.impute_median(['int_rate'])

    # there are 57% and 88% missing values, imputing could be risky to make up such a substantial amount of data
    # issue with
    format.drop_cols(
        ['mths_since_last_record', 'mths_since_last_delinq', 'next_payment_date', 'mths_since_last_major_derog'])

    # these rows have insignificant null vals
    t_form.drop_null_rows(['last_payment_date', 'last_credit_pull_date'])

    plotter.missing_nulls_vis()