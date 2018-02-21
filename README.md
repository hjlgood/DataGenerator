# Data Generator
    Class DataGenerator opens a given file and reads the file line by line.
    use getData method to return Pandas DataFrame or Numpy Arary of each line.



# Example usage
     file = "some_file_path.csv"
     
     a = DataGenerator(file, deliminator=',')
     print('Reading file incrementally. ------------------------------')
     print(a.get_data(lines=3, dtype='df', readtype='incremental'))
     print(a.get_data(lines=3, dtype='df', readtype='incremental'))
     print(a.get_data(lines=3, dtype='df', readtype='incremental'))
     print('Reading file as batch. ----------------------------------')
    
     b = DataGenerator(file, deliminator=',')
     print(b.get_data(lines=3, dtype='np', readtype='batch'))
     print(b.get_data(lines=3, dtype='np', readtype='batch'))
     print(b.get_data(lines=3, dtype='np', readtype='batch'))
     print('---------------------------------------------------------')
