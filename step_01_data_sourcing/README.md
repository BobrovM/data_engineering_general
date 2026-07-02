# STEP 1: DATA SOURCING LAYER

This folder contains solution to the task of:

1. Make a python code for exstracting data from API, which contains less than 2Gigs of information, uses pagination when extracting and sleeps for 3 minutes when stumbles upon 429 status, since the "too much requests" timeout is 3 minutes in here.
2. Make the code as a package, and makeit into an installable module.
3. Test it trough any other python script as an installable module and as a cmd or bash command.

The contains are:

* package developing folder (**data\_sourcer\_task/package\_data\_sourcer\_task**) with all dev files;
* installable module (**data\_sourcer\_task/dist**);
* example\_run.py as an example that the module works;
* txt file with a link to sourced data Google Drive folder, since unpacked it weights \~1,31Gigs. Packed it weights \~308Mb.

The **main code** is in ***data\_sourcer\_task/package\_data\_sourcer\_task/api\_data\_sourcer.py*.**



The task has hard-coded ip with api.

The code handles 429 and other request exceptions.

