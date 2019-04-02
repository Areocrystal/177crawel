# coding="utf-8"
from requests import Session

from requests.exceptions import ConnectionError

from sys import path as sys_path

from os import \
    write as os_write, \
    close as os_close, \
    chdir, makedirs, listdir, getcwd, O_CREAT, O_RDWR, open as os_open

from os.path import join as path_join, basename, isdir, isfile

from re import compile, M, I

from time import sleep

from bs4 import BeautifulSoup

from aiohttp import ClientSession

from asyncio import get_event_loop, wait

from fake_useragent import UserAgent

from retry import retry

from multiprocessing import cpu_count, Pool

from random import random

from socket import timeout

from collections import deque

from tkinter import Tk, Label, Button, StringVar, \
    Entry, END, RIGHT, LEFT, filedialog, TclError

from tkinter.messagebox import showwarning, showinfo, showerror

from PIL import Image, ImageTk


class Crawler177:
    error_txt = '1.txt'
    auth_dirname = compile(r'[\<\>\?\:\*\\\/"\|]', M)
    failure = 0
    max_retry = 10

    def __init__(self, url, dir, dda):
        self.url = url
        if not dir:
            with open(path_join(sys_path[0], dda), 'r') as dir_name:  # path.dirname(__file__)
                self.dir = dir_name.readline()
                dir_name.close()
        else:
            self.dir = dir
        self.html = self.bs_soup(self.url)
        if self.html:
            chdir(self.dir)
            self.create_dir()

    def bs_soup(self, url, retries=1):
        with Session() as S:
            try:
                response = S.get(url=url, headers=self.headers, timeout=30)
            except ConnectionError:
                if retries > self.max_retry:
                    showerror(title="错误", message="呃~无法连接上主网站, o(≧口≦)o")
                    S.close()
                    return
                sleep(float('{:.1f}'.format(random())) + .1)
                self.bs_soup(self.url, retries + 1)
            else:
                response.encoding = 'utf-8'
                S.close()
                return BeautifulSoup(response.text, features='lxml')

    def get_img_source(sekf, img_list):
        return tuple(map(lambda img: img.get('src'), img_list))

    def acquire_img(sekf, u):
        try:
            raw_images = sekf.bs_soup(u).select('.entry-content img')
        except AttributeError:
            pass
        else:
            return sekf.get_img_source(raw_images)

    @property
    def headers(self):
        return {"User-Agent": UserAgent().random, "Referer": self.url}

    @property
    def acquire_img_1(self):
        return self.get_img_source(self.html.select('.entry-content img'))

    @property
    def acquire_pagination(self):
        return tuple(map(
            lambda anchor: anchor.get('href'), self.html.select('#single-navi a')[:-1]
        ))

    @property
    def acquire_title(self):
        return self.html.select('#post-55 h1')[0].get_text()

    async def download_pics(self, session, targets):
        for target in targets:
            try:
                async with session.get(
                        url=target, headers=self.headers, timeout=30
                ) as response:
                    response = await response.read()
            except Exception:
                self.failure += 1
                with open(self.error_txt, "a+") as img_url:
                    img_url.write("%s\n" % target)
                    img_url.close()
                continue
            else:
                with open(basename(target), 'wb') as fw:
                    fw.write(response)
                    fw.close()

    @retry(timeout, tries=10, delay=.2)
    def download_pics_add(self, target):
        s = Session()
        response = s.get(url=target, headers=self.headers, timeout=60)
        if response.status_code == 200:
            with open(target[target.rfind('/') + 1:-1], 'wb') as fw:
                fw.write(response.content)
                fw.close()
            self.failure -= 1
            with open(self.error_txt, mode="r") as urls:
                content = urls.read()
                urls.close()
            with open(self.error_txt, mode="w+") as urls:
                urls.write(content.replace(target, ''))
                urls.close()
        s.close()

    def create_dir(self):
        t = self.acquire_title
        if self.auth_dirname.search(t):
            t = self.auth_dirname.sub('', t)
        if not isdir(t):
            makedirs(t)
        a = "%s/%s" % (self.dir, t)
        chdir(a)
        with open("%s/%s" % (a, self.error_txt), "w") as tip:
            tip.write("{} 下载失败的图片：\n".format(self.url))
            tip.close()
        loop = get_event_loop()
        loop.run_until_complete(self.collection_start(loop))

    async def collection_start(self, loop):
        async with ClientSession() as session:  # 官网推荐建立 Session 的形式
            tasks = deque([
                loop.create_task(self.download_pics(session, self.acquire_img(p))) for p in self.acquire_pagination
            ])
            tasks.appendleft(loop.create_task(
                self.download_pics(session, self.acquire_img_1)
            ))
            await wait(tasks)
            if self.failure:
                await self.replenish()
            showinfo(
                title="完成", message=" φ(≧ω≦*)♪\n\r\n%s张图片下载成功，%s张下载失败！" % (
                    len(listdir()) - 1, self.failure))

    async def replenish(self):
        with open(self.error_txt, "r+") as remainimg:
            if self.failure:
                left_img = Pool(processes=cpu_count())
                left_img.map_async(func=self.download_pics_add, iterable=remainimg.readlines()[1:])
                left_img.close()
                left_img.join()
            remainimg.close()


