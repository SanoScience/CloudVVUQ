import asyncio
import aiohttp
import backoff
from tqdm import tqdm

from cloudvvuq.utils import get_gcp_token


def fatal_code(e):  # todo maybe another solution for faulty responses
    return None


@backoff.on_exception(backoff.expo, (aiohttp.ClientResponseError, aiohttp.ClientOSError),
                      max_tries=7, on_giveup=fatal_code)
async def fetch(session, url, header, input_data):
    async with session.post(url, headers=header, json=input_data) as resp:
        if resp.status == 200:
            result = await resp.json()
            # todo save response here? (to runs/run_id/outputs/...)
            return result
        else:
            print(resp.status)
            print(resp.headers)
            resp.raise_for_status()

        return


async def run_simulations(inputs, url, require_auth):
    header = {'Content-Type': "application/json"}
    if require_auth:  # todo add aws, azure etc?
        id_token = get_gcp_token(url)  # lifetime 1h  # todo add url validation?
        header["Authorization"] = f"Bearer {id_token}"

    async with aiohttp.ClientSession() as session:
        tasks = []
        for input_data in inputs:
            tasks.append(asyncio.ensure_future(fetch(session, url, header, input_data)))

        # results = await asyncio.gather(*tasks)  # preserves order of run_id but no tqdm
        results = [await f for f in tqdm(asyncio.as_completed(tasks), desc="Batch progress", total=len(tasks))]  # todo asyncio timeouterror
        results = [r for r in results if r is not None]  # todo test if necessary then add warning for missing outputs
        results.sort(key=lambda x: x["run_id"])  # todo change to sample_id

    return results
