# coding:utf-8
from requests import Session
from requests.exceptions import ConnectionError
from sys import path as sys_path
from os import write as os_write, close as os_close, \
    path, chdir, makedirs, O_CREAT, O_RDWR, open as os_open, \
    remove as os_remove, listdir
from os.path import join as path_join, basename, isdir, isfile
from re import compile, M, I
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from asyncio import get_event_loop, ensure_future, gather, Semaphore
from fake_useragent import UserAgent
from multiprocessing import cpu_count, Pool, freeze_support
from random import random
from collections import deque
from tkinter import Tk, Label, Button, StringVar, \
    Entry, END, RIGHT, LEFT, filedialog, TclError
from tkinter.messagebox import showwarning, showinfo, showerror
from PIL import Image, ImageTk
from win32 import win32clipboard as wcb
from win32.lib import win32con
import frozen

VERSION = '2.0'

PROXIES = {"http": "http://127.0.0.1:25378", "https": "http://127.0.0.1:25378"}  # vpn代理地址
HEADERS = {
    "Upgrade-Insecure-Requests": "1",
    "Proxy-Connection": "close",
    "Cache-Control": "max-age=0",
    "User-Agent": UserAgent().random,
}
ERR_TXT = "1.txt"
DEFAULT_DIR_ADDRESS = "C:\\Users\default-dir-177.ini"
BG_ADDRESS = 'Beautiful-Chinese-girl-retro-style-fantasy.PNG'
THEME_ICON = '11.ico'
IMG_LOC = "#main .single-content > p > img"
TITLE_LOC = "#main .entry-title"
PAGINATION_LOC = "#main .page-links > a"
MAX_RETRY = 10

