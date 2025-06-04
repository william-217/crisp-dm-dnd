import os
import pandas as pd

class DataLoader:
    def __init__(self, base_folder="data/cleaned_datasets"):
        self.base_folder = base_folder

    def list_subfolders(self):
        """Lista as subpastas dentro de cleaned_datasets/"""
        try:
            return [
                f for f in os.listdir(self.base_folder)
                if os.path.isdir(os.path.join(self.base_folder, f))
            ]
        except Exception as e:
            print(f"Erro ao listar subpastas: {e}")
            return []

    def choose_subfolder(self):
        """Permite ao utilizador escolher uma das subpastas"""
        subfolders = self.list_subfolders()
        if not subfolders:
            print("\nNenhuma subpasta encontrada.")
            return None
        print("\nSubpastas disponíveis:")
        for i, name in enumerate(subfolders, 1):
            print(f"{i}: {name}")
        while True:
            try:
                choice = int(input("Selecione o número da subpasta: "))
                if 1 <= choice <= len(subfolders):
                    return os.path.join(self.base_folder, subfolders[choice - 1])
                else:
                    print("Número inválido.")
            except ValueError:
                print("Por favor, introduza um número válido.")

    def list_csv_files(self, folder_path):
        """Lista ficheiros CSV dentro da subpasta selecionada"""
        try:
            return [
                f for f in os.listdir(folder_path)
                if f.endswith('.csv') and os.path.isfile(os.path.join(folder_path, f))
            ]
        except Exception as e:
            print(f"Erro ao listar ficheiros CSV: {e}")
            return []

    def choose_csv_file(self, folder_path):
        """Permite ao utilizador escolher um ficheiro dentro da subpasta"""
        files = self.list_csv_files(folder_path)
        if not files:
            print("Nenhum ficheiro CSV encontrado.")
            return None
        print("\nFicheiros disponíveis:")
        for i, fname in enumerate(files, 1):
            print(f"{i}: {fname}")
        while True:
            try:
                choice = int(input("Selecione o número do ficheiro: "))
                if 1 <= choice <= len(files):
                    return os.path.join(folder_path, files[choice - 1])
                else:
                    print("Número inválido.")
            except ValueError:
                print("Por favor, introduza um número válido.")

    def load_csv(self, file_path):
        """Carrega o ficheiro CSV selecionado"""
        try:
            df = pd.read_csv(file_path)
            print(f"Ficheiro carregado: {file_path} ({df.shape[0]} linhas, {df.shape[1]} colunas)")
            return df
        except Exception as e:
            print(f"Erro ao carregar ficheiro: {e}")
            return None

    def get_file_and_folder_names(self, file_path, folder_path):
        """Obtém o nome do file e da subpasta sem .csv"""
        try:
            nome_ficheiro = os.path.splitext(os.path.basename(file_path))[0]  # sem .csv
            nome_subpasta = os.path.basename(folder_path)
            return nome_ficheiro, nome_subpasta
        except Exception as e:
            print(f"Erro ao obter nomes: {e}")
            return None, None
