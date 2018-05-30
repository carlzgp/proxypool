from .utils import get_page
from pyquery import PyQuery as pq
import re


class ProxyMetaclass(type):
    """
        元类，在FreeProxyGetter类中加入
        __CrawlFunc__和__CrawlFuncCount__
        两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def crawl_kuaidaili(self):
        for page in range(1, 4):
            # 国内高匿代理
            start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
            html = get_page(start_url)
            ip_adress = re.compile(
                '<td data-title="IP">(.*?)</td>.*?<td data-title="PORT">(.*?)</td>', re.S
            )
            re_ip_adress = re.findall(ip_adress, str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_xicidaili(self):
        for page in range(1, 4):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(page)
            html = get_page(start_url)
            ip_adress = re.compile('<td class="country"><img src=.*?alt="Cn" /></td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', re.S)
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_data5u(self):
        for i in ['gngn', 'gnpt']:
            start_url = 'http://www.data5u.com/free/{}/index.shtml'.format(i)
            html = get_page(start_url)
            ip_adress = re.compile(
                ' <ul class="l2">.*?<span><li>(.*?)</li></span>.*?<span style="width: 100px;"><li class=".*?">(.*?)</li></span>', re.S
            )
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_xroxy(self):
        for i in ['CN', 'TW']:
            start_url = 'http://www.xroxy.com/proxylist.php?port=&type=&ssl=&country={}'.format(
                i)
            for n in range(0, 5):
                url = start_url + '&latency=&reliability=&sort=reliability&desc=true&pnum={}#table'.format(n)
                html = get_page(url)
                if html:
                    ip_adress1 = re.compile(
                        "title='View this Proxy details'>(.*?)<!--")
                    re_ip_adress1 = ip_adress1.findall(str(html))
                    ip_adress2 = re.compile(
                        "title='Select proxies with port number .*?'>(.*?)</a>")
                    re_ip_adress2 = ip_adress2.findall(str(html))
                    for adress, port in zip(re_ip_adress1, re_ip_adress2):
                        adress_port = adress + ':' + port
                        yield adress_port.replace(' ', '')
                else:
                    return None

    def crawl_spys(self):
        start_url = 'http://spys.one/free-proxy-list/CN/'
        html = get_page(start_url)
        ip_address = re.compile('<font class=spy14>(.*?)<script type')
        re_ip_address = re.findall(ip_address, str(html))
        for address in re_ip_address:
            for port in [1080, 8080, 3128]:
                address_port = address + ':' + port
                yield address_port.replace(' ', '')

    '''
    def crawl_nova(self):
        start_url = 'https://www.proxynova.com/proxy-server-list/country-cn/'
        html = get_page(start_url)
        ip_address1 = re.compile('<td align="left" onclick="javascript:check_proxy(this)">.*?<abbr title="(.*?)"><script>.*?<td align="left">\s*(.*?)\s*</td>', re.S)
        ip_address2 = re.compile('<td align="left" onclick="javascript:check_proxy(this)">.*?<abbr title="(.*?)"><script>.*?title="Port.*?>(.*?)</a>', re.S)
        re_ip_address1 = ip_address1.findall(str(html))
        re_ip_address2 = ip_address2.findall(str(html))
        for adress, port in zip(re_ip_address1, re_ip_address2):
            adress_port = adress + ':' + port
            yield adress_port.replace(' ', '')
    '''