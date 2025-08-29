import os
import json
import glob

def extract_domains_from_html_files():
    # 获取result文件夹下所有html文件
    result_dir = r'C:\ml\result'
    html_files = glob.glob(os.path.join(result_dir, '*.html'))
    
    # 提取域名（去掉.html扩展名）
    domains = []
    for html_file in html_files:
        # 获取文件名（不包含路径）
        filename = os.path.basename(html_file)
        # 去掉.html扩展名
        domain = filename.replace('.html', '')
        domains.append(domain)
    
    # 按字母顺序排序
    domains.sort()
    
    # 保存为JSON文件，格式与domains.json相同
    output_file = 'domains_list.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(domains, f, indent=2, ensure_ascii=False)
    
    print(f"成功提取了 {len(domains)} 个域名")
    print(f"结果已保存到 {output_file}")
    
    # 显示前10个域名作为示例
    print("\n前10个域名示例:")
    for i, domain in enumerate(domains[:10]):
        print(f"{i+1}. {domain}")

if __name__ == "__main__":
    extract_domains_from_html_files()
