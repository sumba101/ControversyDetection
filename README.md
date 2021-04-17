# ControversyDetection
controversy detection project for Social Computing course in IIIT Hyderabad. 2021.

## Data scraping
The script used for scraping is present in the folder `dataset_scraper`. Detailed instructions on running the script and its outpout can be found in `dataset_scraper/README.md`

## Preprocessing the scraped data
After downloading the dataset in the data folder, we need to preprocess the data. The data can be preprocessed by using the code in the preprocessor directory. Change the file_name in the notebook to point to your dataset. Run that code to preprocess the data. It will automatically save the file in a pickle file as a dataframe. Change the variable `output_name` to point to the name of the pickle file.

## Perspective API scores
We then need extract perspective API scores on the comments of the extracted dataset. Run `perspective-experiments.ipnb` on the relevant dataset to get the perspective-API scores. It will be stored as `perspective.pickle` in the data directory.

## Sentiment scores

## Models
- For running the baseline models, you should run the notebook within the baselines folder
- For running the baseline model on the perspective scores, you should run `perspective_models.ipynb` within the perspective-api folder
- For the running out final model, you should run the `transformer-cl.ipynb` within the models folder. Set the `sent` variable to True within the params, if you want to include the sentiment scores or False otherwise. Same applies for the `pers` variable within the params. Change the `output_path` within the params to direct to where to store the models. It will store the models after every epoch. 

## Inference
- Choose the best performing model for inference. Only the models using the perspective scores and transformer embeddings can be used for inference. Change the `model` variable in the `flask_inference.py` to point to the saved model. This will start the REST API at port 3000(possibly). You can use [ngrok](https://ngrok.com/) to expose the port to internet. You can now send POST requests to the url in format below to see of the tweet is controversial or not:
```
text = {
    'root': "Root tweet",
    'comments': [
        'Comment 1',
        'Comment 2',
        'Comment 3',
        ....
    ]
}

```

## Browser Extension
- First navigate to the manage extensions page in your chrome browser by typing `chrome://extensions/` into the address bar
- Click on load unpacked and navigate and select the folder `contro` found in this project codebase

Now the browser extension set up is done
- Execute command `pip3 install uvicorn fastapi`
- `cd fastapi-backend` and then enter the command `uvicorn receiver:app --reload` into the terminal
