"""

    Machine Learning Project Work: Tennis Table Tournament
    Group 2:
        Ciaravola Giosuè - g.ciaravola3@studenti.unisa.it
        Conato Christian - c.conato@studenti.unisa.it
        Del Gaudio Nunzio - n.delgaudio5@studenti.unisa.it
        Garofalo Mariachiara - m.garofalo38@studenti.unisa.it

    ---------------------------------------------------------------

    dataset_loader.py

    File containing the class responsible for loading the dataset and
    splitting it into training, testing, and validation sets,
    providing their respective loaders.

"""

import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset
from torch.utils.data import DataLoader, TensorDataset

# Set the device to GPU if available, otherwise use CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Define custom dataset
class ArmDataset(Dataset):
    def __init__(self, csv_file, batch_size=124, seed=3, train_size=0.5, val_size=0.5):
        """
        Initialize the ArmDataset.

        Args:
            csv_file (str): Path to the CSV file containing the dataset.
            batch_size (int): Batch size for the DataLoader.
            seed (int): Random seed for reproducibility.
            train_size (float): Proportion of the dataset to include in the train split.
            val_size (float): Proportion of the train split to include in the validation split.
        """

        # Load the dataset from the CSV file
        data_set = pd.read_csv(csv_file)

        # Split the dataset into input features and target features
        target = data_set.iloc[:, :-2]
        input = data_set.iloc[:, 4:6]

        # Split the dataset into training and sub_test sets
        input_train, input_sub_test, target_train, target_sub_test = train_test_split(input, target, test_size=train_size, random_state=seed)

        # Split the sub_test set into test and validation sets
        input_test, input_val, target_test, target_val = train_test_split(input_sub_test, target_sub_test, test_size=val_size, random_state=seed)

        # Convert the input features to numpy arrays
        input_train_np = input_train.to_numpy()
        input_test_np = input_test.to_numpy()
        input_val_np = input_val.to_numpy()

        # Convert the target features to numpy arrays
        target_train_np = target_train.to_numpy()
        target_test_np = target_test.to_numpy()
        target_val_np = target_val.to_numpy()

        # Convert the input features to torch tensors
        input_train = torch.tensor(input_train_np, dtype=torch.float32).to(device)
        input_test = torch.tensor(input_test_np, dtype=torch.float32).to(device)
        input_val = torch.tensor(input_val_np, dtype=torch.float32).to(device)

        # Convert the target features to torch tensors
        target_train = torch.tensor(target_train_np, dtype=torch.float32).to(device)
        target_test = torch.tensor(target_test_np, dtype=torch.float32).to(device)
        target_val = torch.tensor(target_val_np, dtype=torch.float32).to(device)

        # Create TensorDatasets for training, testing, and validation
        train_dataset = TensorDataset(input_train, target_train)
        test_dataset = TensorDataset(input_test, target_test)
        validation_dataset = TensorDataset(input_val, target_val)

        # Create DataLoaders for training, testing, and validation
        self.train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        self.test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
        self.val_loader = DataLoader(validation_dataset, batch_size=batch_size, shuffle=False)
