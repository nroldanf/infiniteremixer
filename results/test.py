import pickle

def load_from_pickle(load_path):
    """Deserialize data from pickle file.

    :param load_path: (str) Path of file to load

    :return: (Python obj) Deserialised data
    """
    with open(load_path, "rb") as file:
        data = pickle.load(file)
    return data

if __name__ == "__main__":
    dataset = load_from_pickle("/app/results/dataset/dataset.pkl")
    mapping = load_from_pickle("/app/results/dataset/mapping.pkl")
    print(dataset)
    print(dataset.shape)

    print(mapping)