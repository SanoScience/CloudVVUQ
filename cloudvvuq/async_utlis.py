import asyncio
import aiohttp
import backoff

from cloudvvuq.utils import get_gcp_token, batch_progress


def fatal_code(e):  # todo maybe another solution for faulty responses
    return None


@backoff.on_exception(backoff.expo, (aiohttp.ClientResponseError, aiohttp.ClientOSError),
                      max_tries=7, on_giveup=fatal_code)
async def fetch(session, url, header, input_data):
    async with session.post(url, headers=header, json=input_data) as resp:
        if resp.status == 200:
            result = await resp.json()
            # todo save response here? (to runs/input_id/outputs/...)
            return result
        else:
            print(resp.status)
            print(resp.headers)
            resp.raise_for_status()

        return


async def run_simulations(inputs, url, require_auth, pbar):
    header = {'Content-Type': "application/json"}
    if require_auth:  # todo add aws, azure etc?
        id_token = get_gcp_token(url)  # lifetime 1h  # todo add url validation?
        header["Authorization"] = f"Bearer {id_token}"

    async with aiohttp.ClientSession() as session:
        tasks = []
        for input_data in inputs:
            tasks.append(asyncio.ensure_future(fetch(session, url, header, input_data)))

        results = []
        pbar.set_postfix_str(batch_progress(0, len(tasks)))
        for i, f in enumerate(asyncio.as_completed(tasks)):  # todo asyncio timeouterror, .client_exceptions.ServerDisconnectedError:
            results.append(await f)
            pbar.set_postfix_str(batch_progress(i + 1, len(tasks)))

        results = [r for r in results if r is not None]  # todo test if necessary then add warning for missing outputs
        results.sort(key=lambda x: x["input_id"])

    return results
