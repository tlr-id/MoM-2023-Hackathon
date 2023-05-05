import pickle
#Function that opens pickle file and returns a dataframe
def load_file(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)



#Get 5 lines of the dataframe   
df = load_file('data/files_essentia_effnet-discogs.jsonl.pickle')
print(df.head())