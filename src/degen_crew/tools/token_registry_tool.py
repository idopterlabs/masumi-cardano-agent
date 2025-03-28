#!/usr/bin/env python3

import requests
import json
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type, Dict, TypeAlias, List


TokenName: TypeAlias = str
AssetId: TypeAlias = str

class TokenRegistryToolInput(BaseModel):
    asset_ids: List[AssetId] = Field(..., description="A list of asset IDs to be used in the query to the Token Registry API")

class TokenRegistryTool(BaseTool):  
    name: str = "TokenRegistryTool"
    description: str = "Uses the CardanoToken Registry API to fetch information about a set of Cardano tokens"
    args_schema: Type[BaseModel] = TokenRegistryToolInput
    base_url: str = "The base URL of the Token Registry API"
    default_base_url: str = "https://tokens.cardano.org/metadata/query"

    def __init__(self, base_url: Optional[str] = None, **kwargs):     
        super().__init__(**kwargs)
        self.base_url = base_url or self.default_base_url

    def _run(self, asset_ids: List[AssetId]) -> Dict[AssetId, TokenName]:
        try:
            if len(asset_ids) > 10:
                raise ValueError("The maximum number of asset IDs is 10")
            
            # Create a mapping of sanitized to original asset IDs
            asset_id_mapping = {asset_id.replace(".", ""): asset_id for asset_id in asset_ids}
            sanitized_asset_ids = list(asset_id_mapping.keys())
            
            response = requests.post(f"{self.base_url}", json={"subjects": sanitized_asset_ids})
            if response.status_code == 204 or not response.content:
                return {aid: None for aid in asset_ids}

            response_data = response.json()
            # Create mapping of asset ID to token name
            token_names = {}
            for subject in response_data["subjects"]:
                # Get the original asset ID from our mapping
                original_asset_id = asset_id_mapping.get(subject['subject'])
                if original_asset_id:
                    token_names[original_asset_id] = subject["name"]["value"]

            # Ensure all input asset IDs are in the result, even if not found
            for aid in asset_ids:
                if aid not in token_names:
                    token_names[aid] = None
                    
            return token_names

        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return {aid: None for aid in asset_ids}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return {aid: None for aid in asset_ids}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {aid: None for aid in asset_ids}

# Example usage
if __name__ == "__main__":
    tool = TokenRegistryTool()
    result = tool._run(["279c909f348e533da5808898f87f9a14bb2c3dfbbacccd631d927a3f.534e454b", 
    "c863ceaa796d5429b526c336ab45016abd636859f331758e67204e5c.4353574150", 
    "95a427e384527065f2f8946f5e86320d0117839a5e98ea2c0b55fb00.48554e54",
    "2274b1699f5398170e0497598de7877ebb370ba7b5d25a1d0b2fea07.5249534b"])
    print(result)
