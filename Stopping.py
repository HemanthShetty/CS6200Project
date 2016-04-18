__author__ = 'Anupam'



def StopList(unigramIndex,queryTerms):

    stop_list = []
    with open("common_words.txt", "r") as ins:
        for line in ins:
            stop_list.append(line)

    newIndex = dict(unigramIndex)
    newQuery = list(queryTerms)

    for word in stop_list:
        newQuery =remove_values_from_list(newQuery,word)
        newIndex = remove_key(newIndex,word)

    return (newQuery,newIndex)



def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]


def remove_key(d, key):
    r = dict(d)
    if key in r.keys():
        del r[key]
    return r


