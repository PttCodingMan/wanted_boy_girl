import json

import PyPtt

import config

if __name__ == '__main__':
    crawler = PyPtt.API()

    with open(f'../data/data.json', 'r') as f:
        datas = f.readlines()

    datas = [json.loads(data) for data in datas]
    data_set = set([data['aid'] for data in datas])

    try:
        crawler.login(config.PTT_ID, config.PTT_PW)

        newest_index = crawler.get_newest_index(
            PyPtt.NewIndex.BOARD,
            board='Wanted',
            search_type=PyPtt.SearchType.KEYWORD,
            search_condition='[徵求]')

        for i in range(500):
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

            if post['aid'] in data_set:
                continue

            analysis_content = '\n'.join([post['author'], post["title"], post["content"].strip()])

            print('========' * 2)
            print(analysis_content)

            while True:
                label = input('author is [boy/girl/unknown/pass]').strip()
                if label not in ['b', 'g', 'u', 'p']:
                    continue
                break

            if label == 'p':
                continue

            with open(f'../data/data.json', 'a') as f:
                f.write(json.dumps({
                    'author': post['author'],
                    'title': post['title'],
                    'content': post['content'].strip(),
                    'aid': post['aid'],
                    'label': label
                }, ensure_ascii=False))
                f.write('\n')

    finally:
        crawler.logout()
