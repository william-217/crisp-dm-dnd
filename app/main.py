from data_loader import DataLoader
from data_prep import DataPreparation
from models.dummy_classifier import DummyModel
from models.random_forest import RandomForestModel
from models.decision_tree import DecisionTreeModel
from sklearn.model_selection import train_test_split

if __name__ == "__main__":

    # 1. Importar dataset (DataLoader)
    loader = DataLoader(base_folder="data/cleaned_datasets")

    # Escolher subpasta primeiro
    folder = loader.choose_subfolder()
    if not folder:
        exit()

    # Escolher ficheiro dentro da subpasta
    filename = loader.choose_csv_file(folder)
    if not filename:
        exit()

    # Carregar o ficheiro selecionado
    df = loader.load_csv(filename)
    if df is None:
        exit()

    print("\nPrimeiras linhas do dataset:")
    print(df.head())


    # 2. Preparação dos dados (DataPreparation)
    prep = DataPreparation(df)
    prep.interactive_prep()
    target_col = prep.choose_target()
    test_size = prep.choose_split()

    print(f"\nVariável alvo selecionada: {target_col}")
    print(f"Percentagem para teste: {test_size*100:.0f}%")
    print(f"Shuffle: {prep.shuffle}")
    print(f"Random state: {prep.random_state}")
    print(f"Colunas removidas: {prep.removed_cols}")

    # 3. Separar X e y (usar o DataFrame atualizado!)
    X = prep.df.drop(columns=[target_col])
    y = prep.df[target_col]



    # 4. Escolher modelo e treinar/avaliar
    while True:
        print("\nEscolha um modelo:")
        print("1 - DummyClassifier")
        print("2 - Random Forest")
        print("3 - Decision Tree")
        print("0 - Sair")

        choice = input("Selecione o número do modelo: ")

        if choice == '0':
            break
        elif choice == '1':
            model = DummyModel(strategy="most_frequent")
        elif choice == '2':
            model = RandomForestModel()
        elif choice == '3':
            model = DecisionTreeModel()
        else:
            print("Opção inválida.")
            continue

        # dummies nas features - Convert variaveis categóricas em variáveis dummy
        import pandas as pd
        X = pd.get_dummies(X)

        # Split dos dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, shuffle=prep.shuffle, random_state=prep.random_state
        )
        print("Primeiras linhas de X_train:")
        print(X_train.head(20))

        # Treinar e avaliar
        model.train(X_train, y_train)
        model.evaluate(X_test, y_test)