"""
q: When do I use AI to find answers or help me write and study code???
a: If I didn't find the example snippet or explanation in .pdf or internet, or if I need help with understanding specific
function or stuff. This is literally how the learning process works.

q: Is this code good?
a: I DON'T KNOW. I'll ask my friend to feed it to Claude

Also, this would be interesting to do in Bash for AD-HOC, but it's a bit too complicated for me atm.
"""


import httpx
import json
# import os
import os.path 
import asyncio # gotta learn the asyncio lib
import csv
from dotenv import load_dotenv

# dotenv was added through VSCode copilot, had troubles with accessing system env vars and then .env, asked LLM/AI,
# didn't want to share my so sensitive api key.
#load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))


### 2026.05.13 the api is back live
#dir_path = os.path.dirname(os.path.realpath(__file__))

#address = ""
#with open('{0}/api_url.txt'.format(dir_path), 'r') as file:
    #address = file.readline()

#address += address + "/api/v1/logs"

address = "http://5.159.103.79:4000/api/v1/logs"
print(address)


# get the data
async def api_data_receiver():
    """ Get data from hardcoded (maybe for now) API.
    Writes customs_data.csv in a directory where the python script was run.
    If API returns 429 too many requests, the script sleeps for 3 minutes.
    Else if returns any other error it just dies.

    Even this is a try of doing asynchronous code, I need more understanding of how does it work.
    """
    # Force UTF-8, got UnicodeEncodeError: 'charmap' codec can't encode character '\u0f3c' in position 6: character maps to <undefined>
    with open('customs_data.csv', 'w', encoding='utf-8') as file:
        fieldnames = [
            'code',
            'country',
            'direction',
            'district',
            'measure',
            'month',
            'netto',
            'quantity',
            'region',
            'value'
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()


        async with httpx.AsyncClient() as client:
            tries = 0
            page = 1

            while True:
                try:
                    q_params = {
                        "page": page,
                        "per_page": 200
                    }

                    response = await client.get(address, params=q_params)
                    response.raise_for_status()

                    # checkers everything is fine and not empty
                    print(response.status_code)
                    print(response.headers.get('content-type'))

                    # page checker
                    print(page)

                    # try to open json
                    try:
                        json_response = response.json()
                        print(json_response["items"])

                        if not json_response:
                            print("Pages ended")
                            break

                        if  not json_response["items"]:
                            print("Data ended")
                            break

                        # incoming json data from customs API was writen with an empy row each odd row, bizarre
                        writer.writerows(json_response["items"])

                    # if not json and is text or html
                    except json.decoder.JSONDecodeError:
                        text_response = response.text
                        print(text_response)
                        break

                    # increase page and reset tries since the try was successful
                    page += 1
                    tries = 0


                except httpx.TimeoutException:
                    print("uhoh")
                    # limited to 5 timeouts to Ford Escape infinite timeouts
                    tries+=1
                    if tries >= 5: break

                except httpx.HTTPStatusError as exc:
                    if exc.response.status_code == 429:
                        # Waiting 180 secs before retrying since task requirement. Buuuuuuuuut the original api is down,
                        # just putting it for God's sake.
                        await asyncio.sleep(180)
                        continue
                    else:
                        print("MASSIVE UH OH")
                        raise


# python module run
async def main():
    # idk why
    await api_data_receiver()

# bash run
def run_cli():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping data sourcing...")

# local run
if "__main__" == __name__:
    asyncio.run(main())