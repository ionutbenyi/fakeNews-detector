import json

def compare_similarities(array):
    for headline in array:
        print(headline['sentence'])
        for source in headline["sources"]:
            print("BERT = "+ str(source["similarity"])+ " " +source["source"])
            if source["spacy"] != 0.0:
                print("SPACY = "+str(source["spacy"]))
        print("\n")

def merge_similarity_sets():
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    data5 = []
    data6 = []
    data7 = []
    data8 = []
    data9 = []
    data10 = []
    data11 = []
    data12 = []
    data13 = []

    s1 = []
    s2 = []
    s3 = []
    s4 = []
    s5 = []
    s6 = []
    s7 = []
    s8 = []
    s9 = []
    s10 = []
    s11 = []
    s12 = []
    s13 = []

    with open('../data_veritool/0/articles.txt') as inp_data:
        data1 = json.load(inp_data)
    with open('../data_veritool/0/similarities.txt') as inp_data:
        s1 = json.load(inp_data)

    with open('../data_veritool/1/articles.txt') as inp_data:
        data2 = json.load(inp_data)
    with open('../data_veritool/1/similarities.txt') as inp_data:
        s2 = json.load(inp_data)

    with open('../data_veritool/2/articles.txt') as inp_data:
        data3 = json.load(inp_data)
    with open('../data_veritool/2/similarities.txt') as inp_data:
        s3 = json.load(inp_data)

    with open('../data_veritool/3/articles.txt') as inp_data:
        data4 = json.load(inp_data)
    with open('../data_veritool/3/similarities.txt') as inp_data:
        s4 = json.load(inp_data)

    with open('../data_veritool/4/articles.txt') as inp_data:
        data5 = json.load(inp_data)
    with open('../data_veritool/4/similarities.txt') as inp_data:
        s5 = json.load(inp_data)

    with open('../data_veritool/5/articles.txt') as inp_data:
        data6 = json.load(inp_data)
    with open('../data_veritool/5/similarities.txt') as inp_data:
        s6 = json.load(inp_data)

    with open('../data_veritool/6/articles.txt') as inp_data:
        data7 = json.load(inp_data)
    with open('../data_veritool/6/similarities.txt') as inp_data:
        s7 = json.load(inp_data)

    with open('../data_veritool/7/articles.txt') as inp_data:
        data8 = json.load(inp_data)
    with open('../data_veritool/7/similarities.txt') as inp_data:
        s8 = json.load(inp_data)

    with open('../data_veritool/8/articles.txt') as inp_data:
        data9 = json.load(inp_data)
    with open('../data_veritool/8/similarities.txt') as inp_data:
        s9 = json.load(inp_data)

    with open('../data_veritool/9/articles.txt') as inp_data:
        data10 = json.load(inp_data)
    with open('../data_veritool/9/similarities.txt') as inp_data:
        s10 = json.load(inp_data)

    with open('../data_veritool/10/articles.txt') as inp_data:
        data11 = json.load(inp_data)
    with open('../data_veritool/10/similarities.txt') as inp_data:
        s11 = json.load(inp_data)

    with open('../data_veritool/11/articles.txt') as inp_data:
        data12 = json.load(inp_data)
    with open('../data_veritool/11/similarities.txt') as inp_data:
        s12 = json.load(inp_data)

    with open('../data_veritool/12/articles.txt') as inp_data:
        data13 = json.load(inp_data)
    with open('../data_veritool/12/similarities.txt') as inp_data:
        s13 = json.load(inp_data)

    data_res = []
    s_res = []

    for el in data1:
        data_res.append(el)
    for s in s1:
        s_res.append(s)

    for el in data2:
        data_res.append(el)
    for s in s2:
        s_res.append(s)

    for el in data3:
        data_res.append(el)
    for s in s3:
        s_res.append(s)

    for el in data4:
        data_res.append(el)
    for s in s4:
        s_res.append(s)

    for el in data5:
        data_res.append(el)
    for s in s5:
        s_res.append(s)

    for el in data6:
        data_res.append(el)
    for s in s6:
        s_res.append(s)

    for el in data7:
        data_res.append(el)
    for s in s7:
        s_res.append(s)

    for el in data8:
        data_res.append(el)
    for s in s8:
        s_res.append(s)

    for el in data9:
        data_res.append(el)
    for s in s9:
        s_res.append(s)

    for el in data10:
        data_res.append(el)
    for s in s10:
        s_res.append(s)

    for el in data11:
        data_res.append(el)
    for s in s11:
        s_res.append(s)

    for el in data12:
        data_res.append(el)
    for s in s12:
        s_res.append(s)

    for el in data13:
        data_res.append(el)
    for s in s13:
        s_res.append(s)

    with open('data/articles.txt','w') as outp_data:
        json.dump(data_res, outp_data)
        data_res.clear()
        outp_data.close()
    with open('data/similarities.txt','w') as outp_data:
        json.dump(s_res, outp_data)
        s_res.clear()
        outp_data.close()


if __name__ == '__main__':
    merge_similarity_sets()
    