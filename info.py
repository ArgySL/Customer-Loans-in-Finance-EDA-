from db_utils import load_data
from tabulate import tabulate

class DataFrameInfo:
    def __init__(self, df):
        self.df = df

    def describe_columns(self):
        # Return data types of each column in the DataFrame
        return self.df.dtypes

    def extract_statistics(self, columns):
        # Print and return descriptive statistics for specified columns
        for col in columns:
            print(f"Statistics for Col: {col}")
            return self.df[col].describe()

    def skew_data(self, cols):
        # Calculate and print skewness for specified columns
        skew_data = []
        for col in cols:
            skew_value = self.df[col].skew()
            skew_data.append([col, skew_value])

        print(tabulate(skew_data, headers=[
              "Column", "Skewness"], tablefmt="pretty"))

    def distinct_values(self, cols):
        # Print and return the number of unique values for specified columns
        unique_values = {}
        for col in cols:
            print(f"Unique values for col: {col}\n")
            unique_values[col] = self.df[col].nunique()
        return unique_values

    def get_shape(self):
        # Print and return the shape of the DataFrame
        print("Dataframe Shape:")
        return self.df.shape

    def percentage_null(self):
        # Calculate and return the percentage of null values for each column
        null_percentages = (self.df.isna().sum() * 100 / len(self.df)).to_frame(name="% Null")
        non_zero_null_percentages = null_percentages[null_percentages["% Null"] > 0]
        return non_zero_null_percentages


if __name__ == '__main__':
    # Load data from the specified CSV file
    df = load_data("/dataset/formatted_loan_data.csv")
    Info = DataFrameInfo(df)

    # Print and return descriptive statistics for 'loan_amount'
    print(Info.extract_statistics(['loan_amount']))

    # Print and return the number of unique values for 'grade'
    print(Info.distinct_values(['grade']))

    # Print and return the shape of the DataFrame
    print(Info.get_shape())

    # Print and return the percentage of null values for each column
    print(Info.percentage_null())

    # Print data types of each column in the DataFrame
    print(Info.describe_columns())

    # Print and return descriptive statistics for 'mths_since_last_major_derog'
    print(Info.extract_statistics(['mths_since_last_major_derog']))
