__author__ = 'Anupam'


COMMON_WORDS_FILE = "../data/common_words"

def StopList(unigramIndex,queryTerms):

    stop_list = []
    with open(COMMON_WORDS_FILE, "r") as ins:
        for line in ins:
            stop_list.append(line.rstrip())

    newIndex = dict(unigramIndex)
    newQuery = list(queryTerms)

    for word in stop_list:
        newQuery =remove_values_from_list(newQuery,word)
        newIndex = remove_key(newIndex,word)

    return (newIndex,newQuery)

def isStopWord(word):

    stop_list = []
    with open(COMMON_WORDS_FILE, "r") as ins:
        for line in ins:
            stop_list.append(line.rstrip())
    if word in stop_list:
        return True

    return  False

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]


def remove_key(d, key):
    r = dict(d)
    if key in r.keys():
        del r[key]
    return r


