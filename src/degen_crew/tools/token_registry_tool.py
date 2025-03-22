#!/usr/bin/env python3

import requests
import json
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type, Dict, TypeAlias


TokenName: TypeAlias = str

class TokenRegistryToolInput(BaseModel):
    asset_id: str = Field(..., description="The asset ID of the token to be used in the query to the Token Registry API")

class TokenRegistryTool(BaseTool):  
    name: str = "TokenRegistryTool"
    description: str = "Uses the CardanoToken Registry API to fetch information about a given Cardano token"
    args_schema: Type[BaseModel] = TokenRegistryToolInput
    base_url: str = "The base URL of the Token Registry API"
    default_base_url: str = "https://tokens.cardano.org/metadata"

    def __init__(self, base_url: Optional[str] = None, **kwargs):     
        super().__init__(**kwargs)

        self.base_url = base_url or self.default_base_url

    def _run(self, asset_id: str) -> TokenName:
        try:
            sanitized_asset_id = asset_id.replace(".", "")
            response = requests.get(f"{self.base_url}/{sanitized_asset_id}")
            if response.status_code == 204 or not response.content:
                return None

            data = response.json()
            return data["name"]["value"]

        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return {"error": str(e)}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return {"error": str(e)}

   

# Example usage
if __name__ == "__main__":
    tool = TokenRegistryTool()
    result = tool._run("279c909f348e533da5808898f87f9a14bb2c3dfbbacccd631d927a3f.534e454b")
    print(result)
