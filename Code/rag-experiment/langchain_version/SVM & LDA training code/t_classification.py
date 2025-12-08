# import pandas as pd
# from classification import SecurityQuestionClassifier
#
# df = pd.read_excel("StackOverflow_security_sample_labelled.xlsx")
#
# # Instantiate the classifier and train it
# clf = SecurityQuestionClassifier()
# clf.train(df)
# clf.save_model("svm_classifier.joblib")

from classification import SecurityQuestionClassifier

# Loading the trained model
clf = SecurityQuestionClassifier(model_path="svm_classifier.joblib")

# Test input a question
question = "How to implement authentication using JWT in Flask?"
label = clf.predict(question)

print(f"Questions are categorized as：{label}")
