from wait_for_load_crawler import batch_crawl_from_domains

def test_improved_crawler():
    """测试改进后的爬虫"""
    print("=== 测试改进后的爬虫 ===")
    
    # 测试域名列表
    test_domains = [
        "0x60df2k.cc",  # 已知需要JavaScript渲染的网站
        "0x70df1k.cc",  # 另一个测试网站
        "0xcoins.xyz"   # 第三个测试网站
    ]
    
    print(f"测试域名: {test_domains}")
    print("改进内容:")
    print("1. 等待时间从30秒增加到60秒")
    print("2. 更智能的内容稳定性检测")
    print("3. 多种截图方法备选")
    print("4. 额外等待确保内容渲染")
    
    # 运行测试
    result = batch_crawl_from_domains(
        domains=test_domains,
        output_dir="C:/ml/test-results",
        max_wait_time=60
    )
    
    if result:
        print("\n=== 测试结果 ===")
        print(f"总计测试: {result['total_domains']} 个网站")
        print(f"HTML成功: {result['success_count']} 个")
        print(f"截图成功: {result['screenshot_success_count']} 个")
        print(f"HTML成功率: {result['success_rate']}%")
        print(f"截图成功率: {result['screenshot_success_rate']}%")
        
        # 显示详细结果
        print("\n=== 详细结果 ===")
        for i, site_result in enumerate(result['results']):
            if site_result:
                print(f"{i+1}. {site_result['url']}")
                print(f"   标题: {site_result['title']}")
                print(f"   文本长度: {site_result['body_text_length']}")
                print(f"   完全加载: {site_result['is_fully_loaded']}")
                print(f"   截图成功: {site_result['screenshot_saved']}")
                print()

if __name__ == "__main__":
    test_improved_crawler()
