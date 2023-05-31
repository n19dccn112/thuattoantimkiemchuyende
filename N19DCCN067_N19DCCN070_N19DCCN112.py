import math
import time
from nltk.corpus import stopwords

def doc_file(duong_dan):
    with open(duong_dan, 'r') as file:
        noi_dung_file = file.read()
    noi_dung_file = noi_dung_file.lower()

    bat_dau_cau_moi = 0
    vitri_cau = {}
    for i in range(0, len(noi_dung_file)):
        if noi_dung_file[i] == "/":
            list = noi_dung_file[bat_dau_cau_moi:i].strip().split('\n')
            key = list[0]
            value = list[1]
            vitri_cau[key] = value
            bat_dau_cau_moi = i + 1
    return vitri_cau

def dicttumadoc_dictmadocdodaidoc_dodaitb(doc_vitri_cau_dict, stop_words):
    doc_word_list_vitri_dict = {}
    doc_vitridoc_lendoc_dict = {}
    for i, sentence in doc_vitri_cau_dict.items():
        sentence = sentence.lower()
        words = sentence.split()  # tách câu thành các từ
        words_not_stopword = [word for word in words if word not in stop_words]
        doc_vitridoc_lendoc_dict[i] = len(words_not_stopword)
        for word in words:
            if word not in stop_words:  # nếu từ không thuộc stop_words
                if word not in doc_word_list_vitri_dict:  # nếu từ chưa có trong từ điển
                    doc_word_list_vitri_dict[word] = [i]  # tạo key với vị trí đầu tiên của từ trong D
                else:
                    doc_word_list_vitri_dict[word].append(i)  # thêm vị trí của từ vào list tương ứng trong từ điển
    sort_doc_word_list_vitri_dict = dict(sorted(doc_word_list_vitri_dict.items(), key=lambda x: x[0].lower()))
    tb_lendoc = sum(doc_vitridoc_lendoc_dict.values()) / len(doc_vitridoc_lendoc_dict)
    # print(sort_doc_word_list_vitri_dict, ": ", doc_vitridoc_lendoc_dict, ", ", tb_lendoc)
    return sort_doc_word_list_vitri_dict, doc_vitridoc_lendoc_dict, tb_lendoc

def RSV_word(n, df, tf, dl, avdt, k=2, b=0.75):
    # n là số văn bản
    # df là số lần xuất hiện của từ trọng tất cả các tập
    # tf là số lần xuất hiện của từ trong tập đang xét
    # dl là độ dài vb hiện tại
    # avdt là độ dài tb tất cả vb
    # k và b là các tham số của BM25;
    # k điều khiển tỷ lệ tần số; b chuẩn hóa độ dài tài liệu
    result = math.log(n / df, 10) * (((k + 1) / tf) / (k * ((1 - b) + (b * dl) / avdt) + tf))
    return result

def dicttulistvitri(query, doc_word_list_vitri_dict, stop_words):
    query_words_list = [word.lower() for word in query.split() if word not in stop_words]
    query_tu_list_vitri_dict = {}
    for key, value in doc_word_list_vitri_dict.items():
        print("key in query_words_list: ", key, ": ", query_words_list)
        if key in query_words_list:
            query_tu_list_vitri_dict[key] = value
    # print(query_tu_list_vitri_dict)
    return query_tu_list_vitri_dict


def rsv_bm25(doc_vitri_cau_dict, doc_vitridoc_lendoc_dict, tb_lendoc, query_tu_list_vitri_dict):
    vitridoc_rsv_dict = {}
    for i, sentence in doc_vitri_cau_dict.items():  # từng 1: D1, 2: D2, 3: D3,...
        c1 = 0
        for tu, listvitri in query_tu_list_vitri_dict.items():  # Các từ của câu query q1, q2, q3,..
            tf = 0
            sentence = sentence.lower()
            words = sentence.split()
            for word in words:  # Duyệt qua các từ của D1: w1, w2, w3,...
                if tu.lower() == word.lower():
                    tf += 1
            if tf != 0:
                c1 += RSV_word(len(doc_vitri_cau_dict), len(listvitri), tf, doc_vitridoc_lendoc_dict[i], tb_lendoc)
        if c1 != 0:
            vitridoc_rsv_dict[i] = c1
    # print(vitridoc_rsv_dict)
    return vitridoc_rsv_dict


if __name__ == '__main__':
    start_time = time.time()

    base_url = 'C://Users//My//Downloads//IR4'
    noidung_url = base_url + '//npl//doc-text'
    truyvan_url = base_url + '//npl//query-text'
    output_result_url = base_url + '//bm25'

    doc_vitri_cau_dict = doc_file(noidung_url)
    query_vitri_cau_dict = doc_file(truyvan_url)
    stop_words = set(stopwords.words('english'))

    doc_word_list_vitri_dict, doc_vitridoc_lendoc_dict, tb_lendoc = dicttumadoc_dictmadocdodaidoc_dodaitb(doc_vitri_cau_dict, stop_words)
    top_5_values = []
    str_vitridoc_rsv_dict = ""
    for vitri, cauquey in query_vitri_cau_dict.items():
        query_tu_list_vitri_dict = dicttulistvitri(cauquey, doc_word_list_vitri_dict, stop_words)
        vitridoc_rsv_dict = rsv_bm25(doc_vitri_cau_dict, doc_vitridoc_lendoc_dict, tb_lendoc, query_tu_list_vitri_dict)
        vitridoc_rsv_dict = dict(sorted(vitridoc_rsv_dict.items(), key=lambda x: x[1], reverse=True))
        str_vitridoc_rsv_dict += str(vitri) + "\n" + "\n".join([f"{key}\t{value}" for key, value in vitridoc_rsv_dict.items()]) + "\n/\n"

    # f = open(output_result_url, "w")
    # f.write(str_vitridoc_rsv_dict)
    # f.close()

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Thời gian chạy chương trình: {total_time} giây")

