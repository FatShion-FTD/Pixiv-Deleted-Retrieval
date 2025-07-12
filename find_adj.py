import requests
import re
from typing import Tuple, Optional


def build_pixiv_artwork_url(artwork_id: int) -> str:
    """Build complete Pixiv artwork URL from artwork ID."""
    return f"https://www.pixiv.net/en/artworks/{artwork_id}"


def is_valid_artwork_page(html_content: str) -> bool:
    """Check if the page contains valid artwork content (no 'Page not found')."""
    return '<h1>Page not found</h1>' not in html_content


def get_artwork_page_content(artwork_id: int) -> Optional[str]:
    """Get HTML content of Pixiv artwork page. Returns None if 404 or other error."""
    url = build_pixiv_artwork_url(artwork_id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    
    # 确保正确解码内容
    if response.encoding is None:
        response.encoding = 'utf-8'
    
    return response.text


def find_adjacent_valid_artworks(center_id: int) -> Tuple[int, int]:
    """Find previous and next valid artwork IDs around the center ID."""
    print(f"寻找作品 {center_id} 的前后相邻作品...")
    
    # Find previous valid artwork
    prev_id = center_id - 1
    while prev_id > 0:
        print(f"检查前一个作品: {prev_id}")
        content = get_artwork_page_content(prev_id)
        if content is None:
            print(f"❌ 作品 {prev_id} 不存在 (404)")
            prev_id -= 1
            continue
        if is_valid_artwork_page(content):
            print(f"✅ 找到前一个有效作品: {prev_id}")
            break
        prev_id -= 1
    
    # Find next valid artwork
    next_id = center_id + 1
    while next_id < 999999999:  # reasonable upper limit
        print(f"检查后一个作品: {next_id}")
        content = get_artwork_page_content(next_id)
        if content is None:
            print(f"❌ 作品 {next_id} 不存在 (404)")
            next_id += 1
            continue
        if is_valid_artwork_page(content):
            print(f"✅ 找到后一个有效作品: {next_id}")
            break
        next_id += 1
    
    return prev_id, next_id


if __name__ == '__main__':
    # --- 请在这里配置您的参数 ---
    
    # 给定的 Pixiv 作品 ID
    ARTWORK_ID = 123456789
    
    # --- 执行查找 ---
    prev_id, next_id = find_adjacent_valid_artworks(ARTWORK_ID)
    
    print(f"\n=== 结果汇总 ===")
    print(f"中心作品 ID: {ARTWORK_ID}")
    print(f"前一个作品 ID: {prev_id}")
    print(f"前一个作品 URL: {build_pixiv_artwork_url(prev_id)}")
    print(f"后一个作品 ID: {next_id}")
    print(f"后一个作品 URL: {build_pixiv_artwork_url(next_id)}") 