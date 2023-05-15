import chromedriver_autoinstaller
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import csv

# 카페 게시글 제목,링크를 저장하는 리스트 생성
total_list = ['제목', '링크']

# 데이터를 저장하는 csv파일 생성
f = open('craw.csv', 'w', encoding="euc-kr", newline='')
wr = csv.writer(f)
wr.writerow([total_list[0], total_list[1]])
f.close()

# 변수 기본값 지정
url = 'https://nid.naver.com/nidlogin.login'
id = "네이버아이디"
pw = "네이버비밀번호"

# 크롬 드라이버는 이렇게 실행해야지 편하게 작업이 가능합니다.
# 자동으로 크롬 버전을 확인하는 코드chromedriver_autoinstaller
dir_driver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver = webdriver.Chrome(f'./{dir_driver}/chromedriver.exe')
driver.get(url)

driver.implicitly_wait(2)

# execute_script 함수 사용하여 자바스크립트로 id,pw 넘겨주기
driver.execute_script("document.getElementsByName('id')[0].value=\'" + id + "\'")
driver.execute_script("document.getElementsByName('pw')[0].value=\'" + pw + "\'")

# 로그인 버튼 클릭하기
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
time.sleep(1)

# 로그인 정보 저장안함 클릭하기
# login_btn = driver.find_element_by_id('new.dontsave')
# login_btn.click()
# time.sleep(1)

# 내가 검색하려는 카페 주소 입력하기
baseurl = 'https://cafe.naver.com/battlegroundsmobile/'
driver.get(baseurl)

# &search.menuid = : 게시판 번호
# &search.page = : 데이터 수집 할 페이지 번호
# &userDisplay = 50 : 한 페이지에 보여질 게시글 수

clubid = 카페
클럽
ID
번호
입력
menuid = 메뉴
ID
번호
입력
pageNum = 1
userDisplay = 50

driver.get(
    baseurl + 'ArticleList.nhn?search.clubid=' + str(clubid) + '&search.menuid=' + str(menuid) + '&search.page=' + str(
        pageNum) + '&userDisplay=' + str(userDisplay))

# iframe으로 접근
driver.switch_to.frame('cafe_main')

soup = bs(driver.page_source, 'html.parser')

print(str(soup))

soup = soup.find_all(class_='article-board m-tcol-c')[1]

# 네이버 카페 구조 확인후 게시글 내용만 가저오기

# datas = soup.find_all('td', class_ = 'td_article')

datas = soup.find_all(class_='td_article')
dates = soup.find_all(class_='td_date')

for data in datas:
    article_title = data.find(class_='article')
    link = article_title.get('href')
    article_title = article_title.get_text().strip()

    print(article_title)
    print(baseurl + link)

    # 인코딩은 utf-8이 좋아 보임

    f = open('craw.csv', 'a+', newline='', encoding='utf-8')

    wr = csv.writer(f)
    wr.writerow([article_title, baseurl + link])
    f.close()

print('종료')

# driver.close()