from sklearn.ensemble import RandomForestClassifier
from .base_model import BaseModel
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import matplotlib.pyplot as plt

class RandomForestModel(BaseModel):
    def __init__(self, n_estimators=300, max_depth=None, class_weight="balanced_subsample", random_state=42, **kwargs):
        super().__init__()
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            class_weight=class_weight,
            random_state=random_state,
            **kwargs
        )

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print(classification_report(y_test, y_pred))
        # Mostra a matriz de confusão para as 10 classes mais comuns
        labels = list(pd.Series(y_test).value_counts().index[:10])
        print(f"Mostrando matriz de confusão para as 10 classes mais comuns: {labels}")
        self.plot_confusion(y_test, y_pred, labels=labels)

    def plot_feature_importance(self, feature_names):
        importances = pd.Series(self.model.feature_importances_, index=feature_names)
        importances.sort_values().plot(kind='barh', figsize=(8, 5))
        plt.title("Importância das Variáveis")
        plt.tight_layout()
        plt.show()