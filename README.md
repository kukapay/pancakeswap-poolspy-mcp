# PancakeSwap PoolSpy MCP Server

An MCP server that tracks newly created liquidity pools on Pancake Swap, providing real-time data for DeFi analysts, traders, and developers.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg)](https://www.python.org/)
[![smithery badge](https://smithery.ai/badge/@kukapay/pancakeswap-poolspy-mcp)](https://smithery.ai/server/@kukapay/pancakeswap-poolspy-mcp)

## Features

- **Real-Time Pool Tracking**: Fetches pools created within a specified time range (default: 5 minutes).
- **Customizable Queries**: Adjust the time range (in seconds) and the number of pools returned (default: 100).
- **Detailed Metrics**: Includes pool address, tokens, creation timestamp, block number, transaction count, volume (USD), and total value locked (USD).

## Prerequisites

- **Python 3.10+**: Ensure Python is installed on your system.
- **The Graph API Key**: Obtain an API key from [The Graph](https://thegraph.com/) to access the PancakeSwap subgraph.

## Installation

### Installing via Smithery

To install PancakeSwap PoolSpy for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@kukapay/pancakeswap-poolspy-mcp):

```bash
npx -y @smithery/cli install @kukapay/pancakeswap-poolspy-mcp --client claude
```

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/pancakeswap-poolspy-mcp.git
   cd pancakeswap-poolspy-mcp
   ```

2. **Install Dependencies**:
   Install the required Python packages using uv:
   ```bash
   uv add mcp[cli] httpx dotenv
   ```

3. **Client Configuration**
    ```json
    {
      "mcpServers": {
        "PancakeSwap-PoolSpy": {
          "command": "uv",
          "args": ["--directory", "path/to/pancakeswap-poolspy-mcp", "run", "main.py"],
          "env": {
            "THEGRAPH_API_KEY": "your api key from The Graph"
          }
        }
      }
    }
    ```

## Usage

### Running the Server

Run the server in development mode to test it locally:
```bash
mcp dev main.py
```
This launches the MCP Inspector, where you can interact with the `get_new_pools_bsc` tool.

### Available Tool

#### `get_new_pools_bsc(time_range_seconds: int = 300, limit: int = 100)`

Fetches a list of newly created PancakeSwap pools on BNB Smart Chain.

- **Parameters**:
  - `time_range_seconds` (int): Time range in seconds to look back for new pools. Default is 300 seconds (5 minutes).
  - `limit` (int): Maximum number of pools to return. Default is 100 pools.

- **Returns**: A formatted string listing pool details or an error message if the query fails.

- **Example Outputs**:
  - Default (last 5 minutes, up to 100 pools):
    ```bash
    get_new_pools_bsc()
    ```
    ```
    Newly Created Trading Pools (Last 5 Minutes, Limit: 100):
    Pool Address: 0x1234...5678
    Tokens: WETH/USDC
    Created At: 2025-03-16 12:00:00 UTC
    Block Number: 12345678
    Transaction Count: 10
    Volume (USD): 1234.56
    Total Value Locked (USD): 5678.90

    Pool Address: 0x9abc...def0
    Tokens: CAKE/BNB
    Created At: 2025-03-16 12:01:00 UTC
    Block Number: 12345679
    Transaction Count: 5
    Volume (USD): 789.12
    Total Value Locked (USD): 3456.78
    ```

  - Custom (last 10 minutes, up to 50 pools):
    ```bash
    get_new_pools(600, 50)
    ```
    ```
    Newly Created Trading Pools (Last 10 Minutes, Limit: 50):
    [pool details...]
    ```

### **Example Prompts**:

   - "list newly created PancakeSwap pools from the last 1 hours."
   - "Display PancakeSwap pools created within the last 2 minutes."

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
