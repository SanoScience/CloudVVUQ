import sys
import json
import asyncio
import warnings
from collections import defaultdict
from pathlib import Path

import aiohttp
import backoff
from tqdm import tqdm

from cloudvvuq.authorizer import Authorizer
from cloudvvuq.utils import status_map_repr


class CloudConnector:
    url: str
    output_dir: Path
    authorizer: Authorizer
    max_load: int

    def __init__(self, url: str, work_dir: [Path, str], cloud_provider: str, max_load: int):
        self.url = url
        self.output_dir = Path(work_dir, "outputs")
        self.authorizer = Authorizer(url, cloud_provider)
        self.max_load = max_load

        self.output_dir.mkdir(parents=True, exist_ok=True)

        if sys.platform.startswith('win') and sys.version_info[0] == 3 and sys.version_info[1] >= 8:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    def fetch_all(self, inputs: list[dict]):
        return asyncio.run(self._fetch_all(inputs))

    async def _fetch_all(self, inputs):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1000),
                                         timeout=aiohttp.ClientTimeout(total=3600)) as session:
            tasks = []
            sem = asyncio.Semaphore(self.max_load)
            pbar = tqdm(total=len(inputs))
            status_map = defaultdict(int)

            for input_data in inputs:
                task = asyncio.ensure_future(self.fetch_one(input_data, session, sem, pbar, status_map))
                tasks.append(task)

            results = await asyncio.gather(*tasks)
            pbar.close()

        if None in results:
            warnings.warn(f"Missing {results.count(None)} results. Use rerun_missing method.")
            results = [r for r in results if r is not None]

        return results

    @backoff.on_exception(backoff.constant, (aiohttp.ClientError, aiohttp.ServerDisconnectedError, asyncio.TimeoutError),
                          max_tries=7, raise_on_giveup=False)
    async def fetch_one(self, input_data, session, semaphore, pbar, status_map):
        headers = self.authorizer.sign_request(input_data)
        async with semaphore, session.post(self.url, headers=headers, json=input_data) as resp:
            status_map[resp.status] += 1
            pbar.set_postfix_str(status_map_repr(status_map))
            if resp.status == 200:
                result = await resp.json()
                self.save(result)
                pbar.update()
                return result
            else:
                resp.raise_for_status()

    def save(self, result):
        save_path = Path(self.output_dir, f"output_{result['input_id']}.json")
        with open(save_path, "w+") as f:
            json.dump(result, f, indent=4)
