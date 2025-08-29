# Web Crawler for Scam Database

一个智能的网页爬虫工具，专门用于爬取和截图钓鱼网站，支持自动检测错误页面和保持真实比例截图。

## 功能特性

### 🎯 智能页面检测
- **自动跳过错误页面**：检测并跳过GoDaddy出售页面、域名停放页面、404错误页面等
- **页面加载超时处理**：设置30秒超时，避免长时间等待无效网站
- **智能等待机制**：等待页面完全加载，检测内容稳定性

### 📸 真实比例截图
- **保持原始比例**：根据页面实际尺寸设置窗口大小，避免图片变形
- **智能缩放**：大页面按比例缩放，小页面保持原始尺寸
- **多重备用方案**：确保截图成功率

### 📊 详细统计报告
- **成功/跳过/失败统计**：清晰区分不同类型的处理结果
- **截图成功率统计**：单独统计截图成功情况
- **JSON格式报告**：生成详细的爬取摘要

## 文件说明

### 核心文件
- `wait_for_load_crawler.py` - 主要的智能爬虫脚本
- `extract_domains.py` - 从HTML文件名提取域名列表
- `requirements.txt` - Python依赖包列表

### 测试文件
- `test_final_crawler.py` - 测试最终改进的爬虫
- `test_improved_crawler.py` - 测试改进的爬虫功能
- `advanced_crawler.py` - 高级爬虫功能
- `auto_selenium_test.py` - 自动Selenium测试

## 安装和使用

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行爬虫
```bash
python wait_for_load_crawler.py
```

### 3. 选择运行模式
- **模式1**：爬取单个网站测试
- **模式2**：批量爬取所有域名
- **模式3**：批量爬取前10个域名（测试）

## 配置说明

### 输入文件
- `domains_list.json` - 域名列表文件
- `accessible_domains.json` - 可访问域名列表

### 输出目录
- `C:/ml/results-combined-2/` - 默认输出目录
- 包含HTML文件和PNG截图
- 生成 `crawl_summary.json` 统计报告

## 技术特点

### 智能等待算法
```python
def wait_for_page_load(driver, max_wait_time=60):
    # 检测loading元素消失
    # 检查内容稳定性（连续3次稳定）
    # 检测丰富内容（>500字符且不含loading）
```

### 错误页面检测
```python
error_keywords = [
    'godaddy', 'domain', 'parked', 'for sale', 
    'buy this domain', 'domain name', 'purchase', 
    'not found', '404', 'error'
]
```

### 真实比例截图
```python
# 获取页面实际尺寸
page_width = driver.execute_script("return document.documentElement.scrollWidth")
page_height = driver.execute_script("return document.documentElement.scrollHeight")

# 按比例缩放
scale = min(max_width / page_width, max_height / page_height)
window_width = int(page_width * scale)
window_height = int(page_height * scale)
```

## 系统要求

- Python 3.7+
- Chrome浏览器
- Windows 10/11
- 网络连接

## 依赖包

- selenium==4.15.2
- requests==2.31.0
- webdriver-manager==4.0.1

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规。

## 更新日志

### v1.0.0
- 初始版本发布
- 支持智能页面检测
- 支持真实比例截图
- 支持批量处理

### v1.1.0
- 改进错误页面检测
- 优化截图比例算法
- 增强统计报告功能
