import weaviate
import pandas as pd

#connect to db instance
def connect():
    client = weaviate.Client(
        url="http://localhost:8080",  # Replace with your endpoint
        #auth_client_secret=weaviate.AuthApiKey(api_key="MYrhIAUviVpSg64V2gZvsvkZJMVgyCkik8wQ"),
        additional_headers = {
            "X-HuggingFace-Api-Key": "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"  # Replace with your inference API key
        }
    )
    return client


#create class in db
def create_class(client, db_class):
    class_obj = {
        "class": f"{db_class}",
        "vectorizer": "text2vec-transformers"
    }
    client.schema.create_class(class_obj)
    print(f'class {db_class} created')

# Settings for displaying the import progress
counter = 0
interval = 5  # print progress every this many records; should be bigger than the batch_size

def add_object(client, db_class, obj) -> None:
    global counter
    properties = {
        'interviewed_1': obj['interviewed_1'],
        'interviewed_2': obj['interviewed_2'],
        'interviewer_1': obj['interviewer_1'],
        'interviewer_2': obj['interviewer_2'],
	    'interviewer_3': obj['interviewer_3'],
	    'interviewer_4': obj['interviewer_4'],
	    'operator': obj['operator'],
	    'length': obj['length'],
	    'type': obj['type']
    }

    # Add the object to the batch
    client.batch.add_data_object(
        data_object=properties,
        class_name=db_class,
        # If you Bring Your Own Vectors, add the `vector` parameter here
        # vector=obj.vector
    )

    # Calculate and display progress
    counter += 1
    if counter % interval == 0:
        print(f'Imported {counter} articles...')

def add_csv(file, client, db_class):

    # Configure the batch import
    client.batch.configure(
        batch_size=10,
    )
    
    #pandas dataframe iterator with lazy-loading, to not load all records in RAM at once
    with pd.read_csv(file, sep='\t', encoding='utf-8', chunksize=10) as csv_iterator:
        # Iterate through the dataframe chunks and add each CSV record to the batch
        for chunk in csv_iterator:
            for index, row in chunk.iterrows():
                print(index)
                print(row)
                add_object(client, db_class, row)

    # Flush any remaining objects in the batch
    client.batch.flush()
    print(f'Finished importing {counter} articles.')

def to_fill(client, update_tuple):
    create_class(client, update_tuple[1])
    add_csv(update_tuple[0], client, update_tuple[1])

tsv_to_class = {'data/owl.tsv': 'Interviews'}

def main():
    print('trying to connect to create db...')
    client = connect()
    print('trying to create class...')
    for tsv in tsv_to_class.items():
        if tsv[1] not in [x['class'] for x in client.schema.get()['classes']]:
            print(f'adding class {tsv[1]}')
            to_fill(client, tsv)
        else:
            print(f'class {tsv[1]} is already in the db')

if __name__ == '__main__':
    main()