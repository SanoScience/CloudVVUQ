import sys
import json
import asyncio
import warnings
from pathlib import Path

import aiohttp
import backoff
from tqdm import tqdm

from cloudvvuq.auth import get_gcp_token, aws_sign_headers


class CloudConnector:
    url: str
    output_dir: Path
    cloud_provider: str
    max_load: int

    def __init__(self, url, work_dir, cloud_provider, max_load):
        self.url = url
        self.output_dir = Path(work_dir, "outputs")
        self.cloud_provider = cloud_provider
        self.max_load = max_load

        self.output_dir.mkdir(parents=True, exist_ok=True)

        if sys.platform.startswith('win') and sys.version_info[0] == 3 and sys.version_info[1] >= 8:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    def send_and_receive(self, inputs):
        return asyncio.run(self._send_and_receive(inputs))

    async def _send_and_receive(self, inputs):
        header = {'Content-Type': "application/json"}
        if self.cloud_provider == "gcp":
            id_token = get_gcp_token(self.url)  # lifetime 1h
            header["Authorization"] = f"Bearer {id_token}"

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1000)) as session:
            tasks = []
            pbar = tqdm(total=len(inputs))
            sem = asyncio.Semaphore(self.max_load)

            for input_data in inputs:
                tasks.append(asyncio.ensure_future(self.fetch_and_save(session, header, input_data, sem, pbar)))

            results = await asyncio.gather(*tasks)
            pbar.close()

        if None in results:
            warnings.warn(f"Missing {results.count(None)} results. Use rerun_missing method.")
            results = [r for r in results if r is not None]

        results.sort(key=lambda x: x["input_id"])

        return results

    @backoff.on_exception(backoff.constant, (aiohttp.ClientResponseError, aiohttp.ClientOSError,
                                             aiohttp.ServerDisconnectedError),
                          max_tries=7, raise_on_giveup=False)
    async def fetch_and_save(self, session, header, input_data, semaphore, pbar):
        if self.cloud_provider == "aws":
            header = {**header, **aws_sign_headers(self.url, input_data)}
        async with semaphore, session.post(self.url, headers=header, json=input_data) as resp:
            if resp.status == 200:
                result = await resp.json()
                self.save(result)
                pbar.update()
                return result
            else:
                print(resp.status, resp.headers)
                resp.raise_for_status()

            return

    def save(self, result):
        save_path = Path(self.output_dir, f"output_{result['input_id']}.json")
        with open(save_path, "w+") as f:
            json.dump(result, f, indent=4)
