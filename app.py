from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np

popular_df = pd.read_csv('raw_data.csv', encoding='unicode_escape')
Book_name = popular_df['Book-Title'].tolist()
author = popular_df['Book-Author'].tolist()
image = popular_df['Image-URL-M'].tolist()
votes = popular_df['num_rating'].tolist()
rating = popular_df['avg_rating'].tolist()
# print(Book_name)

pt = pickle.load(open('pt.pkl','rb'))
book = pickle.load(open('book.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_rating'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    Book_Name = request.form.get('Book_Name')
    index = np.where(pt.index == Book_Name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
#         print(pt.index[i[0]])
        temp_df = book[book['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Image-URL-M'].values))
        data.append(item)
    return render_template('recommend.html', data=data)



if __name__ == '__main__':
    app.run(debug=True)
