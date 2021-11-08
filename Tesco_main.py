# author Dominik Capkovic 
# contact: domcapkovic@gmail.com; https://www.linkedin.com/in/dominik-čapkovič-b0ab8575/
# GitHub: https://github.com/kilimetr



import bs4 as BeautifulSoup
import requests 
import datetime



def Tesco_main_fun():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
			   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

	source_letaky = requests.get("https://www.kupi.cz/letaky/tesco#sgc=tesco", 
								 headers = headers)

	if source_letaky.status_code != 200:
		print("něco je zle - source")
	else:
		print("access granted")


	soup_letaky = BeautifulSoup.BeautifulSoup(source_letaky.text, "lxml")
	letaky      = soup_letaky.find_all("a", class_ = "item_content")

	for letak in letaky:
		HypermarketLetak = letak.find("strong", itemprop = "name").text
		HypermarketLetak = str(HypermarketLetak)
	
		response = "hypermarket leták" in HypermarketLetak
	
		if response == True:
			StartDate = letak.find("span", itemprop = "startDate")["content"]
			EndDate   = letak.find("span", itemprop = "endDate")["content"]
		
			StartDate = datetime.datetime.strptime(StartDate, "%Y-%m-%d").date()
			EndDate   = datetime.datetime.strptime(EndDate,   "%Y-%m-%d").date()
		
			TodayDate = datetime.date.today()
		
			if StartDate <= TodayDate <= EndDate:
				ODKAZ = letak["href"]
				print(ODKAZ)
				print("mezi datumy")
			
			else:
				print("mimo datumy")
				print()
				print()
		
		else:
			print("not hypermarket")
			print()
	
	print("TESCO MAIN BYL SPUŠTĚN")

	return ODKAZ
	

