import pandas as pd
from db_utils import RDSDatabaseConnector

class DataFormat:
    def __init__(self, df):
        self.df = df

    def string_to_boolean(self, col_name):
        # Convert 'n' to False and 'y' to True
        mask = {'n': False, 'y': True}
        self.df[col_name].map(mask)
        self.df[col_name] = self.df[col_name].astype('bool')
        print(self.df[col_name].unique())

    def cols_to_categories(self, array):
        # Convert specified columns to categorical type
        for col in array:
            self.df[col] = self.df[col].astype('category')

    def strings_to_dates(self, array):
        # Convert specified columns containing strings to datetime
        for col in array:
            self.df[col] = pd.to_datetime(self.df[col], format="%b-%Y")

    def extract_num_from_string(self, cols):
        # Extract numerical values from strings in specified columns
        for col in cols:
            self.df[col] = self.df[col].str.extract('(\d+)')

    def numerical_cols(self, cols):
        # Convert specified columns to numeric type (but missing assignment to df)
        for col in cols:
            pd.to_numeric(self.df[col])

    def rename(self, col_name, new_col_name):
        # Rename specified column
        self.df.rename(columns={col_name: new_col_name})

    def drop_cols(self, cols):
        # Drop specified columns from the DataFrame
        for col in cols:
            self.df.drop(col, axis=1, inplace=True)

    def round_float(self, col, decimal_places):
        # Round values in specified column to a specified number of decimal places
        self.df[col] = self.df[col].apply(lambda x: round(x, decimal_places))

    # despite type coercion we might want to convert explicitly if exporting to excel for cleanliness
    def to_int(self, cols):
        # Convert specified columns to integer type after filling missing values with 0
        for col in cols:
            self.df[col] = self.df[col].fillna(0).astype('int32')


if __name__ == '__main__':
    df = pd.read_csv('./dataset/loan_data.csv')
    Transformer = DataFormat(df)

    # Convert 'n' and 'y' to bool values in the 'payment_plan' column
    Transformer.string_to_boolean('payment_plan')

    categories = ['grade', 'sub_grade', 'home_ownership',
                  'verification_status', 'loan_status', 'purpose', 'employment_length']

    # Convert specified columns to categorical type
    Transformer.cols_to_categories(categories)

    string_dates = ['last_credit_pull_date', 'next_payment_date',
                    'last_payment_date', 'earliest_credit_line', 'issue_date']

    # Convert specified columns containing strings to datetime
    Transformer.strings_to_dates(string_dates)

    # month and year terms to int
    string_to_num_cols = ['term']
    numerical_cols = ['term', 'mths_since_last_record',
                      'mths_since_last_major_derog', 'mths_since_last_delinq', 'mths_since_last_record']

    # Rename columns for clarity
    Transformer.rename('employment_length', 'Years Employed')
    Transformer.rename('term', 'Loan Months')

    # Extract numerical values from strings in specified columns
    Transformer.extract_num_from_string(string_to_num_cols)
    # Convert specified columns to numeric type
    Transformer.numerical_cols(numerical_cols)

    # Drop unnecessary columns
    drop_cols = ['funded_amount', 'application_type',
                 'policy_code', 'out_prncp_inv', 'total_payment_inv', 'Unnamed: 0', 'id']
    Transformer.drop_cols(drop_cols)

    # we don't convert these cols: 'mths_since_last_record', 'mths_since_last_major_derog' to int since they include 0 months since last to signify recent entry and null for NO entry
    # Convert specified columns to integer type after filling missing values with 0
    Transformer.to_int(['term', 'open_accounts', 'total_accounts',
                       'collections_12_mths_ex_med', 'delinq_2yrs', 'loan_amount'])

    # Round values in specified column to 2 decimal places
    Transformer.round_float('collection_recovery_fee', 2)

    # Print data types and information about the DataFrame
    print(Transformer.df.dtypes)
    print(Transformer.df.info())
    
    # Save formatted DataFrame to CSV using the RDSDatabaseConnector
    RDSDatabaseConnector.save_to_csv(Transformer.df, 'formatted_loan_data.csv')
