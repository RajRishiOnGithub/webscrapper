from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#first_url = 'https://www.amazon.in/Sony-MDR-ZX110A-Stereo-Headphones-without/dp/B00KGZZ824?pd_rd_w=rcvBV&pf_rd_p=e6322eff-fb5e-4cc4-8cef-e41c114df71b&pf_rd_r=NTCPZMDHC2J71Y312CTE&pd_rd_r=6d8436bd-5f1a-43a7-af70-aeff235252da&pd_rd_wg=Sd3Bc&ref_=pd_gw_cr_simh'
#first_url = 'https://www.amazon.in/dp/B07KXC1YGG/ref=br_msw_pdt-2?_encoding=UTF8&smid=A14CZOWI0VEHLG&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=&pf_rd_r=NTCPZMDHC2J71Y312CTE&pf_rd_t=36701&pf_rd_p=2b9bb3c1-71bb-48bb-8476-31c6e37895b1&pf_rd_i=desktop'

#first_url = 'https://www.amazon.in/IKALL-N9-7-inch-Calling-Tablet/dp/B078JY86CB/ref=lp_15613852031_1_2_sspa?s=computers&ie=UTF8&qid=1557905774&sr=1-2-spons&psc=1'
#first_url = 'https://www.amazon.in/dp/B07M67SVGP/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B07M67SVGP&pd_rd_w=bzoZx&pf_rd_p=02c0700e-cd85-479f-b670-81a01283e38b&pd_rd_wg=hA1gK&pf_rd_r=Y0VSSGWD5TJRKY11CSE2&pd_rd_r=a90fc818-770b-11e9-9b14-ad0a6ddaf222&smid=A2FER3EHWPU1WG'
#first_url = 'https://www.amazon.in/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_electronics_sr_pg1_1?ie=UTF8&adId=A0271211RWQN4XVRJ583&url=%2FHP-Desktop-C2500-Keyboard-Mouse%2Fdp%2FB00CSK1WC0%2Fref%3Dsr_1_1_sspa%3Fcrid%3D2ZA1SJ5YQHG6I%26keywords%3Dkeyboard%2Bmouse%2Bcombo%26qid%3D1557923038%26s%3Delectronics%26sprefix%3Dkey%252Celectronics%252C383%26sr%3D1-1-spons%26psc%3D1&qualifier=1557923038&id=8861553758614490&widgetName=sp_atf'



print('Enter product link here : ')
first_url = input()
urlClient = uReq(first_url)

html_find = urlClient.read()

urlClient.close()

parsed_page = soup(html_find,"html.parser")

#collects product title
prod_title = parsed_page.find('span',{'id':'productTitle'})
print('Product Title : '+prod_title.text)


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
print('ASIN :'+asin)
    



#collects category of the product 
category = parsed_page.find('input',{'id':'storeID'})
print('category : '+category['value'])


#collects price which is displayed on the website after discount or SELLING PRICE
#unparsedselling = parsed_page.find('span',{'id':'priceblock_dealprice'}).text.split()
try:
    unparsedselling = parsed_page.find('span',{'id':'priceblock_dealprice'}).text.split()
except AttributeError:
    unparsedselling = parsed_page.find('span',{'id':'priceblock_ourprice'}).text.split()
except AttributeError:
    unparsedselling=['NULL']
        
        
sell_price = unparsedselling[0]
print('selling price :'+sell_price)



#collects maximum retail price which is without discount or STRIKED PRICE
unparsedMrp =parsed_page.find('span',class_='priceBlockStrikePriceString a-text-strike').text.split()
mrp = unparsedMrp[0]
print('MRP : '+mrp)



#collects image url
imgtag=parsed_page.find('img')
src= imgtag['src']
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
unparsedrating =parsed_page.findAll('span',class_='a-icon-alt')
rating = unparsedrating[0].text
print('Rating : '+rating)
