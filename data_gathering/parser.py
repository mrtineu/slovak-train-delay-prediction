from scrape import get_train_state
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def clean_train(train):
    #We will delete these two keys as they do not change in time and take up a lot of space
    try:
        train.pop('Trasa',None)
        train.pop('TrasaBody',None)
    except Exception as e:
        logger.error("Exception occured: ",e)
    # DO NOT DELETE THIS - It filters out when a train has no time specified
    if(train['Cas'] == "---"):
        train['Cas'] = None
    else:
        try:
            # Converts the string into datetime object
            train['Cas'] = datetime.strptime(train["Cas"], "%d.%m.%Y %H:%M")
        except ValueError:
            logger.error(f"Error variable Cas '{train["Cas"]}' could not be parsed into a datetime object")
    # DO NOT DELETE THIS
    if(train['CasPlan'] == "---"):
        train['CasPlan'] = None
    else:
        try:
            train['CasPlan'] = datetime.strptime(train["CasPlan"], "%d.%m.%Y %H:%M")
        except ValueError:
            logger.error(f"Error variable CasPlan '{train["CasPlan"]}' could not be parsed into a datetime object")
    return train


def clean_train_data(data):
    clean_data = data[0]
    i = 0
    while i < len(clean_data):
        clean_data[i] = clean_train(clean_data[i])
        i+=1
    return clean_data


if __name__ == "__main__":
    data = get_train_state()
    cleaned_data = clean_train_data(data)
    print(cleaned_data[10])


