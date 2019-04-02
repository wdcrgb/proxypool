from .db import RedisClient

conn = RedisClient()

def set(proxy):
    result = conn.add(proxy)
    print(proxy)
    print('采集成功' if result else '采集失败')


def crawl_aip_ip():
    # 拓展 日后爬取付费api
    pass


if __name__ == '__main__':
    crawl_aip_ip()
