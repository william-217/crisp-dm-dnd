import os
import pandas as pd
from data_loader import DataLoader
from data_prep import DataPreparation
from models.dummy_classifier import DummyModel
from models.random_forest import RandomForestModel
from models.decision_tree import DecisionTreeModel
from sklearn.model_selection import train_test_split

if __name__ == "__main__":

    # 1 Escolher a pasta base
    print("Escolha a origem dos dados:")
    print("1 - cleaned_datasets_repeated_entries")
    print("2 - cleaned_datasets")
    print("0 - Sair")

    folder_choice = input("Selecione o número da pasta: ").strip()
    if folder_choice == "1":
        base_folder = "data/cleaned_datasets_repeated_entries"
    elif folder_choice == "2":
        base_folder = "data/cleaned_datasets"
    elif folder_choice == "0":
        print("A sair...")
        exit()
    else:
        print("Opção inválida. A sair.")
        exit()

    # verificação se é pasta com ou sem duplicados
    if folder_choice == "1":
        duplicados = True 
    else:
        duplicados = False

    # 2. Iniciar Dataloader com a pasta escolhida
    loader = DataLoader(base_folder=base_folder)

    # 3. Escolher subpasta dos dados
    folder = loader.choose_subfolder()
    if not folder:
        exit()

    # 4.Escolher ficheiro dentro da subpasta
    filename = loader.choose_csv_file(folder)
    if not filename:
        exit()
    
    # Guardar o nome do ficheiro e subpasta para confusion matrix e feature importance
    nome_ficheiro = os.path.splitext(os.path.basename(filename))[0]
    nome_subpasta = os.path.basename(folder)

    #5. Carregar o ficheiro selecionado
    df = loader.load_csv(filename)
    if df is None:
        exit()

    # 6. Mostrar primeiras linhas e estatísticas do dataset
    print("\nPrimeiras linhas do dataset:")
    print(df.head())
    print("\nEstatísticas descritivas do dataset:")
    print(df.describe(include='all'))


    # 7. Preparação dos dados (DataPrep)
    prep = DataPreparation(df)
    prep.interactive_prep()
    target_col = prep.choose_target()
    test_size = prep.choose_split()

    print(f"\nVariável alvo selecionada: {target_col}")
    print(f"Percentagem para teste: {test_size*100:.0f}%")
    print(f"Shuffle: {prep.shuffle}")
    print(f"Random state: {prep.random_state}")
    print(f"Colunas removidas: {prep.removed_cols}")

    # 8. Separar X e y (usar o DataFrame atualizado!)
    X = prep.df.drop(columns=[target_col])
    y = prep.df[target_col]
    x = pd.get_dummies(X) # alterado para usar o DataFrame atualizado


    # 9. Escolher modelo e treinar/avaliar
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
            model = DummyModel()
        elif choice == '2':
            model = RandomForestModel()
        elif choice == '3':
            model = DecisionTreeModel()
        else:
            print("Opção inválida.")
            continue

        import pandas as pd
        X = pd.get_dummies(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, shuffle=prep.shuffle, random_state=prep.random_state
        )
        print("\nPrimeiras linhas de X_train:")
        print(X_train.head(20))
        print("\nPrimeiras linhas de y_train:")
        print(y_train.head(20))
     

        # Menu dos parametros dos modelos
        while True:
            print("\nO que pretende fazer com o modelo?")
            print("1 - Ver parâmetros atuais")
            print("2 - Alterar parâmetros")
            print("3 - Treinar e avaliar")
            print("0 - Voltar à escolha do modelo")
            op = input("Escolha a opção: ")

            if op == "1":
                model.show_params()
            elif op == "2":
                params = model.ask_params()
                model.set_params(**params)
                print("Parâmetros atualizados.")
            elif op == "3":
                model.train(X_train, y_train)
                # debug para as labels (agora já existe classes_)
                print("Exemplo y_train:", y_train.head())
                print("Tipo y_train:", y_train.dtype)
                print("Classes do modelo:", model.model.classes_)
                model.print_classification_report(X_test, y_test)
                model.plot_confusion_all(
                    X_test, y_test,
                    filename=nome_ficheiro,
                    subfolder=nome_subpasta,
                    duplicados=duplicados
                )
                # Se for RandomForest, mostrar a importancia das features:
                if hasattr(model, "plot_feature_importance"):
                    model.plot_feature_importance(X_train.columns)
                # Se for DecisionTree, mostrar a árvore:
                if hasattr(model, "plot_tree_diagram"):
                    model.plot_tree_diagram(list(X_train.columns))
            elif op == "0":
                break
            else:
                print("Opção inválida.")

    def plot_confusion_all(self, X_test, y_test, filename=None, subfolder=None, duplicados=None):
        y_pred = self.predict(X_test)
        if hasattr(self.model, "classes_"):
            labels = [str(l) for l in self.model.classes_]
        else:
            labels = [str(l) for l in pd.unique(y_test)]
        self.plot_confusion(
            y_test, y_pred,
            labels=labels,
            filename=filename,
            subfolder=subfolder,
            duplicados=duplicados
        )