class InputGUI(Tk):
    default_dir_address = 'C:\\Users\default-dir-177.ini'
    bg_address = 'Beautiful-Chinese-girl-retro-style-fantasy.PNG'
    theme_icon = '7.ico'

    def __init__(self, title, resolution='300x200'):
        super().__init__()
        self.address = None
        self.dir_name = None
        self.title(title)
        self.geometry(resolution)
        self.widget_arrange()
        try:
            set_bgi = ImageTk.PhotoImage(Image.open(fp=self.bg_address))
            self.bgi = Label(self, text='', image=set_bgi)
        except FileNotFoundError:
            self.bgi = Label(self)
        self.bgi.pack(side=RIGHT)
        try:
            self.iconbitmap(self.theme_icon)
            self.mainloop()
        except TclError:
            pass

    def widget_arrange(self):
        self.input_caption()
        self.input()
        self.directory_choose()
        self.button()

    def input_caption(self):
        inp_caption = Label(self, text='单本地址：', compound='center')
        inp_caption.pack()

    def input(self):
        def del_placeholder(event):
            self.inp.delete(0, END)

        def is_placeholder(event):
            nonlocal inp_tip_text
            self.inp.insert(0, inp_tip_text)

        inp_tip_text = '这里输入本子网址﹏'
        inp_tip = StringVar()
        inp_tip.set(inp_tip_text)

        self.inp = Entry(
            self, textvariable=inp_tip, width=20, fg="#666", bg="#ffef34", justify="left"
        )
        self.inp.bind("<FocusIn>", del_placeholder)
        self.inp.bind("<FocusOut>", is_placeholder)
        self.inp.pack(pady=3, ipadx=5, ipady=2)

    def directory_choose(self):
        self.lb = Label(self)
        self.lb.pack()

    def button(self):
        def choose():
            self.dir_name = filedialog.askdirectory(initialdir="")
            if self.dir_name:
                dd = os_open(self.default_dir_address, O_CREAT | O_RDWR)
                os_write(dd, str.encode(self.dir_name))
                os_close(dd)
                self.lb.config(text="已选择存储地址:%s" % self.dir_name, fg='#00FF7F')
            else:
                self.lb.config(text="未选择存储地址", justify=LEFT, fg='#FA8072')

        def acquire_address():
            is_first = False
            if not isfile(self.default_dir_address):
                self.lb.config(text="先选择文件夹哦", justify=LEFT, fg='#FA8072')
                is_first = True
                choose()
            a_r = compile(
                r'^https?:\/\/www\.177pic([az]?)\1(001)?\.((info)|(net)|(com)|(org))\/html\/20\d{2}\/\d{2}\/\d{4,8}\.html(\/\d{1,2})?$',
                M
            )
            a_r_tail = compile(r'\.html\/\d+$', M | I)
            address = self.inp.get()
            if a_r.match(address):
                if a_r_tail.search(address):
                    address = address[:address.rfind('/')]
                Crawler177(address, self.dir_name, self.default_dir_address)
            elif not is_first:
                showwarning(title="提示",
                            message="Σ( ° △ °|||)︴先输入正确网址喔~~\n(例如：http://www.177pic001.info/html/2018/07/2191389.html/3)")

        self.btn = Button(self, text="存储地址", bg="azure", fg="#666", padx=5, pady=0, command=choose)
        self.btn.pack(pady=20)
        Button(self, text="开始爬取", width=15, padx=5, pady=0, command=acquire_address).pack()

if __name__ == "__main__":
    InputGUI("177漫画单本爬取器")

# http://www.177pic001.info/html/2018/11/2480655.html