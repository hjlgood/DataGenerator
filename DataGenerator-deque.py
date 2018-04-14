import numpy as np
import pandas as pd
import sys, os
from collections import deque

class DataGenerator(object):
    """
    This class opens a given file and reads the file line by line.
    use getData method to return Pandas DataFrame or Numpy Array of each line.
    """

    def __init__(self, file_path, deliminator=',', maxlines = 1):
        """
        Define PATH to the file during instantiation.
        Define deliminator (default is ,)
        """
        self.file_path = file_path
        self.f = open(self.file_path, 'r')
        self.first_position = self.f.tell()
        self.deliminator = deliminator
        self.maxlines = maxlines
        self.getDataCounter = 0
        self.tunnel = deque(maxlen = maxlines)

    @property
    def load_a_line(self):
        """
        Lazily read a single line from file_path.
        INPUT : none
        OUTPUT : yield a single line as list of string (without '\n')
                ['1971.01.04,00:00,0.53690,0.53690,0.53690,0.53690,1']
        """
        for self.line in self.f:
            if self.line[0] == self.deliminator:
                yield EOFError
            else:
                self.line = self.line.splitlines()
                self.line = self.line[0].split(self.deliminator)
                self.line = pd.Series(self.line).apply(pd.to_numeric,errors='ignore').tolist()
                yield self.line

    def read_lines(self):
                
        line_as_list_of_strings = next(self.load_a_line)        
       
        if line_as_list_of_strings == EOFError:
            print('end of file. move to first position')
            self.f.seek(self.first_position)
            self.tunnel.clear() 
            line_as_list_of_strings = next(self.load_a_line)        
 
        elif len(self.tunnel) < self.maxlines:


        else:
            print('fill the tunnel')
            self.tunnel.append(line_as_list_of_strings)     
            

        self.getDataCounter += 1
        
        return list(self.tunnel)



# # example usage
if __name__== "__main__":
    path = sys.argv[0].split(os.path.basename(__file__))[0]
    input_path = 'EURUSD1440R.csv'
    file = path+input_path
    
    a = DataGenerator(file, deliminator=',',maxlines=3)
    print('Reading file incrementally. ------------------------------')
    for i in range(10):
        print(i, "th iteration")
        a.read_lines()
    print('End of Main()---------------------------------------------')
