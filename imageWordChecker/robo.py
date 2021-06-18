import os
import re
import time

from PIL import Image
import pyocr
import pyocr.builders
from googletrans import Translator

class imageWordCheckRobo():

    def __init__(self, image_path, ng_word):
        self.image_path = image_path
        self.ng_word = ng_word


    def getOCRTool(self):
        # Tesseract-OCRのパスを通す
        path_tesseract = "C:\\Program Files\\Tesseract-OCR"
        if path_tesseract not in os.environ["PATH"].split(os.pathsep):
            os.environ["PATH"] += os.pathsep + path_tesseract
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print('利用可能なOCRツールが見つかりません。')
            self.tool = None
        else:
            self.tool = tools[0]
            print(f'このOCRツールを利用します：{self.tool.get_name()}')


    def setTolLang(self):
        if self.tool is None:
            print('使用可能なOCRツールが見つかりません。')
            self.lang = None
        else:
            if self.img_lang == 'en':
                lang_num = 0
            elif self.img_lang == 'ja':
                lang_num = 1
            # 0:Eng 1:Jpn
            langs = self.tool.get_available_languages()
            self.lang = langs[lang_num]


    def imageToText(self):
        if self.tool is None or self.lang is None:
            print('ツール設定に異常があります。設定内容を確認してください。')
            return ''
        else:
            content = self.tool.image_to_string(
                Image.open(self.image_path),
                lang = self.lang,
                # tesseract_layoutは、文字認識のパターン、バリエーションのこと。0~13の範囲で設定可能。デフォルトは３
                builder = pyocr.builders.TextBuilder(tesseract_layout=3)
            )
            return content


    def cleaningContent(self, content):
        content.encode('utf-8')
        content = re.sub('([あ-んア-ン一-龥ー])\s+((?=[あ-んア-ン一-龥ー]))',r'\1\2', content)
        content = re.sub(' ', '', content)
        content_list = content.split('\n')
        content_list = [text for text in content_list if text != '']
        return content_list


    def googleTrans(self,text):
        trans = Translator()
        while True:
            try:
                trans_text = trans.translate(text)
                break
            except:
                time.sleep(1)
        return trans_text.text

    def job(self):
        self.getOCRTool()
        self.img_lang = input('画像内で使用されている言語を指定しください。en or ja:')
        print('画像をテキストに変換中…。')
        self.setTolLang()
        content = self.imageToText()
        content_list = self.cleaningContent(content)
        print('-----------画像内テキスト----------------')
        for text in content_list:
            print(text)
        print('--------------------------------------')
        check = 0
        for text in content_list:
            if self.ng_word in text:
                print('下記の文章内で、NGワードを発見しました。')
                print(f'=>{text}')
                check = 1
        if check == False:
            print('画像内にNGワードはありませんでした。')
        # self.final_lang = input('出力文の言語を選択してください。en or ja:')
        # # if self.img_lang == self.final_lang:
        #     print('-----------最終テキスト----------------')
        #     for text in content_list:
        #         print(text)
        #     print('--------------------------------------')
        # else:
        #     print('翻訳中…')
        #     trans_content_list = []
        #     for text in content_list:
        #         trans_content_list.append(self.googleTrans('これはテストです。'))
        #     print('翻訳が完了しました。')
        #     print('-----------最終テキスト----------------')
        #     for text in trans_content_list:
        #         print(text)
        #     print('--------------------------------------')