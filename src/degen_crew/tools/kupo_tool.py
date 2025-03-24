#!/usr/bin/env python3
import os
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
        base_url = base_url or os.getenv("KUPO_BASE_URL")
        if not base_url:
            raise ValueError("Either set KUPO_BASE_URL environment variable or pass base_url to KupoTool")
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
        
        for utxo in data:
            lovelace = utxo['value']
            assets_total["lovelace"] += int(lovelace['coins'])
            for asset_id, amount in lovelace['assets'].items():
                assets_total.setdefault(asset_id, 0)
                assets_total[asset_id] += int(amount)

        return assets_total

# Example usage
if __name__ == "__main__":
    import os
    tool = KupoTool(base_url=os.getenv("KUPO_BASE_URL"))
    # result = tool._run("addr_test1wz4ydpqxpstg453xlr6v3elpg578ussvk8ezunkj62p9wjq7uw9zq")
    result = tool._run("addr1qyf25say06zvrdtnmcd9w9tly3usy6ncse4cw2cdxd39w68qnc0v4cfl3sruk947cfmhd0ufgs32yxyzqdrufezp8h8qytuwkh")
    print(result)
