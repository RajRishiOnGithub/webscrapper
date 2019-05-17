from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
#from openpyxl import Workbook
import os

try:
    while True:
        
        path = os.getcwd()
        print('CWD >'+path)
        print('\nEnter filename (e.g. filename.csv) : ',end='')
        filename = input()
        print('\n------OPTIONS-------')
        print("\n\n")
        print('1.CREATE NEW WORKBOOK ')
        print('2.APPEND ')
        print("\n>",end='')
        choice = input()
        if choice=="1":
            #headers="PROD_TITLE,PROD_LINK,PUB_DATE,ASIN,CATEGORY,SELL_PRICE,MRP,IMG_URL,MODEL,RATING\n"
            headers ="Amazon ASIN,Product Name,Product Categories,Selling Price,MRP,GST HSN Code,Model No:,Warranty,Return Policy,Highlights,Delivery in,Manufacturers,Product Image URL,Product Variations,Product Attributes,Product Shipping,Short Description,Long Description,Published,Product URL,COD,Sale,Hot,Trending,Verified,Cancellation,Rating\n"
            f = open(filename,"w")
            f.write(headers)

        else:
            f = open(filename,"a")

        try:
            
            while True:
                print('\nEnter product link here : ')
                print('>>',end='')
                first_url = input()
                urlClient = uReq(first_url)

                html_find = urlClient.read()

                urlClient.close()

                parsed_page = soup(html_find,"html.parser")

                #collects product title
                prod_title=''
                try:
                    
                    garbage_title = parsed_page.find('span',{'id':'productTitle'}).text

                    """ removing extra garbage (\n\t\r etc.) characters"""
                    word_list= garbage_title.split() 
                    prod_title=''
                    for i in word_list:
                        prod_title=prod_title+i+' '
                except AttributeError:
                    prod_title='NULL'
                    
                print('Product Title : '+prod_title)


                #collects published date of product on amazon
                date=''
                try:
                    x= parsed_page.select('tr.date-first-available > td')
                    if len(x)>=2:
                        date = x[1].text
                    else:
                        fshnDate = parsed_page.findAll('b',text=' Date first available at Amazon.in:')
                        if len(fshnDate)!=0:
                            date = fshnDate[0].nextSibling
                            
                    print('published date : '+date)
                except:
                    print('published date : '+date)


                #collects asin number
                    
                asin=''
                try:
                    
                    forasin = parsed_page.find('input',{'id':'ASIN'})

                    """
                    ///**trash**//
                    if len(forasin) is 0:
                            forasin = parsed_page.findAll('b',text='ASIN: ')
                            asin = forasin[0].nextSibling
                    else:
                    /*----*/
                    """

                    asin = forasin['value']
                except:
                    asin='NULL'
                print('ASIN :'+asin)
                    



                #collects category of the product
                cat =''
                try:                    
                    category = parsed_page.find('input',{'id':'storeID'})
                    cat = category['value']
                except:
                    cat='NULL'
                print('category : '+cat)


                #collects price which is displayed on the website after discount or SELLING PRICE
                #unparsedselling = parsed_page.find('span',{'id':'priceblock_dealprice'}).text.split()
                try:
                    unparsedselling = parsed_page.find('span',{'id':'priceblock_dealprice'}).text.split()
                except AttributeError:
                    try:
                        
                        unparsedselling = parsed_page.find('span',{'id':'priceblock_ourprice'}).text.split()        
                    except AttributeError:
                        try:                    
                            unparsedselling = parsed_page.find('span',{'id':'priceblock_saleprice'}).text.split()
                        except AttributeError:
                            unparsedselling=['NULL']
                        
                        
                sell_price = unparsedselling[0]
                sell_price=sell_price.replace(',','')
                print('selling price :'+sell_price)



                #collects maximum retail price which is without discount or STRIKED PRICE
                mrp=''
                try:
                    unparsedMrp =parsed_page.find('span',class_='priceBlockStrikePriceString a-text-strike').text.split()
                    mrp = unparsedMrp[0]
                except AttributeError:
                    mrp='NULL'
                mrp=mrp.replace(',','')
                print('MRP : '+mrp)



                #collects image url
                src=''
                try:                    
                    imgtag=parsed_page.find('img')
                    src= imgtag['src']
                except:
                    src='NULL'
                print('Link is : '+src)


                #collects item model number
                td_model=''
                try:
                    td = parsed_page.select('tr.item-model-number > td')
                    if len(td) is not 0:
                        td_model = td[1].text

                except IndexError:
                    td = parsed_page.findAll('td',text='Model Number')
                    if len(td)!=0:
                        td_model = td[0].nextSibling.text
                    
                print('item model number : '+td_model)


                #collects rating and reviews
                rating=''
                try:
                    unparsedrating =parsed_page.findAll('span',class_='a-icon-alt')
                    rating = unparsedrating[0].text
                except:
                    rating='NULL'
                print('Rating : '+rating)

                #f.write(prod_title+","+first_url+","+date+","+asin+","+cat+","+sell_price+","+mrp+","+src+","+td_model+","+rating+"\n")
                f.write(asin+","+prod_title+","+cat+","+sell_price+","+mrp+","+"  "+","+td_model+","+"  "+","+"  "+","+"  "+","+"  "+","+"  "+","+src+","+"  "+","+"  "+ ","+"  "+","+"  "+","+"  "+","+date+","+first_url+","+"  "+","+"  "+","+"  "+","+" "+","+" "+","+" "+","+rating+"\n")

        except KeyboardInterrupt:
            print('\nAll data saved to csv file ..DONE !\n\n')


        f.close()
except KeyboardInterrupt:
    print('\n\n------X.O.X.O--------\n')
    
