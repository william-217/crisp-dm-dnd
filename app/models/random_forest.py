from sklearn.ensemble import RandomForestClassifier
from .base_model import BaseModel
from sklearn.metrics import accuracy_score, classification_report

class RandomForestModel(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = RandomForestClassifier(**kwargs)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print(classification_report(y_test, y_pred))