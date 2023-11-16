import pickle

def load_model(file_path):
    with open(file_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Load the models when this module is imported
cosine_sim = load_model('models/cosine_similarity.pkl')
csr_data = load_model('models/csr_data.pkl')
final_dataset = load_model('models/final_dataset.pkl')
knn = load_model('models/knn.pkl')
movies = load_model('models/movies.pkl')
