import asyncio
import aiohttp
import backoff
import warnings

from cloudvvuq.utils import get_gcp_token, batch_progress


def fatal_code(e):
    return None


@backoff.on_exception(backoff.expo, (aiohttp.ClientResponseError, aiohttp.ClientOSError, aiohttp.ServerDisconnectedError),
                      max_tries=7, on_giveup=fatal_code)
async def fetch(session, url, header, input_data):
    async with session.post(url, headers=header, json=input_data) as resp:
        if resp.status == 200:
            result = await resp.json()
            return result
        else:
            print(resp.status, resp.headers)
            resp.raise_for_status()

        return


async def run_simulations(inputs, url, require_auth, pbar):
    header = {'Content-Type': "application/json"}
    if require_auth:
        id_token = get_gcp_token(url)  # lifetime 1h
        header["Authorization"] = f"Bearer {id_token}"

    async with aiohttp.ClientSession() as session:
        tasks = []
        for input_data in inputs:
            tasks.append(asyncio.ensure_future(fetch(session, url, header, input_data)))

        results = []
        pbar.set_postfix_str(batch_progress(0, len(tasks)))
        for i, f in enumerate(asyncio.as_completed(tasks)):
            results.append(await f)
            pbar.set_postfix_str(batch_progress(i + 1, len(tasks)))

        if None in results:
            warnings.warn(f"Missing {results.count(None)} results.")
            results = [r for r in results if r is not None]

        results.sort(key=lambda x: x["input_id"])

    return results
