import asyncio
import json
from pathlib import Path

import aiohttp
import backoff
import warnings

from cloudvvuq.utils import get_gcp_token, batch_progress


def fatal_code(e):
    return None


class CloudConnector:
    url: str
    output_dir: Path
    require_auth: bool

    def __init__(self, url, work_dir, require_auth):
        self.url = url
        self.output_dir = Path(work_dir, "outputs")
        self.require_auth = require_auth

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def send_and_receive(self, inputs, pbar):
        return asyncio.run(self._send_and_receive(inputs, pbar))

    async def _send_and_receive(self, inputs, pbar):
        header = {'Content-Type': "application/json"}
        if self.require_auth:
            id_token = get_gcp_token(self.url)  # lifetime 1h
            header["Authorization"] = f"Bearer {id_token}"

        async with aiohttp.ClientSession() as session:
            tasks = []
            for input_data in inputs:
                tasks.append(asyncio.ensure_future(self.fetch_and_save(session, header, input_data)))

            results = []
            pbar.set_postfix_str(batch_progress(0, len(tasks)))
            for i, f in enumerate(asyncio.as_completed(tasks)):
                results.append(await f)
                pbar.set_postfix_str(batch_progress(i + 1, len(tasks)))

        if None in results:
            warnings.warn(f"Missing {results.count(None)} results. Use rerun_missing method.")
            results = [r for r in results if r is not None]

        results.sort(key=lambda x: x["input_id"])

        return results

    @backoff.on_exception(backoff.expo, (aiohttp.ClientResponseError, aiohttp.ClientOSError,
                                         aiohttp.ServerDisconnectedError),
                          max_tries=7, on_giveup=fatal_code)
    async def fetch_and_save(self, session, header, input_data):
        async with session.post(self.url, headers=header, json=input_data) as resp:
            if resp.status == 200:
                result = await resp.json()
                self.save(result)
                return result
            else:
                print(resp.status, resp.headers)
                resp.raise_for_status()

            return

    def save(self, result):
        save_path = Path(self.output_dir, f"output_{result['input_id']}.json")
        with open(save_path, "w+") as f:
            json.dump(result, f)





