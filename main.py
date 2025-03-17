from mcp.server.fastmcp import FastMCP
import httpx
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.getenv("THEGRAPH_API_KEY")
if not API_KEY:
    raise ValueError("THEGRAPH_API_KEY is not set in the .env file")
SUBGRAPH_URL = f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/A1fvJWQLBeUAggX2WQTMm3FKjXTekNXo77ZySun4YN2m"

# Initialize the MCP server
mcp = FastMCP("PancakeSwap-PoolSpy")

# Async function to query the subgraph using httpx
async def query_subgraph(query: str, variables: dict = None) -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        response = await client.post(SUBGRAPH_URL, json=payload)
        if response.status_code != 200:
            raise Exception(f"Subgraph query failed with status {response.status_code}: {response.text}")
        result = response.json()
        if "errors" in result:
            raise Exception(f"GraphQL errors: {json.dumps(result['errors'], indent=2)}")
        return result

# Fetch recently created pools with a customizable time range and limit
async def fetch_recent_pools(time_range_seconds: int = 300, limit: int = 100) -> list[dict]:
    time_ago = int((datetime.utcnow() - timedelta(seconds=time_range_seconds)).timestamp())
    query = """
    query RecentPools($timestamp: BigInt!, $limit: Int!) {
        pools(
            where: { createdAtTimestamp_gt: $timestamp }
            orderBy: createdAtTimestamp
            orderDirection: desc
            first: $limit
        ) {
            id
            token0 { symbol }
            token1 { symbol }
            createdAtTimestamp
            createdAtBlockNumber
            txCount
            volumeUSD
            totalValueLockedUSD
        }
    }
    """
    variables = {"timestamp": str(time_ago), "limit": limit}  # Convert timestamp to string for BigInt
    try:
        result = await query_subgraph(query, variables)
        pools = result.get("data", {}).get("pools", [])
        if not pools:
            print(f"No pools found for timestamp > {time_ago}. Response: {json.dumps(result, indent=2)}")
        return pools
    except Exception as e:
        print(f"Error in fetch_recent_pools: {str(e)}")
        raise

# MCP Tool: List newly created trading pools
@mcp.tool()
async def get_new_pools_bsc(time_range_seconds: int = 300, limit: int = 100) -> str:
    """
    Returns a list of trading pools created in the specified time range on Pancake Swap V3 BNB Smart Chain.

    Parameters:
        time_range_seconds (int): The time range in seconds to look back for new pools.
                                  Default is 300 seconds (5 minutes).
        limit (int): The maximum number of pools to return.
                     Default is 100 pools.
    """
    try:
        pools = await fetch_recent_pools(time_range_seconds=time_range_seconds, limit=limit)
        time_range_minutes = time_range_seconds // 60  # Convert to minutes for display
        output = f"Newly Created Trading Pools (Last {time_range_minutes} Minutes, Limit: {limit}):\n"
        for pool in pools:
            timestamp = datetime.fromtimestamp(int(pool["createdAtTimestamp"])).strftime('%Y-%m-%d %H:%M:%S')
            volume_usd = float(pool["volumeUSD"])  # Ensure float for formatting
            tvl_usd = float(pool["totalValueLockedUSD"])  # Ensure float for formatting
            output += (
                f"Pool Address: {pool['id']}\n"
                f"Tokens: {pool['token0']['symbol']}/{pool['token1']['symbol']}\n"
                f"Created At: {timestamp}\n"
                f"Block Number: {pool['createdAtBlockNumber']}\n"
                f"Transaction Count: {pool['txCount']}\n"
                f"Volume (USD): {volume_usd:.2f}\n"
                f"Total Value Locked (USD): {tvl_usd:.2f}\n\n"
            )
        return output if pools else f"No pools created in the last {time_range_minutes} minutes."
    except Exception as e:
        return f"Error fetching new pools: {str(e)}"

# Run the server
if __name__ == "__main__":
    mcp.run()
