from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import os

def wait_for_page_load(driver, max_wait_time=60):
    """等待页面完全加载（改进版）"""
    print("等待页面完全加载...")
    
    start_time = time.time()
    last_text_length = 0
    stable_count = 0
    
    while time.time() - start_time < max_wait_time:
        try:
            # 检查是否还有loading元素
            loading_elements = driver.find_elements(By.ID, "preload")
            
            if len(loading_elements) == 0:
                print("✅ Loading元素已消失，页面加载完成！")
                return True
            
            # 获取当前页面文本
            body_text = driver.find_element(By.TAG_NAME, "body").text
            current_text_length = len(body_text)
            
            # 检查内容是否稳定
            if current_text_length == last_text_length and current_text_length > 100:
                stable_count += 1
                if stable_count >= 3:  # 连续3次内容稳定
                    print(f"✅ 页面内容已稳定 {stable_count} 次，加载完成！")
                    return True
            else:
                stable_count = 0
            
            last_text_length = current_text_length
            
            # 检查是否有实际内容（不仅仅是loading文本）
            if current_text_length > 500 and "loading" not in body_text.lower():
                print(f"✅ 检测到丰富内容 ({current_text_length} 字符)，加载完成！")
                return True
            
            print(f"⏳ 仍在加载中... (已等待 {int(time.time() - start_time)}秒, 文本长度: {current_text_length})")
            time.sleep(5)  # 增加等待间隔
            
        except Exception as e:
            print(f"等待过程中出现错误: {e}")
            time.sleep(3)
    
    print(f"⚠️ 等待超时 ({max_wait_time}秒)，保存当前内容")
    return False

def crawl_and_save_html(driver, domain, output_dir, max_wait_time=60):
    """爬取单个网站并等待完全加载后保存HTML内容和截图（改进版）"""
    try:
        # 构建URL
        url = f"http://{domain}"
        print(f"正在访问: {url}")
        
        # 设置页面加载超时
        driver.set_page_load_timeout(30)
        
        try:
            driver.get(url)
        except Exception as load_error:
            print(f"❌ 页面加载失败: {load_error}")
            return None
        
        # 检查是否是错误页面（GoDaddy出售页面等）
        title = driver.title.lower()
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        
        # 检测错误页面关键词
        error_keywords = [
            'godaddy', 'domain', 'parked', 'for sale', 'buy this domain',
            'domain name', 'purchase', 'not found', '404', 'error',
        ]
        
        is_error_page = any(keyword in title or keyword in body_text for keyword in error_keywords)
        
        if is_error_page:
            print(f"⚠️ 检测到错误页面 (标题: {driver.title})，跳过处理")
            return None
        
        # 等待页面完全加载
        is_fully_loaded = wait_for_page_load(driver, max_wait_time)
        
        # 额外等待确保内容完全渲染
        if is_fully_loaded:
            print("额外等待5秒确保内容完全渲染...")
            time.sleep(5)
        
        # 获取页面信息
        title = driver.title
        page_source = driver.page_source
        body_text = driver.find_element(By.TAG_NAME, "body").text
        
        # 检查是否还在loading
        loading_elements = driver.find_elements(By.ID, "preload")
        is_loading = len(loading_elements) > 0
        
        # 保存HTML文件到指定目录
        html_filename = os.path.join(output_dir, f"{domain}.html")
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(page_source)
        
        # 保存截图到指定目录（改进版 - 保持真实比例）
        screenshot_filename = os.path.join(output_dir, f"{domain}.png")
        screenshot_saved = False
        
        try:
            print("准备截图...")
            
            # 获取页面实际尺寸
            try:
                # 获取页面实际宽度和高度
                page_width = driver.execute_script("return document.documentElement.scrollWidth")
                page_height = driver.execute_script("return document.documentElement.scrollHeight")
                
                print(f"页面实际尺寸: {page_width}x{page_height}px")
                
                # 计算合适的窗口大小，保持真实比例
                max_width = 1920
                max_height = 1080
                
                # 如果页面尺寸过大，按比例缩放
                if page_width > max_width or page_height > max_height:
                    scale = min(max_width / page_width, max_height / page_height)
                    window_width = int(page_width * scale)
                    window_height = int(page_height * scale)
                else:
                    window_width = page_width
                    window_height = page_height
                
                # 确保最小尺寸
                window_width = max(window_width, 1200)
                window_height = max(window_height, 800)
                
                print(f"设置窗口大小: {window_width}x{window_height}px")
                
                # 设置窗口大小
                driver.set_window_size(window_width, window_height)
                time.sleep(2)
                
                # 截图
                driver.save_screenshot(screenshot_filename)
                print(f"📸 截图已保存 (真实比例): {screenshot_filename}")
                screenshot_saved = True
                
            except Exception as e1:
                print(f"方法1失败: {e1}")
                
                # 备用方法：使用固定比例
                try:
                    # 使用16:9比例
                    driver.set_window_size(1920, 1080)
                    time.sleep(2)
                    driver.save_screenshot(screenshot_filename)
                    print(f"📸 截图已保存 (16:9比例): {screenshot_filename}")
                    screenshot_saved = True
                    
                except Exception as e2:
                    print(f"方法2也失败: {e2}")
                    
                    # 方法3：滚动截图
                    try:
                        driver.set_window_size(1920, 1080)
                        time.sleep(2)
                        
                        # 滚动到页面底部确保内容加载
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        driver.execute_script("window.scrollTo(0, 0);")
                        time.sleep(1)
                        
                        driver.save_screenshot(screenshot_filename)
                        print(f"📸 截图已保存 (滚动后): {screenshot_filename}")
                        screenshot_saved = True
                        
                    except Exception as e3:
                        print(f"所有截图方法都失败: {e3}")
                        screenshot_saved = False
                        screenshot_filename = None
                        
        except Exception as screenshot_error:
            print(f"⚠️ 截图失败: {screenshot_error}")
            screenshot_saved = False
            screenshot_filename = None
        
        result = {
            'url': url,
            'title': title,
            'is_loading': is_loading,
            'is_fully_loaded': is_fully_loaded,
            'body_text_length': len(body_text),
            'page_source_length': len(page_source),
            'html_file': html_filename,
            'screenshot_file': screenshot_filename,
            'screenshot_saved': screenshot_saved,
            'body_text_preview': body_text[:200] if body_text else "无文本内容"
        }
        
        print(f"✓ 爬取完成: {title} (文本长度: {len(body_text)})")
        
        if is_fully_loaded and not is_loading:
            print(f"✅ 页面完全加载完成并保存到 {html_filename}")
        elif is_fully_loaded:
            print(f"✅ 页面内容已稳定，保存到 {html_filename}")
        else:
            print(f"⚠️ 页面可能未完全加载，但已保存到 {html_filename}")
        
        return result
        
    except Exception as e:
        print(f"爬取失败 {domain}: {e}")
        return None

