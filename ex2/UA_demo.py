from fake_useragent import UserAgent
import time

# headers = {
#         'User-Agent':UserAgent().random
#         # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
#         # 'Cookie':'_ga=GA1.3.422496169.1677653943; iPlanetDirectoryPro=3doJr0toEZ409QRDMDciUh; device_token=cb5977e59effc7fd5d2aae420900bacb; public_product_id=xmu; session_sso_cookie_name=884a97444c62e40f601f29eccf57b204; fc_session=eyJpdiI6IlhOYVpIMnl1MkMrbVwvajJqTnNzZTlnPT0iLCJ2YWx1ZSI6IlhKYTdxSVExdjNNTytkN3JMb0c2OFVVd21XbHpITnVpUEo3d2JKelIza05sM0xYcU1VcXVXcDdhaFloa2xaV0gya21GK2ZEVVcwQkxCdDNMRjlBc05BPT0iLCJtYWMiOiI3NTJmZTEwNTIyZDk3N2FkMzM0OTk2YWM3NzRkNGM3Njk1ZmZlMzIxYzNmNGMzY2Q3OGU0OGIxMDUwODYzNjNmIn0=; _gat=1; session=V2-1-4e1b31e4-06b9-4679-8c1f-b7df035ebe3f.NTc1OTY.1680528173815.S89JHVLEdEjPZQlfkKLLRJGskL4'
#         }

while True:
    headers = {
        'User-Agent':UserAgent().random
        }

    print(headers['User-Agent'])
    time.sleep(0.5)