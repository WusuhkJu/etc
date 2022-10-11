# -*- coding: utf-8 -*-

!curl -s https://raw.githubusercontent.com/teddylee777/machine-learning/master/99-Misc/01-Colab/mecab-colab.sh | bash
!pip install wordcloud
!pip install Pillow

from google.colab import files
from konlpy.tag import Mecab
from wordcloud import WordCloud
from PIL import Image
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd
import re

class Wordcloud:
    def __init__(self, df, col_name='응답'):
        self.col_name = col_name
        self.raw = df[col_name].values

        self.cleaned_sentences = None

        self.n_tokens = None
        self.v_tokens = None
        self.a_tokens = None
        self.total_tokens_raw = None
        self.total_tokens_proc_1 = None
        self.total_tokens_proc_2 = None
        self.total_tokens_proc_all = None

        self.value_count = None
        self.value_count_abs = None
        self.freq_dic = None

    def get_cleaned(self):
        def sub(x):
            return re.sub("[^A-Za-z0-9가-힣 ]", '', str(x))
        pre_cleaned_sentences = [sub(sentence) for sentence in self.raw]

        cleaned_sentences = []
        def out_zero(x,cleaned_sentences=cleaned_sentences):
            if len(x) == 0:
                pass
            else:
                cleaned_sentences.append(x)
        [ out_zero(x) for x in pre_cleaned_sentences ]

        self.cleaned_sentences = np.array(cleaned_sentences)

        print('########## Sentences have been cleansed ##########')

    def get_tokens(self,n=True,v=True,a=True,erase_list=['있다','좋다','없다','같다','하다']):
        """
        :param n: 체언류 포함 여부
        :param v: 용언류 포함 여부
        :param a: 부사류 포함 여부
        :param erase_list: 제거하고 싶은 토큰 지정
        :return: total_tokens_raw = 문장 그대로 토큰화,
                 total_tokens_proc_1 = 길이가 1인 단어 제외,
                 total_tokens_proc_2 = 제거하고 싶은 단어 제거,
                 total_tokens_proc_all = proc_1, procl_2 모두 적용
        """

        mecab = Mecab(dicpath = r'C:/mecab/mecab-ko-dic')
        cleaned_sentences = self.cleaned_sentences

        total_tokens = []
        if n:
            n_tokens = []
            def n_tokenizer(x,mecab=mecab,n_tokens=n_tokens):
                n_list = ['NNG', 'NNP']
                t = mecab.pos(x)
                for tup in t:
                    if tup[1] in n_list:
                        n_tokens.append(tup[0])
            [n_tokenizer(x) for x in cleaned_sentences]
            for nn in n_tokens:
                total_tokens.append(nn)
            self.n_tokens = n_tokens

        if v:
            v_tokens = []
            def v_tokenizer(x,mecab=mecab,v_tokens=v_tokens):
                v_list = ['VV', 'VA', 'VA+EC', 'VA+EF']
                t = mecab.pos(x)
                for tup in t:
                    if tup[1] in v_list:
                        if (tup[1] == 'VV') or (tup[1] == 'VA'):
                            v_tokens.append(tup[0]+'다')
                        else:
                            v_tokens.append(tup[0])
            [v_tokenizer(x) for x in cleaned_sentences]
            for vv in v_tokens:
                total_tokens.append(vv)
            self.v_tokens = v_tokens

        if a:
            a_tokens = []
            def a_tokenizer(x,mecab=mecab,a_tokens=a_tokens):
                a_list = ['MAG']
                t = mecab.pos(x)
                for tup in t:
                    if tup[1] in a_list:
                        a_tokens.append(tup[0])
            [a_tokenizer(x) for x in cleaned_sentences]
            for aa in a_tokens:
                total_tokens.append(aa)
            self.a_tokens = a_tokens

        total_tokens_no_one_letter = []
        def get_over_one(token,total_tokens_no_one_letter=total_tokens_no_one_letter):
            if len(token) > 1:
                total_tokens_no_one_letter.append(token)
        [get_over_one(token) for token in total_tokens]

        total_tokens_erase_words = []
        def get_erase(token,total_tokens_erase_words=total_tokens_erase_words):
            if token in erase_list:
                pass
            else:
                total_tokens_erase_words.append(token)
        [get_erase(token) for token in total_tokens]

        total_tokens_proc_all = []
        [get_erase(token,total_tokens_proc_all) for token in total_tokens_no_one_letter]

        self.total_tokens_raw = total_tokens
        self.total_tokens_proc_1 = total_tokens_no_one_letter
        self.total_tokens_proc_2 = total_tokens_erase_words
        self.total_tokens_proc_all = total_tokens_proc_all

        print('########## tokens have been made ##########')

    def get_freq(self,token_type='proc_all',percent=0.5):
        if token_type == 'raw':
            tokens = self.total_tokens_raw
        elif token_type == 'proc_1':
            tokens = self.total_tokens_proc_1
        elif token_type == 'proc_2':
            tokens = self.total_tokens_proc_2
        elif token_type == 'proc_all':
            tokens = self.total_tokens_proc_all

        value_count = pd.DataFrame({'token':tokens}).value_counts(normalize=True)
        value_count_abs = pd.DataFrame({'token':tokens}).value_counts(normalize=False)

        adding = 0
        cri_percent = percent
        i = 0
        while adding <= cri_percent:
            adding += value_count[i]
            i += 1

        letters = []
        counts = []
        for l,c in value_count_abs.items():
            letters.append(l[0])
            counts.append(c)

        using_letters = letters[:i]
        using_counts = counts[:i]

        freq_dic = {}
        for l,c in zip(using_letters,using_counts):
            freq_dic[l] = c

        def get_df(series):
            letters = []
            counts = []
            for l, c in series.items():
                letters.append(l[0])
                counts.append(c)
            return pd.DataFrame( {'letters':np.array(letters), 'counts':np.array(counts)} )

        self.value_count = get_df(value_count)
        self.value_count_abs = get_df(value_count_abs)
        self.freq_dic = freq_dic

    def get_wordcloud(self,font,img,width=1000,height=700,horizontal=False,colormap='viridis',background_color='white'):
        """
        'viridis' # 기본 색상
        'tab10', 'hls', 'husl', 'Set2', 'Paired','rocket'
        'mako', 'flare', 'crest', 'magma', 'viridis', 'spring', 'summer'
        """
        mask = Image.open(img)
        mask_arr = np.array(mask)
        print('===please wait=>')

        wordcloud = WordCloud(font_path=font,mask=mask_arr,width=width,height=height,prefer_horizontal=horizontal,background_color=background_color,colormap=colormap)
        wordcloud.generate_from_frequencies(self.freq_dic)
        print('===please wait===>')

        plt.figure(figsize=(width/100, height/100))
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()

# Uploading datasets
upload = files.upload()

df = pd.read_excel(r'')
font = r''
img = r''

w = Wordcloud(df)
w.get_cleaned()
w.get_tokens()
w.get_freq()

w.get_wordcloud(font=font,img=img)