def batch_crawl_from_domains(domains, output_dir="C:/ml/results-combined-2", max_wait_time=60):
    """批量爬取网站列表"""
    print(f"开始批量爬取 {len(domains)} 个网站...")
    print(f"输出目录: {output_dir}")
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ 创建输出目录: {output_dir}")
    
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
        print("正在自动安装ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        results = []
        success_count = 0
        skipped_count = 0
        
        for i, domain in enumerate(domains):
            print(f"\n=== 进度: {i+1}/{len(domains)} ===")
            print(f"正在处理: {domain}")
            
            result = crawl_and_save_html(driver, domain, output_dir, max_wait_time)
            
            if result:
                results.append(result)
                success_count += 1
            else:
                skipped_count += 1
                print(f"⏭️ 跳过 {domain}")
            
            # 避免请求过于频繁
            if i < len(domains) - 1:  # 不是最后一个
                print("等待3秒后继续下一个...")
                time.sleep(3)
        
        # 关闭浏览器
        driver.quit()
        
        # 统计截图成功数量
        screenshot_success_count = sum(1 for result in results if result and result.get('screenshot_saved', False))
        
        # 保存爬取结果摘要
        summary_file = os.path.join(output_dir, "crawl_summary.json")
        summary = {
            'total_domains': len(domains),
            'success_count': success_count,
            'skipped_count': skipped_count,
            'failed_count': len(domains) - success_count - skipped_count,
            'success_rate': round(success_count / len(domains) * 100, 2),
            'screenshot_success_count': screenshot_success_count,
            'screenshot_success_rate': round(screenshot_success_count / len(domains) * 100, 2),
            'results': results
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 批量爬取完成！")
        print(f"总计: {len(domains)} 个网站")
        print(f"成功: {success_count} 个")
        print(f"跳过: {skipped_count} 个 (错误页面/无法访问)")
        print(f"失败: {len(domains) - success_count - skipped_count} 个")
        print(f"截图成功: {screenshot_success_count} 个")
        print(f"成功率: {summary['success_rate']}%")
        print(f"截图成功率: {summary['screenshot_success_rate']}%")
        print(f"结果摘要已保存到: {summary_file}")
        
        return summary
        
    except Exception as e:
        print(f"批量爬取失败: {e}")
        return None

def load_domains_from_file(filename="accessible_domains.json"):
    """从文件加载域名列表"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            domains = json.load(f)
        print(f"✅ 从 {filename} 加载了 {len(domains)} 个域名")
        return domains
    except Exception as e:
        print(f"❌ 加载域名文件失败: {e}")
        return []

if __name__ == "__main__":
    print("=== 智能等待加载爬虫 ===")
    print("选择运行模式:")
    print("1. 爬取单个网站测试")
    print("2. 批量爬取所有域名")
    print("3. 批量爬取前10个域名（测试）")
    
    choice = input("请输入选择 (1, 2 或 3): ").strip()
    
    if choice == "1":
        # 爬取单个网站测试
        test_domains = ["0x60df2k.cc"]
        batch_crawl_from_domains(test_domains, max_wait_time=45)
        
    elif choice == "2":
        # 批量爬取所有域名
        domains = load_domains_from_file()
        if domains:
            batch_crawl_from_domains(domains, max_wait_time=30)
        else:
            print("无法加载域名列表，请检查 domains_list.json 文件")
            
    elif choice == "3":
        # 批量爬取前10个域名（测试）
        domains = load_domains_from_file()
        if domains:
            test_domains = domains[:10]
            print(f"测试模式：只爬取前 {len(test_domains)} 个域名")
            batch_crawl_from_domains(test_domains, max_wait_time=30)
        else:
            print("无法加载域名列表，请检查 domains_list.json 文件")
            
    else:
        print("无效选择")
