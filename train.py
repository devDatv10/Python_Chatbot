import os
import json
import re
import nltk
import pickle
import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from gensim.models import Word2Vec
from underthesea import word_tokenize
from collections import Counter


nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('vietnamese'))

keyword_dict = {
    "macbook": "Macbook",
    "lenovo": "Lenovo",
    "acer": "Acer",
    "asus": "Asus",
    "card": "Card màn hình",
    "ram": "Dung lượng RAM",
    "cpu": "Chip xử lý",
    "ssd": "Ổ cứng SSD",
    "bao nhiêu" : "Giá cả",
    "triệu" : "Giá cả",
    "pin": "Pin và thời lượng sử dụng",
    "bảo hành": "Chính sách bảo hành",
    "giá": "Giá cả",
    "hiệu suất": "Hiệu suất và hiệu năng",
    "thiết kế đồ họa" : "Card đồ họa và Công nghệ màn hình",

}

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().lower()

def get_topic(text):
    for keyword, topic in keyword_dict.items():
        if keyword in text:
            return topic
    return "Khác"

def preprocess_data(sentences):
    processed_sentences = []
    topics = []
    for sentence in sentences:
        words = word_tokenize(clean_text(sentence), format="text")
        filtered_words = [w for w in words.split() if w not in stop_words]
        processed_text = " ".join(filtered_words)
        processed_sentences.append(processed_text)
        topics.append(get_topic(processed_text))
    return processed_sentences, topics

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
file_path = os.path.join(BASE_DIR, "src", "data", "json", "dataset.json")

dataset = load_data(file_path)
questions = list(set([data['question'] for data in dataset]))
answers = [' '.join(map(clean_text, data['answers'])) for data in dataset]

preprocessed_questions, topics = preprocess_data(questions)

unique_topics = list(set(topics))
topic_map = {topic: i for i, topic in enumerate(unique_topics)}
y_labels = [topic_map[topic] for topic in topics]

# Chia tập dữ liệu
X_train, X_test, y_train, y_test = train_test_split(
    preprocessed_questions, y_labels, test_size=0.1, random_state=42
)

# Vectorization (TF-IDF)
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train RandomForest với GridSearchCV
param_grid = {'n_estimators': [100, 200], 'max_depth': [None, 10]}
kf = KFold(n_splits=min(3, len(y_train)), shuffle=True, random_state=42)
rf_model = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=kf)
rf_model.fit(X_train_tfidf, y_train)

# Train Word2Vec
sentences = [sentence.split() for sentence in preprocessed_questions]
word2vec_model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

def sentence_to_vec(sentence, model):
    words = sentence.split()
    word_vectors = [model.wv[word] for word in words if word in model.wv]
    return np.mean(word_vectors, axis=0) if word_vectors else np.zeros(model.vector_size)

X_train_w2v = np.array([sentence_to_vec(q, word2vec_model) for q in X_train])
X_test_w2v = np.array([sentence_to_vec(q, word2vec_model) for q in X_test])

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy, precision, recall, f1

# Đánh giá RandomForest
accuracy, precision, recall, f1 = evaluate_model(rf_model, X_test_tfidf, y_test)
print(f'RandomForest - Accuracy: {accuracy:.2f}, Precision: {precision:.2f}, Recall: {recall:.2f}, F1-score: {f1:.2f}')

# Huấn luyện các mô hình khác
nb_model = MultinomialNB()
nb_model.fit(X_train_tfidf, y_train)

logistic_model = LogisticRegression(max_iter=1000)
logistic_model.fit(X_train_tfidf, y_train)

# Đánh giá các mô hình
nb_results = evaluate_model(nb_model, X_test_tfidf, y_test)
logistic_results = evaluate_model(logistic_model, X_test_tfidf, y_test)
print(f'Naive Bayes - Accuracy: {nb_results[0]:.2f}, Precision: {nb_results[1]:.2f}, Recall: {nb_results[2]:.2f}, F1-score: {nb_results[3]:.2f}')
print(f'Logistic Regression - Accuracy: {logistic_results[0]:.2f}, Precision: {logistic_results[1]:.2f}, Recall: {logistic_results[2]:.2f}, F1-score: {logistic_results[3]:.2f}')

model_dir = "./src/models"
os.makedirs(model_dir, exist_ok=True)

with open(os.path.join(model_dir, "random_forest.pkl"), "wb") as f:
    pickle.dump(rf_model, f)

with open(os.path.join(model_dir, "naive_bayes.pkl"), "wb") as f:
    pickle.dump(nb_model, f)

with open(os.path.join(model_dir, "logistic_regression.pkl"), "wb") as f:
    pickle.dump(logistic_model, f)

word2vec_model.save(os.path.join(model_dir, "word2vec.model"))

with open(os.path.join(model_dir, "tfidf_vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print("Đã lưu tất cả mô hình vào thư mục 'models'.")

def predict_answer(question, vectorizer, model, topic_map, word2vec_model, answers):
    cleaned_question = preprocess_data([question])[0][0]
    question_vector = vectorizer.transform([cleaned_question])
    predicted_topic_id = model.predict(question_vector)[0]
    predicted_topic = [key for key, value in topic_map.items() if value == predicted_topic_id][0]
    
    question_vec = sentence_to_vec(cleaned_question, word2vec_model)
    similarities = [(i, np.dot(question_vec, sentence_to_vec(q, word2vec_model))) for i, q in enumerate(X_train)]
    best_match_idx = max(similarities, key=lambda x: x[1])[0]

    return answers[best_match_idx]


topic_counts = Counter(y_labels)

# print(f"Tổng số topic: {len(topic_counts)}")
# print("Số lượng câu hỏi theo từng topic:")

label_map_inv = {v: k for k, v in topic_map.items()}

# for topic_id, count in topic_counts.items():
#     topic_name = label_map_inv.get(topic_id, "Unknown")
#     print(f"- {topic_name}: {count} câu hỏi")


# Tạo dữ liệu cho biểu đồ
models = ['RandomForest', 'Naive Bayes', 'Logistic Regression']
accuracies = [accuracy, nb_results[0], logistic_results[0]]

# Vẽ biểu đồ
plt.figure(figsize=(8, 5))
sns.barplot(x=models, y=accuracies, palette='viridis')

# Hiển thị giá trị trên cột
for i, v in enumerate(accuracies):
    plt.text(i, v + 0.01, f"{v:.2f}", ha='center', fontsize=12)

plt.ylim(0, 1)
plt.xlabel("Mô hình")
plt.ylabel("Độ chính xác")
plt.title("So sánh độ chính xác giữa các mô hình")
plt.show()



# # Thử nghiệm với câu hỏi nhập từ bàn phím
# while True:
#     user_input = input("Nhập câu hỏi (hoặc 'exit' để thoát): ")
#     if user_input.lower() == 'exit':
#         break
#     topic, response = predict_answer(user_input, vectorizer, rf_model, topic_map, word2vec_model, answers)
#     print(f"Chủ đề dự đoán: {topic}\nCâu trả lời gợi ý: {response}")

# if __name__ == "__main__":
#     dataset = load_data(file_path)


# Export variables
exported_vectorizer = vectorizer
exported_model = rf_model
exported_topic_map = topic_map
exported_word2vec_model = word2vec_model
exported_answers = answers

