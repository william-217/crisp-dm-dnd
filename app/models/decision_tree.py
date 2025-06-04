from sklearn.tree import DecisionTreeClassifier
from .base_model import BaseModel
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import plot_tree
from matplotlib import pyplot as plt
class DecisionTreeModel(BaseModel):
    DEFAULT_PARAMS = {
        **BaseModel.DEFAULT_PARAMS,  # herda os do base
        "criterion": "entropy",         # melhor separação em classes desbalanceadas
        "max_depth": 10,                # evita overfitting segundo o livro
        "min_samples_split": 10,        # mínimo de amostras para dividir
        "min_samples_leaf": 5,          # mínimo de amostras por folha
        "class_weight": "balanced",     # muito importante neste caso
        
    }

    def __init__(self, **params):
        super().__init__()
        self.params = self.DEFAULT_PARAMS.copy()
        self.params.update(params)
        self.model = DecisionTreeClassifier(**self.params)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def set_params(self, **params):
        self.params.update(params)
        self.model = DecisionTreeClassifier(**self.params)

    @staticmethod
    def ask_params():
        print("\n--- Parâmetros do DecisionTree ---")
        params = {}
        # criterion
        crit = input("criterion (gini/entropy/log_loss, ENTER para 'entropy'): ").strip().lower()
        params["criterion"] = crit if crit in ["gini", "entropy", "log_loss"] else "entropy"
        # max_depth
        max_depth_in = input("max_depth (ENTER para 10): ").strip()
        params["max_depth"] = int(max_depth_in) if max_depth_in else 10
        # min_samples_split
        min_split_in = input("min_samples_split (ENTER para 10): ").strip()
        params["min_samples_split"] = int(min_split_in) if min_split_in else 10
        # min_samples_leaf
        min_leaf_in = input("min_samples_leaf (ENTER para 5): ").strip()
        params["min_samples_leaf"] = int(min_leaf_in) if min_leaf_in else 5
        # class_weight
        cw = input("class_weight (None/balanced, ENTER para 'balanced'): ").strip().lower()
        params["class_weight"] = cw if cw in ["none", "balanced"] else "balanced"
        if params["class_weight"] == "none":
            params["class_weight"] = None
        # random_state
        random_state_in = input("random_state (ENTER para 42): ").strip()
        params["random_state"] = int(random_state_in) if random_state_in else 42
        return params

    def plot_tree_diagram(self, feature_names):
        """Mostra e guarda a árvore de decisão treinada."""
        plt.figure(figsize=(20, 10))
        plot_tree(
            self.model,
            filled=True,
            rounded=True,
            feature_names=feature_names,
            class_names=[str(c) for c in self.model.classes_],
            fontsize=10
        )
        plt.title("Árvore de Decisão (critério: {})".format(self.params.get("criterion", "")))
        plt.tight_layout()
        plt.savefig("arvore_decisao_dnd.png", dpi=300)
        plt.show()
