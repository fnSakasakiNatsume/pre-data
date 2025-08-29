import os
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import urllib.parse

class AdvancedCrawler:
    def __init__(self, headless=True):
        """初始化爬虫"""
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        self.driver = None
        self.results = {}
        
    def start_driver(self):
        """启动浏览器驱动"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            return True
        except Exception as e:
            print(f"启动浏览器失败: {e}")
            return False
    
    def crawl_website(self, url, wait_time=10):
        """爬取单个网站"""
        if not self.driver:
            if not self.start_driver():
                return None
        
        try:
            print(f"正在爬取: {url}")
            self.driver.get(url)
            
            # 等待页面加载
            time.sleep(3)
            
            # 等待页面内容加载完成
            try:
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except TimeoutException:
                print(f"页面加载超时: {url}")
            
            # 获取页面标题
            title = self.driver.title
            
            # 获取页面内容
            page_source = self.driver.page_source
            
            # 获取页面文本内容
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # 检查是否还在loading
            loading_elements = self.driver.find_elements(By.ID, "preload")
            is_loading = len(loading_elements) > 0
            
            result = {
                'url': url,
                'title': title,
                'is_loading': is_loading,
                'body_text_length': len(body_text),
                'page_source_length': len(page_source),
                'body_text_preview': body_text[:500] if body_text else "无文本内容"
            }
            
            print(f"✓ 爬取完成: {title} (文本长度: {len(body_text)})")
            return result
            
        except Exception as e:
            print(f"爬取失败 {url}: {e}")
            return None
    
    def crawl_multiple_sites(self, urls, output_file='crawled_results.json'):
        """批量爬取多个网站"""
        results = []
        
        for i, url in enumerate(urls):
            print(f"\n进度: {i+1}/{len(urls)}")
            result = self.crawl_website(url)
            if result:
                results.append(result)
            
            # 避免请求过于频繁
            time.sleep(2)
        
        # 保存结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n爬取完成！结果已保存到 {output_file}")
        return results
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()

def test_single_site():
    """测试单个网站爬取"""
    crawler = AdvancedCrawler(headless=False)  # 设置为False可以看到浏览器操作
    
    # 测试你提到的网站
    test_url = "http://0x60df2k.cc"
    result = crawler.crawl_website(test_url, wait_time=15)
    
    if result:
        print("\n爬取结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    crawler.close()

def batch_crawl_from_domains():
    """从domains_list.json批量爬取"""
    # 读取域名列表
    with open('domains_list.json', 'r', encoding='utf-8') as f:
        domains = json.load(f)
    
    # 转换为URL列表（只测试前5个）
    test_domains = domains[:5]
    urls = [f"http://{domain}" for domain in test_domains]
    
    crawler = AdvancedCrawler(headless=True)
    results = crawler.crawl_multiple_sites(urls, 'test_crawl_results.json')
    crawler.close()
    
    return results

if __name__ == "__main__":
    print("选择运行模式:")
    print("1. 测试单个网站")
    print("2. 批量测试前5个网站")
    
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        test_single_site()
    elif choice == "2":
        batch_crawl_from_domains()
    else:
        print("无效选择")
