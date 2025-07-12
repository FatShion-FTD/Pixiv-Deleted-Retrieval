import requests
import os
import re
import time

def download_pixiv_gallery(start_url, download_dir):
    """
    根据给定的一个 Pixiv 图片 URL，下载整个作品集（p0, p1, ...）。

    :param start_url: 作品集中任何一张图片的 URL。
                      例如: "https://i.pximg.net/img-original/img/YYYY/MM/DD/HH/MM/SS/{ARTWORK_ID}_p0.png"
    :param download_dir: 图片要保存到的本地文件夹路径。
    """
    
    # 1. 使用正则表达式解析 URL，提取关键部分
    # 模式: (基础路径)(作品ID)_p(页码)(.扩展名)
    pattern = re.compile(r'(https?://.*/)(\d+)_p\d+(\..+)')
    match = pattern.match(start_url)
    
    if not match:
        print(f"错误：无法解析给定的 URL 格式。\n请确保 URL 类似于: '.../12345678_p0.png'")
        return

    base_url, illust_id, extension = match.groups()
    print(f"解析成功:\n  - 作品ID: {illust_id}\n  - 文件格式: {extension}\n  - 基础路径: {base_url}")
    
    # 2. 准备请求头和下载目录
    headers = {
        'Referer': 'https://www.pixiv.net/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    
    # 创建下载目录（如果不存在）
    # exist_ok=True 可以在目录已存在时不引发错误
    os.makedirs(download_dir, exist_ok=True)
    print(f"文件将被下载到: {os.path.abspath(download_dir)}\n")

    # 3. 循环遍历并下载
    page_num = 0
    while True:
        # 构建当前页码的文件名和完整 URL
        filename = f"{illust_id}_p{page_num}{extension}"
        current_url = f"{base_url}{filename}"
        
        print(f"正在尝试下载: {filename} ... ", end="")
        
        try:
            # 使用 stream=True 进行流式请求，适合下载文件
            response = requests.get(current_url, headers=headers, stream=True, timeout=20)
            
            # 检查响应状态
            if response.status_code == 200:
                # 构建本地保存的完整路径
                local_filepath = os.path.join(download_dir, filename)
                
                # 以二进制写模式打开文件，并写入内容
                with open(local_filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"✅ 下载成功")
                
            elif response.status_code == 404:
                print("❌ 未找到 (404 Not Found)。系列下载完成。")
                break # 找不到文件，说明系列结束，退出循环
            else:
                print(f"❌ 失败 (HTTP 状态码: {response.status_code})")
                break # 遇到其他错误也停止

        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
            break # 遇到网络问题停止

        # 准备下载下一张
        page_num += 1
        # 礼貌性地等待一下，避免过快请求
        time.sleep(0.5)

    print("\n所有任务已结束。")


if __name__ == '__main__':
    # --- 请在这里配置您的参数 ---

    # 1. 给出系列中任何一张图片的 URL
    TARGET_URL = "https://i.pximg.net/img-original/img/YYYY/MM/DD/HH/MM/SS/{ARTWORK_ID}_p0.png"
    
    # 2. 指定下载到的本地文件夹路径
    # 在 Windows 上，路径中的反斜杠 `\` 最好写成 `\\` 或者使用 `/`
    DOWNLOAD_PATH = r"C:\Downloads"

    # --- 执行下载 ---
    download_pixiv_gallery(TARGET_URL, DOWNLOAD_PATH)