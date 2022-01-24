import pandas as pd
import pickle

class Recommendation_System():
  def __init__(self):
   
    self.df_recommendation = pd.read_pickle('./pickles/reviews_data.pkl')
    self.recommendation_model = pickle.load(open('./pickles/user_final_rating.pkl', 'rb'))
    self.sentiment_analysis_model = pickle.load(open('./pickles/final_sentiment_analysis.pkl', 'rb'))
    self.vectorizer_model = pickle.load(open('./pickles/tfidf_vectorizer.pkl', 'rb'))

  def get_top_5_recommendations(self, username):
    """
    """
    
    try:
        #extracting top 20 products from the recommendation model for given user
        top_20_user_recommendations = self.recommendation_model.loc[user].sort_values(ascending=False)[0:20]
        list_top_20_recommendations = top_20_user_recommendations.index.tolist()
      
        print('top_20_product_recommendations_list :')
        print(top_20_product_recommendations_list)
        
        product_positive_sentiment_percent = []
        
        # for each product, calculate positive sentiment score
        for product in list_top_20_recommendations:
        
            #extract the required reviews data for the given product
            df_product = df_recommendation[df_recommendation['name'] == product][['name','reviews_title', 'reviews_text']]
    
            #extract features from the review text using TF-IDF vectorizer
            tfidf_model = vectorizer_model.transform(df_product['reviews_text'])
            df_tfidf = pd.DataFrame(tfidf_model.toarray(), columns=vectorizer_model.get_feature_names())
    
            #cutoff for the RandomForest model
            cutoff = 0.48
    
            # Make sentiment prediction using the final Random Forest model
            y_proba = sentiment_analysis_model.predict_proba(df_tfidf)[:, 1]
            y_pred = list(map(lambda x: 1 if x >= cutoff else 0, y_proba.tolist()))

            # Calculate Positive Sentiment percentage out of the predicted sentiment
            positive_sentiment_percent = y_pred.count(1)/len(y_pred)
            
            product_positive_sentiment_percent.append(positive_sentiment_percent)
        
        df_top_20_user_recommendations = pd.DataFrame(data={
        "Product": list_top_20_recommendations,
        "Positive_sentiment_percent": product_positive_sentiment_percent})
        
        list_top_20_products = df_top_20_user_recommendations.sort_values(by="Positive_sentiment_percent", ascending=False)['Product'].tolist()
        
        return list_top_20_products[:5], ''
    except Exception as e:
        error = f"{str(e)}: Something went wrong! Please check the username and try again."
        return '', error
