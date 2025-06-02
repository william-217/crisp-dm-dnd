from sklearn.dummy import DummyClassifier
from .base_model import BaseModel
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

class DummyModel(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = DummyClassifier(**kwargs)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print(classification_report(y_test, y_pred))
        # Mostra a matriz de confusão para as 10 classes mais comuns
        labels = list(pd.Series(y_test).value_counts().index[:10])
        print(f"Mostrando matriz de confusão para as 10 classes mais comuns: {labels}")
        self.plot_confusion(y_test, y_pred, labels=labels)
    
    