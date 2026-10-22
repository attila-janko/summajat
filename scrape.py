import requests
from bs4 import BeautifulSoup

# define URLs
urls = [
  #  'https://444.hu/',
     'https://hvg.hu/',
    #  'https://telex.hu/',
    # 'https://portfolio.hu/',
    # 'https://www.blikk.hu/',
    # 'https://index.hu/',
    # 'https://24.hu/'
]

oldalak = {'title': [], 'link': []}

for url in urls:
    # send request to the website
    response = requests.get(url)
    # parse HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # find the article title and link
    article_title = soup.find('h1', class_='heading-1').text.strip()
    article_link = soup.find('h1', class_='heading-1').find('a')['href']
    article_link = url + article_link
    # print the results
    print(f"{url} \nTitle: {article_title} \nLink: {article_link}\n")
    oldalak = {'title': article_title, 'link': article_link}
#print the first item of article_link

#find all the links from the main page
links =  soup.find_all('h1',class_='heading-3')
print(links)
# get the urls from link and store them in link_n
link_n = []
for link in links:
    link_n.append(url + link.find('a')['href'])

print(link_n)

text = link_n[2]
print(text)
# send request to the website
response = requests.get(text)
# parse HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

#find class="article-datetime" from div and store it in date
date = soup.find('time', class_='article-datetime').text.strip()
print(date)

#replace hungarian name to english
date = date.replace('január', 'January')
date = date.replace('február', 'February')
date = date.replace('március', 'March')
date = date.replace('április', 'April')
date = date.replace('május', 'May')
date = date.replace('június', 'June')
date = date.replace('július', 'July')
date = date.replace('augusztus', 'August')
date = date.replace('szeptember', 'September')
date = date.replace('október', 'October')
date = date.replace('november', 'November')
date = date.replace('december', 'December')

#convert into datetime
from datetime import datetime
date = datetime.strptime(date, '%Y. %B. %d. %H:%M')

#find class="main " from div


article_main = soup.find("div", class_="article-main")

# Find all 'embed-container' divs within the 'article-main' div
embed_containers = article_main.find_all("div", class_="embed-container")

# Remove all 'embed-container' divs found
for embed_container in embed_containers:
    embed_container.decompose()

# Print the modified 'article-main' div content
text = article_main.text.strip()

print(text)

#set up chat GPT api
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")


#shorten the text to 1024 characters and make it a string
text = str(text[:1024])
# Let's ask chatgpt to summarize the text in bulletpoints
input_ids = tokenizer.encode(text, return_tensors="pt")
chat_history_ids = model.generate(
    input_ids,
    max_length=1000,
    pad_token_id=tokenizer.eos_token_id,
    no_repeat_ngram_size=3,
    do_sample=True,
    top_k=10,
    top_p=0.7,
    temperature=0.8
)

# Print the output
print("ChatGPT: ", tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True))


