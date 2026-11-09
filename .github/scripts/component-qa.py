import asyncio
import json
import os
from pathlib import Path
import site
import subprocess
import sys
import tempfile
import urllib.request
import venv

root=Path(sys.argv[1])
cfg=json.loads((root/'active.json').read_text(encoding='utf-8'))
for path in cfg.get('core_sites',[]):site.addsitedir(path)
from playwright.sync_api import sync_playwright
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
url='http://127.0.0.1:19345'
with sync_playwright() as playwright:
    browser=playwright.chromium.launch(headless=True,**({'executable_path':cfg['browser']} if cfg.get('browser') else {}))
    page=browser.new_page()
    page.goto(url+'/mcp')
    page.get_by_role('button',name='Kết nối Claude',exact=True).click()
    page.locator('#result').filter(has_text='Claude').wait_for()
    page.get_by_role('button',name='Kết nối Codex',exact=True).click()
    page.locator('#result').filter(has_text='Codex').wait_for()
    status=page.request.get(url+'/api/mcp-clients').json()
    assert status['claude']['configured'] and status['codex']['configured'],status
    browser.close()
conf=json.loads((Path(os.environ['APPDATA'])/'Claude/claude_desktop_config.json').read_text(encoding='utf-8'))
assert conf.get('unrelated')=='preserved' and 'other' in conf['mcpServers']
mcpconf=conf['mcpServers']['MuseAutoVid']
async def handshake():
    params=StdioServerParameters(command=mcpconf['command'],args=mcpconf['args'],env={**os.environ,**mcpconf['env']})
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            tools=await session.list_tools()
            assert any(tool.name=='muse_status' for tool in tools.tools)
            print('Configured Claude/Codex and completed real MCP stdio handshake',len(tools.tools),'tools.')
asyncio.run(handshake())
# Simulate an existing customer runtime using isolated .pth entries; never mutate source libraries.
external=root.parent/'customer-python'
venv.EnvBuilder(with_pip=False).create(external)
site_dir=external/'Lib/site-packages'
site_dir.mkdir(parents=True,exist_ok=True)
sites=list(dict.fromkeys([*cfg.get('core_sites',[]),*cfg.get('asr_sites',[])]))
(site_dir/'customer-libraries.pth').write_text('\n'.join(sites)+'\n')
python=external/'Scripts/python.exe'
env={**os.environ,'MUSE_CORE_PYTHON':str(python),'MUSE_ASR_PYTHON':str(python),
     'MUSE_FFMPEG':cfg['ffmpeg'],'MUSE_WHISPER_MODEL':cfg['model']}
if cfg.get('browser'):env['MUSE_BROWSER_EXECUTABLE']=cfg['browser']
if cfg.get('browser_cache'):env['PLAYWRIGHT_BROWSERS_PATH']=cfg['browser_cache']
manifest=next(root.glob('components-win.json'))
# Bootstrap helper copies are retained by the native installer in its own managed directory.
helper=next(root.glob('component_setup.py'))
import hashlib
expected=hashlib.sha256(manifest.read_bytes()).hexdigest()
second=root.parent/'reuse-components'
result=subprocess.run([str(python),'-I','-B',str(helper),'--root',str(second),'--manifest',str(manifest),
                       '--manifest-sha256',expected],env=env,capture_output=True,text=True,encoding='utf-8',timeout=600)
print(result.stdout[-10000:])
if result.returncode:
    print(result.stderr[-2000:])
    raise AssertionError('Existing-library installation failed')
events=[json.loads(line) for line in result.stdout.splitlines() if line.startswith('{')]
downloaded=[e['id'] for e in events if e.get('event')=='component' and e.get('state')=='downloading']
assert downloaded==['app'],downloaded
assert json.loads((second/'active.json').read_text())['model']==cfg['model']
print('Existing FFmpeg, Whisper, model, core and browser reused; only the app was downloaded.')
