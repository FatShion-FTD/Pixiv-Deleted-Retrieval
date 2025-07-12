import requests
import datetime
import time

def check_pixiv_image_existence(base_url_template, start_time_str, end_time_str, image_id):
    """
    在指定时间范围内逐秒检查 Pixiv 图片资源是否存在。

    :param base_url_template: 包含日期和 {time} 占位符的 URL 模板。
                              例如: "https://i.pximg.net/img-original/img/2025/06/08/{time}/"
    :param start_time_str: 开始时间，格式为 "HH:MM:SS" 或 "HH/MM/SS"。
    :param end_time_str: 结束时间，格式为 "HH:MM:SS" 或 "HH/MM/SS"。
    :param image_id: 图片的文件名，例如: "123456789_p0.png"。
    """
    
    # 标准化时间字符串格式，替换 "/" 为 ":"
    start_time_str = start_time_str.replace('/', ':')
    end_time_str = end_time_str.replace('/', ':')

    # 将时间字符串解析为 datetime 对象
    try:
        start_time = datetime.datetime.strptime(start_time_str, '%H:%M:%S')
        end_time = datetime.datetime.strptime(end_time_str, '%H:%M:%S')
    except ValueError:
        print("错误: 时间格式不正确。请使用 HH/MM/SS 或 HH:MM:SS 格式。")
        return

    # 伪装请求头，这是绕过 403 错误的关键
    headers = {
        'Referer': 'https://www.pixiv.net/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    found_timestamps = []
    current_time = start_time

    print(f"开始扫描...\n从: {start_time.strftime('%H:%M:%S')}\n到:   {end_time.strftime('%H:%M:%S')}\n")

    while current_time <= end_time:
        # 将当前时间格式化为 URL 所需的 HH/MM/SS 格式
        time_for_url = current_time.strftime('%H/%M/%S')
        
        # 构建完整的 URL
        full_url = base_url_template.format(time=time_for_url) + image_id
        
        try:
            # 发送 GET 请求
            response = requests.get(full_url, headers=headers, timeout=10) # 设置10秒超时
            
            # 检查 HTTP 状态码
            if response.status_code == 200:
                timestamp_str = current_time.strftime('%H:%M:%S')
                print(f"✅ 资源存在! 时间: {timestamp_str} -> {full_url}")
                found_timestamps.append(timestamp_str)
            else:
                # 使用 print 的 end='\r' 来实现单行刷新，避免刷屏
                print(f"❌ 未找到... 时间: {current_time.strftime('%H:%M:%S')} (状态码: {response.status_code})", end='\r')

        except requests.exceptions.RequestException as e:
            # 处理网络连接等异常
            print(f" E 发生错误: {current_time.strftime('%H:%M:%S')} - {e}", end='\r')

        # 时间增加一秒
        current_time += datetime.timedelta(seconds=1)
        
        # 可以取消注释下一行来降低请求频率，避免对服务器造成过大压力
        # time.sleep(0.1) 

    print("\n\n扫描完成。")

    if found_timestamps:
        print("\n--- 存在的资源时间戳汇总 ---")
        for ts in found_timestamps:
            print(ts)
    else:
        print("\n在指定时间范围内没有找到任何存在的资源。")


if __name__ == '__main__':
    # --- 请在这里配置您的参数 ---

    # 1. URL 模板 (从您给的 URL 中提取)
    # 将时间部分替换为 {time}
    BASE_URL_TEMPLATE = "https://i.pximg.net/img-original/img/YYYY/MM/DD/"
    BASE_URL_TEMPLATE += "{time}/"
    # 2. 图片文件名 (从您给的 URL 中提取)
    ARTWORK_ID = 123456789
    IMAGE_ID = f"{ARTWORK_ID}_p0.png"

    # 3. 开始和结束时间
    START_TIME = "HH/MM/SS"
    END_TIME = "HH/MM/SS"

    # --- 执行检查 ---
    check_pixiv_image_existence(BASE_URL_TEMPLATE, START_TIME, END_TIME, IMAGE_ID)