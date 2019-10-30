from webscrap import wlog
from webscrap import wscrap

wlog.set_custom_log_info('html/error.log')

news_scrap= wscrap.WebScraper(wscrap.url, wlog)
news_scrap.retrieve_page()
news_scrap.write_data_as_html()
news_scrap.read_data_as_html()
news_scrap.convert_data_to_bs4()
news_scrap.soup_parse_to_simple_html()