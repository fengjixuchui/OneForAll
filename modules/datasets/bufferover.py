import cloudscraper
from common.query import Query
from config.log import logger


class BufferOver(Query):
    def __init__(self, domain):
        Query.__init__(self)
        self.domain = domain
        self.module = 'Dataset'
        self.source = 'BufferOverQuery'
        self.addr = 'https://dns.bufferover.run/dns?q='

    def query(self):
        """
        向接口查询子域并做子域匹配
        """
        # 绕过cloudFlare验证
        scraper = cloudscraper.create_scraper()
        scraper.proxies = self.get_proxy(self.source)
        url = self.addr + self.domain
        try:
            resp = scraper.get(url, timeout=self.timeout)
        except Exception as e:
            logger.log('ERROR', e.args)
            return
        if resp.status_code != 200:
            return
        self.subdomains = self.collect_subdomains(resp)

    def run(self):
        """
        类执行入口
        """
        self.begin()
        self.query()
        self.finish()
        self.save_json()
        self.gen_result()
        self.save_db()


def run(domain):
    """
    类统一调用入口

    :param str domain: 域名
    """
    query = BufferOver(domain)
    query.run()


if __name__ == '__main__':
    run('example.com')
