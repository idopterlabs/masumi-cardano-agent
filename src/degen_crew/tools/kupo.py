#!/usr/bin/env python3

import requests
import json
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type, Dict

class KupoToolInput(BaseModel):
    cardano_address: str = Field(..., description="The Cardano address to query using the Kupo API")

class KupoTool(BaseTool):
    name: str = "KupoTool"
    description: str = "Uses the Kupo AI to fetch the total ADA amount stored in a given Cardano address"
    args_schema: Type[BaseModel] = KupoToolInput
    base_url: str = "The base URL of the Kupo API"

    def __init__(self, base_url: Optional[str] = None, **kwargs):     
        super().__init__(**kwargs)
        if not base_url:
            raise ValueError("base_url is required")
        self.base_url = base_url

    def _run(self, cardano_address: str) -> Dict[str, int]:
        try:
            data = requests.get(f"{self.base_url}/matches/{cardano_address}?unspent").json()
            fetched_assets = self._process_kupo_data(data)

            return fetched_assets

        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return {"error": str(e)}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return {"error": str(e)}

    def _process_kupo_data(self, data: list) -> Dict[str, int]:
        assets_total: Dict[str, int] = {"lovelace": 0}
        
        for item in data:
            if 'value' in item:
                value = item['value']
                if 'coins' in value:
                    assets_total["lovelace"] += int(value['coins'])
                if 'assets' in value:
                    for asset_id, amount in value['assets'].items():
                        if asset_id not in assets_total:
                            assets_total[asset_id] = 0
                        assets_total[asset_id] += amount
            return assets_total

# Example usage
if __name__ == "__main__":
    tool = KupoTool(base_url="")
    # result = tool._run("addr_test1wz4ydpqxpstg453xlr6v3elpg578ussvk8ezunkj62p9wjq7uw9zq")
    result = tool._run("addr_test1wpxs63au9yehzl8uhwkyjt84zhrf9slaflhhnvjtg7ukhks8sxm0t")
    print(result)
