from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.models import Variable


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

    # try except?
    driver.get('https://www.nalog.gov.ru/rn77/program/5961290/')
    date_text = driver.find_element(
        By.XPATH,
        '/html/body/form/div[3]/div[1]/div[4]/div[2]/div/div/div/div[2]/p[1]/span'
    )

    # prepare date
    text = date_text.text
    driver.quit()
    date_human = text.split()[-1]
    date_split = date_human.split('.')
    date_prepared = date_split[2] + date_split[1] + date_split[0]

    date_in_airflow = Variable.get('date_in_airflow', default_var=None)

    if not date_in_airflow:
        Variable.set('date_in_airflow', date_prepared)
        return 'do_update_download_zip'

    if date_prepared > date_in_airflow:
        Variable.set('date_in_airflow', date_prepared)
        return 'do_update_download_zip'
    else:
        return 'no_update'

# download zip if updated
def _do_update_download_zip():
    print('MEOW')


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

    do_update_download_zip = PythonOperator(
        task_id='do_update_download_zip',
        python_callable=_do_update_download_zip
    )

    no_update = EmptyOperator(
        task_id='no_update'
    )

parse_date_update_check >> [do_update_download_zip, no_update]