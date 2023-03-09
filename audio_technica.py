import os
import requests
from time import sleep
from tqdm import tqdm
from bs4 import BeautifulSoup
from discordwebhook import Discord

forever = True
while (forever):
  URL = "https://outlet.audio-technica.com/all-products?product_list_limit=all"
  discord = Discord(url=os.getenv('DISCORD_WEBHOOK'))
  
  page = requests.get(URL)
  
  soup = BeautifulSoup(page.content, "html.parser")
  
  product_list = []
  price_list = []
  url_list = []
  
  for items in soup.find_all("div", class_="c-product__title"):
      product_list.append(items.text)
  
  for items in soup.find_all("span", class_="price"):
      price_list.append(items.text)
  
  for items in soup.find_all("a", class_="c-product__button", href=True):
      url_list.append(items['href'])
  
  my_watchlist = open("/home/watchlist.txt").read().splitlines()
  
  watchlist_items = []
  watchlist_prices = []
  watchlist_urls = []
  
  listing_volume = len(product_list) - 1
  
  print("--- All Items ---")
  
  while listing_volume > -1:
    print(product_list[listing_volume] + " - " + price_list[listing_volume] + " - " + url_list[listing_volume])
    if product_list[listing_volume] in my_watchlist:
       watchlist_items.append(product_list[listing_volume])
       watchlist_prices.append(price_list[listing_volume])
       watchlist_urls.append(url_list[listing_volume])
    listing_volume -= 1
  
  watchlist_volume = len(watchlist_items) - 1
  
  print("\n--- Watchlist Items Found ---")
  
  while watchlist_volume > -1:
    print(watchlist_items[watchlist_volume] + " - " + watchlist_prices[watchlist_volume] + " - " + watchlist_urls[watchlist_volume])
    discord.post(content="Item Available: " + watchlist_items[watchlist_volume] + " - " + watchlist_prices[watchlist_volume] + " - " + watchlist_urls[watchlist_volume])
    watchlist_volume -= 1

  print("\nWaiting for next refresh:")

  for i in tqdm(range(7200)):
      sleep(1)
