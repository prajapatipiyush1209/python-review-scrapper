from flask import Flask,render_template,request
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
import socket

logging.basicConfig(level=logging.INFO,filename="app.log", format= '%(asctime)s - %(levelname)s-%(message)s {}'.format(socket.gethostbyname(socket.gethostname())))

application = Flask(__name__)
app=application
@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/review", methods = ['POST'])
def review():
    if request.method == "POST":
        logging.info("Post Method called")
        searching_item = request.form['content'].replace(" ", "")
        flipkart_url = "https://www.flipkart.com/search?q="  + searching_item
        uclient = uReq(flipkart_url)
        flipkartpage= uclient.read()
        logging.info("read html data")
        uclient.close()
        print(flipkartpage)
        product_html=bs(flipkartpage, "html.parser")
        print(product_html)
        bigboxes = product_html.findAll("div", {"class":"_1AtVbE col-12-12"})
        print(bigboxes)
        print(len(bigboxes))
        box = bigboxes[2]
        productlink = "https://www.flipkart.com" + box.div.div.div.a['href']
        logging.info("retrive the product link")
        print(productlink)
        productreq = requests.get(productlink)
        logging.info("Response {}".format(productlink))
        print(request)
        prod_html = bs(productreq.text, "html.parser")
        comment_box = prod_html.find_all("div", {"class": "_16PBlm"})
        reviews=[]
        for i in comment_box:
        
            try:
                rating=i.div.div.div.div.text
            except:
                rating = 'No rating'


        
            try :
                comment=i.div.div.find_all("div", {"class": ""})[0].div.text    
            except Exception as e:
                print("Exception while creating dictionary: ",e)

            

            try :
                heading=i.div.div.div.p.text
            except:
                heading = 'No Comment Heading'

        

            try :
                cust_name = i.find_all("p", {"class": "_2sc7ZR _2V5EHH"})[0].text

            except Exception as e:
                cust_name = "No name"
                logging.error(e)

            mydict= {"Product": searching_item,"rating": rating, "comment": comment, "comment_heading": heading ,"cust_name":cust_name}    
            reviews.append(mydict)
        print(reviews)

        print(len(reviews))
        return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])

if __name__ == "__main__":
    app.run(debug=True)


