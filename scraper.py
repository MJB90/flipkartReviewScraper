from selenium.webdriver.common.by import By
from contextlib import closing
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from cleaning import clean_content
import pandas as pd

temp_df = pd.DataFrame(columns=['Reviewer', 'Review_Date', 'Review_Title', 'Upvotes', 'Down_Votes', 'Content'])
file_name = "data.csv"


def remove_non_ascii_1(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


with closing(Firefox()) as browser:
    site = "https://www.flipkart.com/asus-zenfone-2-laser-ze550kl-black-16-gb/product-reviews" \
           "/itme9j58yzyzqzgc?pid=MOBE9J587QGMXBB7"
    browser.get(site)

    file = open("review.txt", "w")

    for count in range(1, 10):
        nav_btns = browser.find_elements_by_class_name('_2Xp0TH')

        button = ""

        for btn in nav_btns:
            number = int(btn.text)
            if number == count:
                button = btn
                break

        button.send_keys(Keys.RETURN)
        WebDriverWait(browser, timeout=10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_2xg6Ul")))

        read_more_btns = browser.find_elements_by_class_name('_1EPkIx')

        for rm in read_more_btns:
            browser.execute_script("return arguments[0].scrollIntoView();", rm)
            browser.execute_script("window.scrollBy(0, -150);")
            rm.click()

        page_source = browser.page_source

        soup = BeautifulSoup(page_source, "lxml")
        ans = soup.find_all("div", class_="_1PBCrt")

        for tag in ans:
            # code to extract the title from each review
            title = unicode(tag.find("p", class_="_2xg6Ul").string).replace(u"\u2018", "'").replace(
                u"\u2019", "'")
            title = remove_non_ascii_1(title)
            title.encode('ascii', 'ignore')

            # code to extract the reviewer's name
            reviewer = unicode(tag.find("p", class_="_3LYOAd _3sxSiS").string).replace(u"\u2018", "'").replace(
                u"\u2019", "'")
            reviewer = remove_non_ascii_1(reviewer)
            reviewer.encode('ascii', 'ignore')

            # code to extract the date when review was posted
            date_array = tag.find_all("p", class_="_3LYOAd")

            posting_date = unicode(date_array[1].string).replace(u"\u2018", "'").replace(
                u"\u2019", "'")
            posting_date = remove_non_ascii_1(posting_date)
            posting_date.encode('ascii', 'ignore')

            # rating = tag.find("div", class_="hGSR34 E_uFuv").string
            # rating = rating[26]

            # code to extract the review content
            content = tag.find("div", class_="qwjRop").div.prettify().replace(u"\u2018", "'").replace(
                u"\u2019", "'")
            content = remove_non_ascii_1(content)
            content.encode('ascii', 'ignore')
            content = content[15:-7]
            content = clean_content(content)

            votes = tag.find_all("span", class_="_1_BQL8")
            upvotes = int(votes[0].string)
            downvotes = int(votes[1].string)

            file.write("Reviewer Name: %s\n\n" % reviewer)
            file.write("Reviewing Date: %s\n\n" % posting_date)
            # file.write("Rating: %s\n\n" % rating)
            file.write("Review Title : %s\n\n" % title)
            file.write("Upvotes : " + str(upvotes) + "\n\nDownvotes : " + str(downvotes) + "\n\n")
            file.write("Review Content :\n%s\n\n\n\n" % content)
            temp_df.loc[-1] = [reviewer, posting_date, title, upvotes, downvotes, content]
            temp_df.index = temp_df.index + 1

    file.close()
    temp_df.to_csv(file_name, index=False)

