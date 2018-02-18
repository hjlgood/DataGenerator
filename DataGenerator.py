import numpy as np
import pandas as pd


class DataGenerator():
    """
    This class opens a given file and reads the file line by line.
    use getData method to return Pandas DataFrame or Numpy Arary of each line.
    """

    def __init__(self, file_path):
        """
        Define PATH to the file during instantiation.
        """
        self.file_path = file_path
        self.f = open(self.file_path, 'r')
        self.first_position = self.f.tell()

    def readline(self):
        """
        Lazily read a single line from file_path.

        INPUT : none
        OUTPUT : yield a single line (without '\n')
        """
        for self.line in self.f:
            if self.line[0] == ',':
                yield EOFError
            else:
                yield self.line.splitlines()

    def getData(self, lines=1, dtype='pd'):
        """
        Read each line from file_path and vertically stack each line in Pandas.DataFrame.
        If dtype is set to 'np', this function will return two np.arrays. (numeric data and strings)

        INPUT : number of lines to read , data_type to return = 'pd' or 'np' (default is 'pd)
        OUTPUT : pd.DataFrame of lines OR
                np.array of data, np.array of strings
        """
        # loop through the lines
        for i in range(lines):

            # read a single line and make it as pd.DataFrame
            self.line_as_list_of_strings = next(
                self.readline())  # ['1971.01.04,00:00,0.53690,0.53690,0.53690,0.53690,1']

            # if there is nothing else to read,
            # move the readline() pointer to the start of the file
            # and stop reading lines
            if self.line_as_list_of_strings == EOFError:
                self.f.seek(self.first_position)
                break

            # ['1971.01.04', '00:00', '0.53690', '0.53690', '0.53690', '0.53690', '1']
            self.line_as_list_of_strings = \
                self.line_as_list_of_strings[0].split(",")

            # Pandas DataFrame of a single line
            self.df_single_row = \
                pd.DataFrame(self.line_as_list_of_strings).transpose()

            # concatenate if there are multiple lines
            if i == 0:
                self.df_multiple_rows = self.df_single_row
            else:
                self.df_multiple_rows = \
                    pd.concat([self.df_multiple_rows, self.df_single_row])

        # change every column to floats or ints (only if possible)
        for k in list(self.df_multiple_rows):
            self.df_multiple_rows[[k]] = \
                self.df_multiple_rows[[k]].apply(pd.to_numeric, errors='ignore')

        # if dtype is 'pd' return everything as Pandas DataFrame
        if dtype == 'pd':
            return self.df_multiple_rows.reset_index(drop=True)

        # if dtype is 'np', return np.array of data and np.array of strings
        if dtype == 'np':
            self.np_numbs = \
                np.array(self.df_multiple_rows.select_dtypes(include=['float64', 'int64', 'bool']).values)  # [[],[]]
            self.np_strings = \
                np.array(self.df_multiple_rows.select_dtypes(exclude=['float64', 'int64', 'bool']).values)  # [[],[]]
            return self.np_numbs, self.np_strings

# example usage
#a = DataGenerator("Somefile.csv")
#print(a.getData(lines=100, dtype='pd'))
