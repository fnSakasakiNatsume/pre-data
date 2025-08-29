from wait_for_load_crawler import batch_crawl_from_domains

def test_fixed_crawler():
    """测试修复后的爬虫"""
    print("=== 测试修复后的爬虫 ===")
    
    # 测试域名列表
    test_domains = [
        "0x60df2k.cc",      # 正常网站
        "0x70df1k.cc",      # 正常网站
        "0xcoins.xyz"       # 正常网站
    ]
    
    print(f"测试域名: {test_domains}")
    print("修复内容:")
    print("1. 改进页面加载检测 - 检查多种loading元素")
    print("2. 检查页面状态 (document.readyState)")
    print("3. 检查loading文本内容")
    print("4. 只在页面完全加载后截图")
    print("5. 截图前再次验证页面状态")
    
    # 运行测试
    result = batch_crawl_from_domains(
        domains=test_domains,
        output_dir="C:/ml/test-fixed-results",
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
    test_fixed_crawler()
