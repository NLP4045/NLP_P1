from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

reviews = pd.read_csv("jewel_reviews.csv")['reviews']
vectorizer = TfidfVectorizer(stop_words=["airport"], max_df=0.7)
X = vectorizer.fit_transform(reviews)


query = ""
while query != "q":
    query = input('Enter search query to search reviews of Jewel Changi Airport ("q" to exit): ')
    if query == "q":
        break

    query_vector = vectorizer.transform([query])
    results = cosine_similarity(X, query_vector).flatten()

    # Sort cosine similarity to get the ranking, while removing all reviews with a similarity score of 0
    docid_scores = sorted([(idx, score) for idx,score in enumerate(results) if score > 0], key=lambda x:x[1], reverse=True)

    # If no resulting reviews found (i.e., all similarity score is 0 -- skip this query)
    if len(docid_scores) == 0:
        print("No similar reviews found! Please try another search query")
        continue

    docids_ranked = [docid for (docid,score) in docid_scores]
    # Display the reviews in a readable format, in chunks of 5 reviews per "page"
    for i in range(0,len(docids_ranked),5):
        current_docs = docids_ranked[i:i+5]
        rank_docs = [((idx + i + 1), docid) for idx, docid in enumerate(current_docs)]
        rank_docs_strs = [("{}: ".format(rank) + reviews[docid]) for rank,docid in rank_docs]
        while True:
            print("\n"*10)
            print('Reviews {} to {} (out of {}) for search query "{}"'.format(i+1, i+len(rank_docs_strs), len(docids_ranked), query))
            print("==============================================================="*2)
            print()
            print("\n\n".join(rank_docs_strs))
            print("\n\n")
            view_next_5_choice = ""
            if i+5 >= len(docids_ranked):
                break
            view_next_5_choice = input("Would you like to view the next 5 reviews? (Y/N): ")
            if view_next_5_choice in ["Y","y","N","n"]:
                break
            else:
                print("Invalid choice!")
                input("Press ENTER to continue...")
        if view_next_5_choice in ["Y","y"]:
            continue
        else:
            break
                
