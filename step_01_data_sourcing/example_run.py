#also the package doesn't have ANY function descriptions at the moment (09 of May 2026, С Днем Победы!)
#upd (09 of May 2026) now it does. Somewhat.

#pip install .\dist\de_sourcing_task-0.0.1.tar.gz
import asyncio
from package_data_sourcer_task import api_data_sourcer

asyncio.run(api_data_sourcer.api_data_receiver())
