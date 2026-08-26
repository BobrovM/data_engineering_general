from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.models import Variable


URL_TO_PARSE = 'https://www.nalog.gov.ru/rn77/program/5961290/'
URL_TO_DOWNLOAD = 'https://data.nalog.ru/files/tnved/tnved.zip'


def _parse_date_update_check():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options


    # set chrome driver
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')

    chrome_paths = [
        '/usr/bin/google-chrome',
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/opt/google/chrome/chrome'
    ]

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)

    xpath = '/html/body/form/div[3]/div[1]/div[4]/div[2]/div/div/div/div[2]/p[1]/span'
    # try except?
    driver.get(URL_TO_PARSE)
    date_text = driver.find_element(
        By.XPATH,
        xpath
    )

    # prepare date
    text = date_text.text
    driver.quit()
    date_human = text.split()[-1]
    date_split = date_human.split('.')
    date_prepared = date_split[2] + date_split[1] + date_split[0]

    date_in_airflow = Variable.get('relevant_date', default_var=None)

    if not date_in_airflow:
        Variable.set('relevant_date', date_prepared)
        return 'do_update_download_decode_tnved3'

    if date_prepared > date_in_airflow:
        Variable.set('relevant_date', date_prepared)
        return 'do_update_download_decode_tnved3'
    else:
        return 'no_update'


# download tnved3 if updated
def _do_update_download_decode_tnved3():
    from pathlib import Path
    import requests
    import zipfile
    import io

    URL_TO_DOWNLOAD = 'https://data.nalog.ru/files/tnved/tnved.zip'

    paths = []
    paths.append(Path('/') / 'app' / 'data_share' / '06_airflowed_tnved')
    paths.append(Path('..') / '..' / 'data_share' / '06_airflowed_tnved')
    outpath = Path('.')

    for path in paths:
        path = path.resolve()
        if path.exists():
            outpath = path
            break

    print(outpath)

    # data.nalog blocks (403) after some 'bot' like activity
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }

    response = requests.get(URL_TO_DOWNLOAD, headers=headers, timeout=(10, 120))
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        with zip_ref.open('TNVED3.TXT') as f:
            contents = f.read()

        contents = contents.decode('cp866')

        with open(outpath / 'TNVED3_DECODED.TXT', 'w', encoding='utf-8', newline='') as f:
            f.write(contents)


with DAG(
    'download_tnved',
    start_date=datetime(2026, 8, 1),
    catchup=False,
    schedule='@daily'
) as dag:
    parse_date_update_check = BranchPythonOperator(
        task_id='parse_date_update_check',
        python_callable=_parse_date_update_check
    )

    do_update_download_decode_tnved3 = PythonOperator(
        task_id='do_update_download_decode_tnved3',
        python_callable=_do_update_download_decode_tnved3
    )

    no_update = EmptyOperator(
        task_id='no_update'
    )

parse_date_update_check >> [do_update_download_decode_tnved3, no_update]