class Crawler177:
    auth_dirname = compile(r'[\<\>\?\:\*\\\/"\|]', M)
    extract_num = compile(r'\[(\d+)p\]$', M | I)

    def __init__(self, url, dir, dda):
        self.url = url
        if not dir:
            with open(path_join(sys_path[0], dda), 'r') as dir_name:  # path.dirname(__file__)
                self.dir = dir_name.readline()
                dir_name.close()
        else:
            self.dir = dir
        self.html = self.bs_soup(self.url, 1)
        if self.html:
            chdir(self.dir)
            self.create_dir()

    def bs_soup(self, url, retries):
        with Session() as S:
            try:
                response = S.get(url=url, headers=dict(HEADERS, **{"Referer": self.url}), proxies=PROXIES, timeout=60)
            except ConnectionError:
                if retries > MAX_RETRY:
                    showerror(title="网络错误", message="呃~无法连接上主网站,请设置vpn, o(≧口≦)o")
                    S.close()
                    return
                self.bs_soup(self, url, retries + 1)
            else:
                response.encoding = 'utf-8'
                return BeautifulSoup(response.text, features='html.parser')

    @staticmethod
    def bs_soup_others(url):
        with Session() as S:
            try:
                response = S.get(url=url, headers=dict(HEADERS, **{"Referer": url}), proxies=PROXIES, timeout=30)
                response.encoding = 'utf-8'
            except ConnectionError:
                return []
            else:
                return list(map(lambda img: img.get('data-lazy-src'),
                                BeautifulSoup(response.text, features='html.parser').select(IMG_LOC)))

    @staticmethod
    def download_pics(target):
        with Session() as S:
            try:
                res = S.get(url=target, headers=dict(HEADERS, **{"Host": "img.177pic.info"}), proxies=PROXIES,
                            timeout=150)
            except Exception as e:
                print(e)
                with open(ERR_TXT, "a+") as img_url:
                    img_url.write(target + "\n")
                    img_url.close()
            else:
                res.encoding = 'utf-8'
                with open(basename(target), 'wb') as fw:
                    fw.write(res.content)
                    fw.close()

    @property
    def acquire_img_1(self):
        return self.get_img_source(self.html.select(IMG_LOC))

    @property
    def acquire_pagination(self):
        return list(map(
            lambda anchor: anchor.get('href'),
            self.html.select(PAGINATION_LOC)[1:-1]
        ))

    @property
    def acquire_title(self):
        return self.html.select(TITLE_LOC)[0].get_text()

    @property
    def get_picture_nums(self):
        num_extract = compile(r'\[(\d+)p?\]', M | I)  # 提取标题中的数字
        return int(num_extract.search(self.acquire_title).group(1))

    @property
    def private_imgs(self):
        return len(list(filter(lambda x: not bool(compile(r'\.txt$').search(x)), listdir())))

    @property
    def get_url_list(self):
        get_src_pool = Pool(processes=int(cpu_count()))
        src_list = []
        for url in self.acquire_pagination:
            src_list.append(get_src_pool.apply_async(func=self.bs_soup_others, args=(url,)))
        get_src_pool.close()
        get_src_pool.join()
        return self.acquire_img_1 + sum([src.get() for src in src_list], [])
        # return self.acquire_img_1 + sum([Crawler177.bs_soup_others(p) for p in self.acquire_pagination], [])

    @staticmethod
    def get_img_source(img_list):
        return list(map(lambda img: img.get('data-lazy-src'), img_list))  # 该网站现在采用图片懒加载

    def acquire_img(self, u):
        try:
            result = self.bs_soup(u, 1).select(IMG_LOC)
        except TypeError:
            pass
        else:
            return self.get_img_source(result)

    @staticmethod
    async def download_pics_add(target, restriction):
        async with restriction:
            async with ClientSession() as session:  # 官网推荐建立 Session 的形式
                try:
                    async with session.get(url=target, headers=dict(HEADERS, **{"Host": "img.177pic.info"}),
                                           proxy=PROXIES['http'], timeout=150) as r:
                        response = await r.read()
                except Exception:
                    pass
                else:
                    with open(target[target.rfind('/') + 1:-1], 'wb') as fw:
                        fw.write(response)
                        fw.close()
                    with open(ERR_TXT, mode="r") as urls:
                        content = urls.read()
                        urls.close()
                    with open(ERR_TXT, mode="w+") as urls:
                        urls.write(content.replace(target, ''))
                        urls.close()
                await session.close()

    def create_dir(self):
        t = self.acquire_title
        if self.auth_dirname.search(t):
            t = self.auth_dirname.sub('', t)
        if not isdir(t):
            makedirs(t)
        a = "%s/%s" % (self.dir, t)
        chdir(a)
        with open("%s/%s" % (a, ERR_TXT), "w") as tip:
            tip.write("{} 下载失败的图片：\n".format(self.url))
            tip.close()
        self.collection_process()

    def collection_process(self):
        download_pool = Pool(processes=int(cpu_count() * 1.5))
        for url in self.get_url_list:
            download_pool.apply_async(func=self.download_pics, args=(url,))
        download_pool.close()
        download_pool.join()
        self.replenish()

    def replenish(self):
        loop = get_event_loop()
        with open(ERR_TXT, "r+") as remain_img:
            tasks = [
                ensure_future(
                    self.download_pics_add(u, Semaphore(100))
                ) for u in remain_img.readlines()[1:]
            ]
            loop.run_until_complete(gather(*tasks))
            remain_img.close()
        loop.close()
        showinfo(
            title="完成", message=" φ(≧ω≦*)♪\n\r\n%s张图片下载成功，%s张下载失败！" % (
                self.private_imgs, self.get_picture_nums - self.private_imgs
            )
        )


