"""
q: When do I use AI to find answers or help me write and study code???
a: If I didn't find the example snippet or explanation in .pdf or internet, or if I need help with understanding specific
function or stuff. This is literally how the learning process works.

q: Is this code good?
a: I DON'T KNOW. I'll ask my friend to feed it to Claude

Also, this would be interesting to do in Bash for AD-HOC, but it's a bit too complicated for me atm.
"""


import httpx
# import os
import os.path 
import asyncio # gotta learn the asyncio lib
import csv
# from csvkit import convert
from dotenv import load_dotenv

# dotenv was added through VSCode copilot, had troubles with accessing system env vars and then .env, asked LLM/AI,
# didn't want to share my so sensitive api key.
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))


### Looks like pirated course API got shut down before 2026.05.05, or it is temp unavailable at this moment, idk.
### 2026.05.04 it was fine. Changing project to CoinGecko MR Beast cryptoscams for fun and funny training. But it's not 2 gigs...
"""
dir_path = os.path.dirname(os.path.realpath(__file__))

address = "";
with open('{0}/api_url.txt'.format(dir_path), 'r') as file:
    address = file.readline()
"""

api_key = os.getenv('CoinGecko_OfficeGuy_API')
address = "https://api.coingecko.com/api/v3/coins/list"
header = {"x-cg-demo-api-key": api_key}

### test to see that I did not f-up the address
# print(address)
# print(header)


# async def was AI suggestion, had troubles with await, I need to study asyncio, interested if each response is a unique callback
# will it be an unsorted mess????
# can it bug out and make a duplicate?????
# and 5 minutes after I did it i found the solution in pdf files of the pirated courses
# TODO needs pagination, learn pagination
async def api_data_receiver():
    """ Get data from hardcoded (maybe for now) API.
    Writes final_data.csv in a directory where the python script was run.
    If API returns 429 too many requests, the script sleeps for 3 minutes.
    Else if returns any other error it just dies.

    Even this is a try of doing asynchronous code, I need more understanding of how does it work.
    """
    # Force UTF-8, got UnicodeEncodeError: 'charmap' codec can't encode character '\u0f3c' in position 6: character maps to <undefined>
    with open('final_data.csv', 'w', encoding='utf-8') as file:    
        fieldnames = ["id", "symbol", "name"]
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()


        async with httpx.AsyncClient() as client:
            tries = 0
            while True:
                try:
                    # Getting cryptoscams lists
                    # print(httpx.get(address, headers=header).text)
                    response = await client.get(address, headers=header)
                    response.raise_for_status()

                    json_response = response.json()

                    for row in json_response:
                        writer.writerow(row)
                    break

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