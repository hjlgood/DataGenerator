# Data Generator
    Class DataGenerator opens a given file and reads the file line by line.
    use getData method to return Pandas DataFrame or Numpy Arary of each line.



# Example usage
    a = DataGenerator("somefile.csv")
    print(a.getData(lines=10, dtype='pd'))
    print(a.getData(lines=1, dtype='np'))
