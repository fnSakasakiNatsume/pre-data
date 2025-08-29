from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def test_selenium_crawler():
    """测试Selenium爬虫（自动安装ChromeDriver）"""
    print("正在自动安装ChromeDriver...")
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    try:
        # 自动安装并启动ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 访问网站
        url = "http://0x60df2k.cc"
        print(f"正在访问: {url}")
        driver.get(url)
        
        # 等待页面加载
        print("等待页面加载...")
        time.sleep(10)  # 增加等待时间
        
        # 获取页面信息
        title = driver.title
        page_source = driver.page_source
        body_text = driver.find_element("tag name", "body").text
        
        # 检查是否还在loading
        loading_elements = driver.find_elements("id", "preload")
        is_loading = len(loading_elements) > 0
        
        result = {
            'url': url,
            'title': title,
            'is_loading': is_loading,
            'body_text_length': len(body_text),
            'page_source_length': len(page_source),
            'body_text_preview': body_text[:500] if body_text else "无文本内容"
        }
        
        print("\nSelenium爬虫结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if not is_loading:
            print("\n✅ 成功获取完整内容！")
        else:
            print("\n⚠️  页面仍在加载中，可能需要更长的等待时间。")
        
        # 关闭浏览器
        driver.quit()
        return result
        
    except Exception as e:
        print(f"爬取失败: {e}")
        return None

if __name__ == "__main__":
    test_selenium_crawler()
