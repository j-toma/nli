# 母语识别
## DEMO
![](demo2.gif)

### 项目解释
-[项目提案](appIdea.pdf)

-[获取资料](https://docs.qq.com/doc/DYmdpdnRQUm5wVlRu)

### 背景资料
-[报告](background.pdf)

-[A Report on the First Native Language Identification Shared Task](https://www.aclweb.org/anthology/W13-1706/)
```
@inproceedings{tetreault-etal-2013-report,
    title = "A Report on the First Native Language Identification Shared Task",
    author = "Tetreault, Joel  and
      Blanchard, Daniel  and
      Cahill, Aoife",
    booktitle = "Proceedings of the Eighth Workshop on Innovative Use of {NLP} for Building Educational Applications",
    month = jun,
    year = "2013",
    address = "Atlanta, Georgia",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W13-1706",
    pages = "48--57",
}
```
-[Native Language Identificatio non Text and Speech](https://www.aclweb.org/anthology/W17-5045/)
```
@inproceedings{zampieri-etal-2017-native,
    title = "Native Language Identification on Text and Speech",
    author = "Zampieri, Marcos  and
      Ciobanu, Alina Maria  and
      Dinu, Liviu P.",
    booktitle = "Proceedings of the 12th Workshop on Innovative Use of {NLP} for Building Educational Applications",
    month = sep,
    year = "2017",
    address = "Copenhagen, Denmark",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W17-5045",
    doi = "10.18653/v1/W17-5045",
    pages = "398--404",
    abstract = "This paper presents an ensemble system combining the output of multiple SVM classifiers to native language identification (NLI). The system was submitted to the NLI Shared Task 2017 fusion track which featured students essays and spoken responses in form of audio transcriptions and iVectors by non-native English speakers of eleven native languages. Our system competed in the challenge under the team name ZCD and was based on an ensemble of SVM classifiers trained on character n-grams achieving 83.58{\%} accuracy and ranking 3rd in the shared task.",
}
```

### 指示
下载安装
```
git clone https://github.com/j-toma/nli.git
pip install requirements/site.txt
python3 app.py
```
因为模型超过github的最大文件大小的限制，请打开这个[腾讯微云文件夹](https://share.weiyun.com/kbrvsZai)，密码为6fm395，最好要下载整个文件夹，把他放在nli文件夹里面。

打开127.0.0.1:5000，上传或粘贴您要检查的内容。可以上传用腾讯微云里面的两个.txt文件来测试一下。test_true.txt作者的母语是英语，test_false.txt作者的母语是中文。

### 注意
结果和语法或拼写没有关系，模型只是按照文件里出现的2-grams和3-grams判断整个文件是什么母语的作者给写的。意思是如果有东西在Strong Non Native那个类别里面，这是说该文件里出现一些经常在非母语作者的论文出现的2-grams或3-grams。按照这个想法，不一定要去该这些，因为不一定有语法错误，但是你可以考虑一下能不能换一个说法，改善的的写作风格。

有问题可以联系我jtoma5@protonmail.com

