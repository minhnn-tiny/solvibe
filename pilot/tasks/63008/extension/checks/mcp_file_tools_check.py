# Path and behaviour checks of the study MCP server, through a real MCP client (no model).
import asyncio, json
from fastmcp import Client
async def main():
    cfg = {"mcpServers": {"study": {"command": "/opt/openhands/bin/python",
           "args": ["/opt/study/mcp_server.py", "--files"], "env": {"STUDY_PROJECT": "/work"}}}}
    async with Client(cfg) as c:
        tools = sorted(t.name for t in await c.list_tools())
        print("tools:", tools)
        async def call(name, **kw):
            try:
                r = await c.call_tool(name, kw)
                return "OK  " + (r.content[0].text if r.content else "")[:80].replace("\n", " | ")
            except Exception as e:
                return "ERR " + str(e)[:110]
        for name, kw in [("read_file", {"path": "a.txt"}), ("read_file", {"path": "../outside.txt"}),
                         ("read_file", {"path": "/etc/passwd"}), ("read_file", {"path": "link_out"}),
                         ("list_dir", {"path": "sub/etclink"}), ("write_file", {"path": "../evil.txt", "content": "x"}),
                         ("write_file", {"path": "link_out", "content": "x"}), ("write_file", {"path": "new/b.txt", "content": "hi\n"}),
                         ("replace_in_file", {"path": "new/b.txt", "old": "hi", "new": "bye"}), ("read_file", {"path": "new/b.txt"}),
                         ("search_text", {"pattern": "bye"}), ("list_dir", {"path": "."})]:
            print(name, json.dumps(kw)[:50], "->", await call(name, **kw))
asyncio.run(main())
