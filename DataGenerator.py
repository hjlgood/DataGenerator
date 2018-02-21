import numpy as np
import pandas as pd


class DataGenerator(object):
    """
    This class opens a given file and reads the file line by line.
    use getData method to return Pandas DataFrame or Numpy Array of each line.
    """

    def __init__(self, file_path, deliminator=','):
        """
        Define PATH to the file during instantiation.
        Define deliminator (default is ,)
        """
        self.file_path = file_path
        self.f = open(self.file_path, 'r')
        self.first_position = self.f.tell()
        self.deliminator = deliminator
        self.getDataCounter = 0
        self.df_multiple_rows = pd.DataFrame()

    def read_lines(self, lines):
        """
        Loop through each lines,
        cut single line of string into multiple columns,
        and concatenate it to Pandas DataFrame.

        Input : number of lines to read
        Output : none
        Side-effect : class variable self.df_multiple_lines is altered
        """
        for i in range(lines):
            # read a single line and make it as pd.DataFrame
            line_as_list_of_string = next(
                self.readline)  # ['1971.01.04,00:00,0.53690,0.53690,0.53690,0.53690,1']
            # if there is nothing else to read,
            # move the readline() pointer to the start of the file
            # and stop reading lines
            if line_as_list_of_string == EOFError:
                self.f.seek(self.first_position)
                break
            self.make_string_to_dataframe(line_as_list_of_string)

    @property
    def readline(self):
        """
        Lazily read a single line from file_path.
        INPUT : none
        OUTPUT : yield a single line (without '\n')
        """
        for self.line in self.f:
            if self.line[0] == self.deliminator:
                yield EOFError
            else:
                yield self.line.splitlines()

    def make_string_to_dataframe(self, line_as_list_of_strings):
        # ['1971.01.04', '00:00', '0.53690', '0.53690', '0.53690', '0.53690', '1']
        line_as_list_of_strings = \
            line_as_list_of_strings[0].split(self.deliminator)
        # Pandas DataFrame of a single line
        df_single_row = \
            pd.DataFrame(line_as_list_of_strings).transpose()
        # Concatenate single line to self.df_multiple_rows
        self.df_multiple_rows = pd.concat([self.df_multiple_rows, df_single_row])

    def change_columns_to_numeric(self, df):
        # change every column to floats or ints (only if possible)
        for k in list(df):
            df[[k]] = \
                df[[k]].apply(pd.to_numeric, errors='ignore')
        self.df_multiple_rows = df

    def return_pd_or_np(self, dtype):
        # if dtype is 'pd' return everything as Pandas DataFrame
        if dtype == 'df':
            return self.df_multiple_rows.reset_index(drop=True)
        # if dtype is 'np', return np.array of data and np.array of strings
        if dtype == 'np':
            np_numbs = \
                np.array(self.df_multiple_rows.select_dtypes(include=['float64', 'int64', 'bool']).values)  # [[],[]]
            np_strings = \
                np.array(self.df_multiple_rows.select_dtypes(exclude=['float64', 'int64', 'bool']).values)  # [[],[]]
            return np_numbs, np_strings

    def get_data(self, lines=1, dtype='df', readtype='batch'):
        """
        Read each line from file_path and vertically stack it to Pandas.DataFrame.
        If dtype is set to 'df', this function will return a Pandas.DataFrame.
        If dtype is set to 'np', this function will return two np.arrays. (numeric data and strings)
        If readtype is 'batch', the program will return next batch upon next call.
        If readtype is 'incremental', the program will return next batch FROM SECOND LINE OF FILE.
                                                                    Then THIRD LINE OF FILE. etc.

        INPUT : number of lines to read ,
                data_type to return = 'df' or 'np' (default is 'df'),
                readtype (default is 'batch')
        OUTPUT : pd.DataFrame OR
                np.array of numeric data, np.array of strings
        """
        if readtype == 'batch':
            self.read_lines(lines)
            self.change_columns_to_numeric(self.df_multiple_rows)
            if self.getDataCounter == 0:
                self.getDataCounter += 1
                return self.return_pd_or_np(dtype)
            else:
                self.df_multiple_rows = self.df_multiple_rows[lines:]
                self.getDataCounter += 1
                return self.return_pd_or_np(dtype)

        if readtype == 'incremental':
            if self.getDataCounter == 0:
                self.read_lines(lines)
                self.change_columns_to_numeric(self.df_multiple_rows)
                self.getDataCounter += 1
                return self.return_pd_or_np(dtype)
            else:
                self.read_lines(1)
                self.change_columns_to_numeric(self.df_multiple_rows)
                self.df_multiple_rows = self.df_multiple_rows[1:]
                self.getDataCounter += 1
                return self.return_pd_or_np(dtype)


# example usage
# file = "some_file_path.csv"
# a = DataGenerator(file, deliminator=',')
# print('Reading file incrementally. ------------------------------')
# print(a.get_data(lines=3, dtype='df', readtype='incremental'))
# print(a.get_data(lines=3, dtype='df', readtype='incremental'))
# print(a.get_data(lines=3, dtype='df', readtype='incremental'))
# print('Reading file as batch. ----------------------------------')
# b = DataGenerator(file, deliminator=',')
# print(b.get_data(lines=3, dtype='np', readtype='batch'))
# print(b.get_data(lines=3, dtype='np', readtype='batch'))
# print(b.get_data(lines=3, dtype='np', readtype='batch'))
# print('---------------------------------------------------------')
