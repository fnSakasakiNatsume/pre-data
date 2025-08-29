from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os

def crawl_and_save_html(domain, wait_time=15):
    """爬取网站并保存完整HTML内容"""
    print(f"正在自动安装ChromeDriver...")
    
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
        
        # 构建URL
        url = f"http://{domain}"
        print(f"正在访问: {url}")
        driver.get(url)
        
        # 等待页面加载
        print("等待页面加载...")
        time.sleep(wait_time)
        
        # 获取页面信息
        title = driver.title
        page_source = driver.page_source
        body_text = driver.find_element("tag name", "body").text
        
        # 检查是否还在loading
        loading_elements = driver.find_elements("id", "preload")
        is_loading = len(loading_elements) > 0
        
        # 保存HTML文件
        output_filename = f"{domain}_new.html"
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(page_source)
        
        result = {
            'url': url,
            'title': title,
            'is_loading': is_loading,
            'body_text_length': len(body_text),
            'page_source_length': len(page_source),
            'saved_file': output_filename,
            'body_text_preview': body_text[:500] if body_text else "无文本内容"
        }
        
        print(f"\nSelenium爬虫结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if not is_loading:
            print(f"\n✅ 成功获取完整内容并保存到 {output_filename}！")
        else:
            print(f"\n⚠️  页面仍在加载中，但已保存当前内容到 {output_filename}")
        
        # 关闭浏览器
        driver.quit()
        return result
        
    except Exception as e:
        print(f"爬取失败: {e}")
        return None

def batch_crawl_and_save(domains, output_dir="crawled_html"):
    """批量爬取并保存多个网站"""
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    results = []
    
    for i, domain in enumerate(domains):
        print(f"\n=== 进度: {i+1}/{len(domains)} ===")
        
        # 切换到输出目录
        original_dir = os.getcwd()
        os.chdir(output_dir)
        
        result = crawl_and_save_html(domain, wait_time=20)
        
        # 返回原目录
        os.chdir(original_dir)
        
        if result:
            results.append(result)
        
        # 避免请求过于频繁
        time.sleep(3)
    
    # 保存结果摘要
    summary_file = "crawl_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n批量爬取完成！结果摘要已保存到 {summary_file}")
    return results

if __name__ == "__main__":
    print("选择运行模式:")
    print("1. 爬取单个网站 (0x60df2k.cc)")
    print("2. 批量爬取前5个网站")
    
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        # 爬取单个网站
        crawl_and_save_html("0x60df2k.cc")
    elif choice == "2":
        # 批量爬取
        test_domains = ["0x60df2k.cc", "0x70df1k.cc", "0xcoins.xyz", "0xpendle.xyz", "1.ark40.com"]
        batch_crawl_and_save(test_domains)
    else:
        print("无效选择")
