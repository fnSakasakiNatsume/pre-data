from wait_for_load_crawler import batch_crawl_from_domains

def test_final_crawler():
    """测试最终改进的爬虫"""
    print("=== 测试最终改进的爬虫 ===")
    
    # 测试域名列表（包含一些可能无法访问的域名）
    test_domains = [
        "0x60df2k.cc",      # 正常网站
        "0x70df1k.cc",      # 正常网站
        "invalid-domain-12345.com",  # 无效域名
        "example.com",      # 可能被GoDaddy出售的域名
        "0xcoins.xyz"       # 正常网站
    ]
    
    print(f"测试域名: {test_domains}")
    print("最终改进内容:")
    print("1. 自动检测并跳过错误页面 (GoDaddy出售页面等)")
    print("2. 保持截图真实比例，避免过长图片")
    print("3. 页面加载超时处理")
    print("4. 更详细的统计信息")
    
    # 运行测试
    result = batch_crawl_from_domains(
        domains=test_domains,
        output_dir="C:/ml/test-final-results",
        max_wait_time=60
    )
    
    if result:
        print("\n=== 测试结果 ===")
        print(f"总计测试: {result['total_domains']} 个网站")
        print(f"成功: {result['success_count']} 个")
        print(f"跳过: {result['skipped_count']} 个")
        print(f"失败: {result['failed_count']} 个")
        print(f"截图成功: {result['screenshot_success_count']} 个")
        print(f"成功率: {result['success_rate']}%")
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
    test_final_crawler()
