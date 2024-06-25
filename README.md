[NOTICE: This is provided as-is and likely will not function as described below.]

This is a useful project for scraping items from temu.com to list on your e-commerce site. 

![temu](https://github.com/n1ceh4t/Temu-Item-Scraper/assets/119663530/9fc4afb2-f9f2-49c5-804c-09d6f0559caf)


It includes support for the Woo-Commerce API (WCAPI.)

It will automatically upload pictures and adjust prices as well as generate product descriptions using chatGPT to your WooCommerce inventory. 

The items will be inactive until reviewed by a human and activated through wordpress, but this takes a lot of the difficulty out of populating inventory for your dropshipping business.

Included is a web panel, (***This should only be run locally, as system calls are made***,) and it does the job well but only imports one item at a time. 
You can also run temu.py and use the command-line interface. If I remember correctly, functions exist to add top items from search as a batch. This will take some time.


Getting this to work for you will take no small amount of code review and alterations. You will have to manually change your categories in temu.py, dash-dev.py and ip.html

Some features may not work all of the time, as temu tries to prevent this kind of thing from happening. Rate-limiting and the pop-up spinner can cause the search to fail. 
Also, you may need to update the token from an actual search for it to work.

However, some people may find this useful and was a fun/lucrative project.

USE AT YOUR OWN RISK.
