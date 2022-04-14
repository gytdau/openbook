from config import config
import openai
from db import db

openai.api_key = config["OPENAI_API_KEY"]
db_connection = config["DB_CONNECTION"]

def classify_text(title, author, snippet):
    if author is not None:
        author = "by " + author

#     prompt = f'''The following are excerpts from books and a short blurb.

# "Frankenstein; Or, The Modern Prometheus" by Mary Wollstonecraft Shelley
# "Letter 1
# To Mrs. Saville, England.

# St. Petersburgh, Dec. 11th, 17—.

# You will rejoice to hear that no disaster has accompanied the commencement of an enterprise which you have regarded with such evil forebodings. I arrived here yesterday, and my first task is to assure my dear sister of my welfare and increasing confidence in the success of my undertaking."

# Blurb: Victor Frankenstein is a scientist obsessed with generating life from lifeless matter. He subsequently manages to create a horrifying, sentient creature assembled from pieces of stolen body parts. Shunned by society and faced with eternal isolation, the creature becomes murderous with revenge against the one who brought him into existence, Frankenstein.

# "{title}" {author}
# "{snippet}"

# Blurb:'''

    prompt = f'''The following are excerpts from books and the categories they fall into.

"Frankenstein; Or, The Modern Prometheus" by Mary Wollstonecraft Shelley
"Letter 1
To Mrs. Saville, England.

St. Petersburgh, Dec. 11th, 17—.

You will rejoice to hear that no disaster has accompanied the commencement of an enterprise which you have regarded with such evil forebodings. I arrived here yesterday, and my first task is to assure my dear sister of my welfare and increasing confidence in the success of my undertaking."

Categories: Classics, Fiction, Horror, Science Fiction, Gothic, Fantasy

"{title}" {author}
"{snippet}"

Categories:'''
    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=prompt,
        temperature=0.1,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    return response.choices[0].text

def update_book_classification():
    with db(db_connection, create_tables=False) as con:
        books = con.get_featured_books()
        # print(books)

        for book in books:
            classifications = classify_text(book[1], book[2], book[3]) 

            print(f"#{book[0]} {book[1]}, {book[2]}): {classifications}")
            for cat in classifications.split(","):
                cat = cat.strip()
                id = book[0]
                con.add_category(cat)
                con.add_book_category(id, cat)

            

# print(classify_text("Moby Dick; Or, The Whale", "Herman Melville", "CHAPTER 1. Loomings.Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen and regulating the circulation."))
update_book_classification()
