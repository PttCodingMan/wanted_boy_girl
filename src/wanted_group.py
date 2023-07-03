import json

import PyPtt
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

import config

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

if __name__ == '__main__':
    crawler = PyPtt.API()

    with open('wanted_group.txt', 'r') as f:
        sentences = json.load(f)

    try:
        crawler.login(config.PTT_ID, config.PTT_PW, kick_other_session=True)

        newest_index = crawler.get_newest_index(
            PyPtt.NewIndex.BOARD,
            board='Wanted',
            search_type=PyPtt.SearchType.KEYWORD,
            search_condition='[徵求]')

        for i in reversed(range(5000)):
            cur_index = newest_index - i

            post = crawler.get_post(
                board='Wanted',
                index=cur_index)

            if not post:
                continue

            if post["post_status"] != PyPtt.PostStatus.EXISTS:
                continue

            if not post["pass_format_check"]:
                continue

            if not post['content']:
                continue

            analysis_content = '\n'.join([post['author'], post["title"], post["content"].strip()])

            if '群組' in analysis_content:
                continue

            if analysis_content in sentences:
                continue

            print('index:', cur_index, i)
            sentences.append(analysis_content)

    finally:
        crawler.logout()

        with open('wanted_group.txt', 'w') as f:
            f.write(json.dumps(sentences, ensure_ascii=False, indent=4))

    # kmeans = KMeans()
    # kmeans.fit(model.encode(sentences))
    #
    # # 獲取每個樣本的分群結果
    # labels = kmeans.labels_
    #
    # # 顯示分群結果
    # print(labels)
