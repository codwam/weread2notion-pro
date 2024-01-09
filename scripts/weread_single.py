#!/usr/bin/python3

import argparse
import os
import json

from weread_api import WeReadApi


class Helper:

    @classmethod
    def write_obj(cls, file_name, data):
        s = None
        if isinstance(data, list):
            s = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
        elif isinstance(data, dict):
            s = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            s = data
        #
        Helper.write(file_name, s)

    @classmethod
    def write(cls, file_name, s):
        if isinstance(s, str) == False:
            print("error type: %s" % (type(s)))
            return

        curpath = os.path.abspath(os.curdir)
        fullpath = os.path.join(curpath, file_name)
        print("Trying to open: %s" % (fullpath))
        #
        with open(fullpath, "w") as file:
            file.write(s)
    
    @classmethod
    def read(cls, file_name):
        curpath = os.path.abspath(os.curdir)
        fullpath = os.path.join(curpath, file_name)
        print("Trying to open: %s" % (fullpath))
        #
        file = open(fullpath, "r")
        return file.read()
            

class SingleWeread:
    def __init__(self):
        # 本地 CookieFile 存放 Cookie，不会同步到 git
        self.__weread_api = WeReadApi(Helper.read("tmp/CookieFile"))

    def save_book_details(self, title):
        """
        获取书本详情
        """
        try:
            books = self.__weread_api.get_notebooklist()
            Helper.write_obj("tmp/get_notebooklist.json", books)
            if books != None:
                for index, book in enumerate(books):
                    bookId = book.get("bookId")
                    b_book = book.get("book")
                    b_title = b_book.get("title")
                    if title == b_title:
                        b_json = self.__weread_api.get_bookinfo_data(bookId)
                        Helper.write_obj(f"tmp/《{title}》", b_json)
                        chapter = self.__weread_api.get_chapter_info(bookId)
                        Helper.write_obj(f"tmp/《{title}》 - 目录", chapter)
                        chapter_output = []
                        for key, value in chapter.items():
                            if value["level"] == 1:
                                chapter_output.append(value["title"])
                        Helper.write(f"tmp/《{title}》 - 目录 (修改)", "\n\n".join(chapter_output))
                        bookmark_list = self.__weread_api.get_bookmark_list(bookId)
                        Helper.write_obj(f"tmp/《{title}》 - 划线", bookmark_list)
                        reviews = self.__weread_api.get_review_list(bookId)
                        Helper.write_obj(f"tmp/《{title}》 - 笔记", reviews)
            else:
                print("获取书本详情失败")
        except Exception as e:
             print(e)
             return
        
        print("获取书本详情成功")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # options = parser.parse_args()
    sw = SingleWeread()
    sw.save_book_details("学习之道：11天高效入门版")
    
