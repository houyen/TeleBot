import requests
from bs4 import BeautifulSoup
import json
from Article import Article

baseUrl = "https://www.gamerpower.com/"

def GetGames(limit_games = 20): # Tạo biến limit để lấy số lượng tin mà mình cần thôi
    s = requests.Session() # Store sesstion lại
    response = s.get(baseUrl) # Thực hiện Get request
    soup = BeautifulSoup(response.content, 'html.parser') # Đưa vào biến soup chuẩn bị bóc tách dữ liệu
    article = soup.select("article.card-title text-truncate mt-n1 mb-1", limit=limit_games) # Tách dữ liệu phần thẻ article ra

    listArticle = []
    for element in article:
        title = element.select("a.card-title> a") # Lấy phần thẻ chứa title
        description = element.select("p.card-text truncate2 text-muted mb-2 mt-1> p") # Lấy phần thẻ chứa description
        for x in range(len(title)): # serialize object này lại thành json để lấy dữ liệu dễ dàng hơn
            listArticle.append(json.dumps(Article(title[x]['title'], title[x]['href'], description[x].text).__dict__, ensure_ascii=False))
    return listArticle
