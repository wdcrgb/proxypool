# Proxy池-模块说明

##### 由于爬虫业务大部分涉及电商、行业数据、资讯价值数据，被爬方一般为了反爬取，大部分会采用初级的反爬措施，其中较为常用的就是IP限制。
##### 为方便爬取网站，搭建了IP池模块，供大家可以使用。

* 项目结构：
```
proxypool
│   __init__.py
│   proxy_provider.txt    
│   requirements.txt 
│   run.py
│   README.md
└───proxypool
    │   __init__.py
    │   crawler.py
    │   db.py
    │   error.py  
    │   getter.py
    │   importer.py
    │   scheduler.py
    │   setting.py
    │   tester.py
    │   utils.py
    │

```

* IP代理池调用

  * 调用Get_Proxy()中的 process_request 返回随机得分高的IP
```python
import logging
import redis
from random import choice

class Get_Proxy():
    def __init__(self,host,port):
        self.logger = logging.getLogger(__name__)
        self.REDIS_KEY = 'proxies' #
        self.MAX_SCORE = 100
        # 连接数据库
        pool = redis.ConnectionPool(host=host,port=port)
        self.db = redis.StrictRedis(connection_pool=pool)

    def get_random_proxy(self):
        # 数据库拿数据IP，优先得分高的IP
        result = self.db.zrangebyscore(self.REDIS_KEY,self.MAX_SCORE,self.MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(self.REDIS_KEY,0,100)
            if len(result):
                return choice(result)
            else:
                raise EOFError    
    def process_request(self):
        proxy = self.get_random_proxy()
        if proxy:
            proxy_uri = 'http://{proxy}'.format(proxy=proxy.decode('utf-8'))
            self.logger.debug("正在使用代理："+proxy_uri)
            return proxy_uri
```
* 模块可分享点
  *  使用元类实现方法的自动调用[crawler.py]
  * 由于使用元类识别以crawl_的方法，因此拓展抓取方法请按crawl_XX 定义[crawler.py]

```python
class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)
```

```python
class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies
       
    def crawl_XX(self):

        XXXXXXXXX
```

* 添加测试网站（建议爬取哪个网站就添加哪个网站进入测试）[setting.py]

```python
# 测试，建议抓哪个网站测哪个
TEST_URL = [
    'https://tech.china.com/',
]
```

* 抓取的代理信息[proxy_provider.txt]
 

```
代理：
https://proxy.mimvp.com/free.php?proxy=in_hp
http://www.coobobo.com/free-http-proxy
http://ip.zdaye.com/
http://www.mayidaili.com/free/anonymous/%E9%AB%98%E5%8C%BF
http://http.taiyangruanjian.com/
http://http.zhimaruanjian.com/
http://ip.jiangxianli.com

66代理
云代理
快代理
西刺代理
无忧代理
免费IP代理
```














