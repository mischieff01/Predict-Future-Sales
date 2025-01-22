from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
from sklearn.preprocessing import LabelEncoder
from itertools import product


app = Flask(__name__)

# Load the pre-trained model
model_path = "D:/Prediction Sales/sales_model.pkl"  # Path to the saved model file
model = joblib.load(model_path)

# Load datasets
sales = pd.read_csv("D:/Prediction Sales/DataSet/sales_train.csv")
items = pd.read_csv("D:/Prediction Sales/DataSet/items.csv")
item_categories = pd.read_csv("D:/Prediction Sales/DataSet/item_categories.csv")
shops = pd.read_csv('D:/Prediction Sales/DataSet/shops.csv')

# Helper functions for transformation
def lag_features(df,lags,col):
  print(col)
  for i in lags:
    shifted = df[['date_block_num','shop_id','item_id',col]].copy()
    shifted.columns = ['date_block_num', 'shop_id','item_id',col+'_lag_'+str(i)]
    shifted['date_block_num'] += i
    df = pd.merge(df,shifted,on=['date_block_num','shop_id','item_id'],how='left')
  return df


def preprocess_test_data(sales, test, items, item_categories,shops):
    
    # remove outliers
    sales = sales[(sales.item_price<100000)&(sales.item_price>0)]

    # remove duplicates
    sales = sales.drop_duplicates()

    # handles shops
    shops.loc[shops.shop_name == 'Сергиев Посад ТЦ "7Я"',"shop_name"] = 'СергиевПосад ТЦ "7Я"'
    shops['shop_city'] = shops['shop_name'].str.split(' ').map(lambda x: x[0])
    shops['shop_category'] = shops.shop_name.str.split(' ').map(lambda x: x[1:])
    shops.shop_category = shops.shop_category.apply(' '.join)
    shops.loc[shops.shop_city == "!Якутск", "shop_city"] = "Якутск"

    encoder = LabelEncoder()
    shops['shop_city'] = encoder.fit_transform(shops.shop_city)
    shops['shop_category'] = encoder.fit_transform(shops.shop_category)    
    shops = shops[['shop_id','shop_category','shop_city']]

    item_categories['category_type'] = item_categories.item_category_name.apply(lambda x:x.split(" ")[0]).astype(str)
    item_categories.loc[(item_categories.category_type == 'Игровые') | (item_categories.category_type == "Аксессуары"), "category_type"] = "Игры"
    item_categories["split"] = item_categories.item_category_name.apply(lambda x: x.split("-"))
    item_categories["category_subtype"] = item_categories.split.apply(lambda x: x[1].strip() if len(x) > 1 else x[0].strip())

    item_categories['category_type'] = encoder.fit_transform(item_categories.category_type)
    item_categories['category_subtype'] = encoder.fit_transform(item_categories.category_subtype)
    item_categories = item_categories[['item_category_id','category_type','category_subtype']]

    sales = sales.groupby(['date_block_num', 'shop_id','item_id'], as_index=False).agg({'item_cnt_day': 'sum'}).rename(columns={'item_cnt_day': 'item_cnt_month'}, inplace=False)

    new_df = pd.concat([sales, test],ignore_index=True)

    # create a feature matrix
    matrix = []
    for i in range(35):
        tmp = new_df[new_df.date_block_num==i]
        matrix.append(np.array(list(product([i], tmp.shop_id.unique(), tmp.item_id.unique())), dtype='int16'))

    # turn the grid into dataframe
    matrix = pd.DataFrame(np.vstack(matrix),columns=['date_block_num','shop_id','item_id'])

    # add the features from sales data to the matrix
    matrix = matrix.merge(new_df, on=['date_block_num','shop_id','item_id'], how='left').fillna(0)


    # merge features from shops, items and item categories
    matrix = matrix.merge(shops, on ='shop_id', how = 'left')
    matrix = matrix.merge(items[['item_id','item_category_id']], on = 'item_id', how = 'left')
    matrix = matrix.merge(item_categories, on = 'item_category_id', how = 'left')


    # add month
    matrix['month']= matrix.date_block_num%12
    matrix['item_cnt_month'] = matrix['item_cnt_month'].clip(0,20)

    matrix = lag_features(matrix,[1,2,3,4,5,12],'item_cnt_month')

    # shop/date_block_num aggregates lags
    gb = matrix.groupby(['shop_id', 'date_block_num'],as_index=False)\
            .agg({'item_cnt_month':'sum'})\
            .rename(columns={'item_cnt_month':'cnt_block_shop'}, inplace=False)
    matrix = matrix.merge(gb, how='left', on=['shop_id', 'date_block_num']).fillna(0)
    matrix = lag_features(matrix, [1, 2, 3, 4, 5, 12], 'cnt_block_shop')
    matrix.drop('cnt_block_shop', axis=1, inplace=True)

    # item/date_block_num aggregates lags
    gb = matrix.groupby(['item_id', 'date_block_num'],as_index=False)\
            .agg({'item_cnt_month':'sum'})\
            .rename(columns={'item_cnt_month':'cnt_block_item'}, inplace=False)
    matrix = matrix.merge(gb, how='left', on=['item_id', 'date_block_num']).fillna(0)
    matrix = lag_features(matrix, [1, 2, 3, 4, 5, 12], 'cnt_block_item')
    matrix.drop('cnt_block_item', axis=1, inplace=True)


    # category/date_block_num aggregates lags
    gb = matrix.groupby(['category_type', 'date_block_num'],as_index=False)\
            .agg({'item_cnt_month':'sum'})\
            .rename(columns={'item_cnt_month':'cnt_block_category'}, inplace=False)
    matrix = matrix.merge(gb, how='left', on=['category_type', 'date_block_num']).fillna(0)
    matrix = lag_features(matrix, [1, 2, 3, 4, 5, 12], 'cnt_block_category')
    matrix.drop('cnt_block_category', axis=1, inplace=True)


    X_test = matrix[matrix.date_block_num == 34].drop(['item_cnt_month'], axis=1)
    X_test.drop('date_block_num', axis=1, inplace=True)

    return X_test


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    shop_id = int(data["shop_id"])
    item_id = int(data["item_id"])


    test = pd.DataFrame({"shop_id": [shop_id], "item_id": [item_id], "date_block_num": [34], "item_cnt_month":[0] })

    # Preprocess the test data
    test_data = preprocess_test_data(sales, test, items, item_categories,shops)

    # Prepare the data for prediction
    dtest = xgb.DMatrix(test_data)

    # Make prediction
    prediction = model.predict(dtest)[0]

    # Convert prediction to a native Python float for JSON serialization
    prediction = float(prediction)

    return jsonify({"prediction": prediction})


@app.route("/get_shop_ids", methods=["GET"])
def get_shop_ids():
    # Load shop data
    # shops = pd.read_csv('D:/Prediction Sales/DataSet/shops.csv')
    unique_shop_ids = shops['shop_id'].unique().tolist()
    return jsonify(unique_shop_ids)

@app.route("/get_item_ids", methods=["GET"])
def get_item_ids():
    # Load item data
    # items = pd.read_csv('D:/Prediction Sales/DataSet/items.csv')
    unique_item_ids = items['item_id'].unique().tolist()
    return jsonify(unique_item_ids)


if __name__ == "__main__":
    app.run(debug=True)


