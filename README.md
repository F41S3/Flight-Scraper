# Flight-Scraper
A simple python script making use of Selenium and BeautifulSoup to create an operations log for the day for a given airport.


I created this for a job I'm working to autogenerate an operational log of all flights handled that day. It is very special purpose in its first iteration.

Usage:
  Currently if you run the script all values and URLs are hardcoded. You will generate an operations log for flights at YHZ contracted with the company.
  

TODO:
  Make UI
  Add an option to select an airport
  Add an option to select n number of airlines
  Add an option to select a given date and only recieve those flights.
  Fix Sunwing interactions, currently the aircraft registration is not recorded. 
  Automatically note what flights took delays and by how much. 
  Comment code
  Refactor code to be more generalizable