class InputGUI(Tk):
    site_detect = compile(
        r'^https?:\/\/www\.177pic([az]?)\1(001)?\.((info)|(net)|(com)|(org))\/html\/20\d{2}\/\d{2}\/\d{4,8}\.html(\/\d{1,2}\/?)?$',
        M
    )

    def __init__(self, title, resolution='320x240'):
        super().__init__()
        self.address = None
        self.dir_name = None
        self.title(title)
        self.geometry(resolution)
        self.widget_arrange()
        try:
            set_bgi = ImageTk.PhotoImage(Image.open(fp=BG_ADDRESS))
            self.bgi = Label(self, text='', image=set_bgi)
        except FileNotFoundError:
            self.bgi = Label(self)
        self.bgi.pack(side=RIGHT)
        try:
            self.iconbitmap(THEME_ICON)
        except TclError:
            pass
        else:
            self.mainloop()

    def widget_arrange(self):
        self.input_caption()
        self.input()
        self.directory_choose()
        self.button()

    def input_caption(self):
        inp_caption = Label(self, text='单本地址：', compound='center')
        inp_caption.pack()

    def input(self):
        def handle_callback(event):
            nonlocal inp_tip_text
            self.inp.delete(0, END)
            wcb.OpenClipboard()
            try:
                inp_tip_text = wcb.GetClipboardData(win32con.CF_TEXT).decode("gb2312").strip()
            except (TypeError, UnicodeDecodeError) as e:
                print(e)
            wcb.CloseClipboard()
            if bool(self.site_detect.match(inp_tip_text)):
                self.inp.insert(0, inp_tip_text)

        def is_placeholder(event):
            nonlocal inp_tip_text
            self.inp.insert(0, inp_tip_text)

        inp_tip_text = '这里输入本子网址﹏'
        inp_tip = StringVar()
        inp_tip.set(inp_tip_text)

        self.inp = Entry(
            self, textvariable=inp_tip, width=20, fg="#666", bg="#ffac00",
            borderwidth=5, justify="left", insertborderwidth=6,
            relief="sunken", highlightcolor="azure", selectborderwidth=4
        )
        self.inp.bind("<FocusIn>", handle_callback)
        self.inp.bind("<FocusOut>", is_placeholder)
        self.inp.pack(pady=3, ipadx=5, ipady=2)

    def directory_choose(self):
        self.lb = Label(self)
        self.lb.pack()

    def button(self):
        def choose():
            self.dir_name = filedialog.askdirectory(initialdir="")
            dda = DEFAULT_DIR_ADDRESS
            dn = self.dir_name
            if dn:
                try:
                    dd = os_open(dda, O_CREAT | O_RDWR)
                except PermissionError:
                    showerror(title="错误", message="请确保C盘用户文件夹有读写权限哦")
                else:
                    if path.exists(dda):
                        os_close(dd)
                        os_remove(dda)
                        dd = os_open(dda, O_CREAT | O_RDWR)
                    os_write(dd, str.encode(dn))
                    os_close(dd)
                    self.lb.config(text="已选择存储地址:%s" % dn, fg="#00FA9A", font=("simsun", "9"))
            else:
                self.lb.config(text="未选择存储地址", justify=LEFT, fg="#FA8072", font=("simsun", "9"))

        def acquire_address():
            is_first = False
            if not isfile(DEFAULT_DIR_ADDRESS):
                self.lb.config(text="先选择文件夹哦", justify=LEFT, fg='#FA8072')
                is_first = True
                choose()
            a_r_tail = compile(r'(.+)\/\d+\/?$', M | I)
            address = self.inp.get()
            if bool(self.site_detect.match(address)):
                a_r_tail_search = a_r_tail.search(address)
                if bool(a_r_tail_search):
                    address = a_r_tail_search.group(1)
                Crawler177(address, self.dir_name, DEFAULT_DIR_ADDRESS)
            elif not is_first:
                showwarning(title="提示",
                            message="Σ( ° △ °|||)︴先输入正确网址喔~~\n(例如：http://www.177pic001.info/html/2018/07/2191389.html/3)")

        self.btn = Button(self, text="存储地址", bg="azure", fg="#666", padx=5, pady=0, command=choose)
        self.btn.pack(pady=20)
        Button(self, text="开始爬取", width=16, padx=6, pady=0, command=acquire_address).pack()


if __name__ == "__main__":
    InputGUI("177漫画单本下载器")
    freeze_support()

# http://www.177pic.info/html/2018/11/2480655.html
# http://www.177pic.info/html/2019/10/3172423.html

# http://www.177pic.info/html/2019/11/3188684.html
# http://www.177pic.info/html/2019/11/3188606.html
