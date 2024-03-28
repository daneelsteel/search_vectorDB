from razdel import tokenize
import more_itertools as mit

#pass query to the db; get top answer and its distance
def ask(string_search, column, client):
    response = (
        client.query
        .get("Interviews", [column])
        .with_near_text({
            "concepts": [f"{string_search}"]
        })
        .with_additional(["distance", "id"])
        .with_limit(1)
        .do()
    )
    return response

#divide list of tokens into same-size chunks
def divide_chunks(l, n, step):
    winds = list(mit.windowed(l, n, step))
    return [list(filter(None, w)) for w in winds]

#tokenize string without punct
def tokenized(string):
    z = list(tokenize(string))
    return [_.text for _ in z if any(c.isalnum() for c in _.text)]
 
#windowed search: if gmore than 16 tokens on screen, get bigger window
def search(string_search, client):
    tokens = tokenized(string_search)
    windows = divide_chunks(tokens, 5, 2)
    #start searching
    candidates = []
    for i in windows:
        response = ask(' '.join([str(x) for x in i]), "interviewed_1", client)
        distance = response['data']['Get']['Interviews'][0]['_additional']['distance']
        if distance<0.3 and distance>0.2:
            response_2 = ask(' '.join([str(x) for x in i]), "interviewed_2", client)
            distance_2 = response_2['data']['Get']['Interviews'][0]['_additional']['distance']
            if distance_2<distance:
                fin_distance = distance_2
                fin_response = response_2
        elif distance<0.2:
            fin_response = response
            fin_distance = distance
        if fin_response:
            print(fin_distance)
            info = (response['data']['Get']['Interviews'][0]['text'], response['data']['Get']['Interviews'][0]['_additional']['id'])
        candidates.append(info)
    return candidates

#each info is a tuple size 2: error text, error id
def main(string_search, client):
    if len(string_search)==0:
        return {'success': False, 'text': 'что не так?'}
    else:
        candidates = search(string_search, client)
        result = {}
        if len(candidates)>0:
            top_answer = sorted(candidates, key=lambda item: item[1])[0]
            print(top_answer)
            data_object = client.data_object.get_by_id(top_answer[0], class_name='Interviews')
            result = {'success': True, 
                    'interviewed_1': data_object['properties']['interviewed_1'], 
                    'interviewed_2': data_object['properties']['interviewed_2'], 
                    'date': f"Записано {data_object['properties']['date']}?", 
                    'length': data_object['properties']['length'], 
                    'type': data_object['properties']['type']}
        else:
            print('Я не могу найти такое интервью')
            result = {'success': False, 'text': 'Я не могу найти такое интервью'}
        print(result)
        return result