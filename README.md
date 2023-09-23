Hello Lego scientists ;)

Here is a bunch of inrotmation which can be useful for us during using these scipts.

1. Brikcset login.
   For using Brikset API you need to create free account and generate api token here:
     https://brickset.com/tools/webservices/requestkey
   Then update the variables in file "brickset_download.py" with your data:
     apiKey = ''
     username = ''
     password = ''
   Also useful can be the documentation about queries in Brickset:
     https://brickset.com/tools/webservices/requestkey
2. The order of running files to get similar files like ours:
  2.1. brickset_download.py
  2.2. status_download.py
  2.3. links_download.py
  2.4. retail_price_poland_add.py
  2.5. history_price_add.py
  2.6. data_processing.py
3. Remember you can modify parameters in code like for example range of history prices (in default it is from 06.2018 to 06.2023)

If you have any questions please write emails to:
bartosz.tomasz.podgorski@gmail.com
wiktoria.szczepanska.wsz@gmail.com
