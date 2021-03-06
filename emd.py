# -*- coding: utf-8 -*-

"""
#markdown text builder
"""

__author__ = 'awang'

import os, os.path, re  # nopep8


class MDBuilder(object):
    """
    MarkDown Docs Builder
    """
    skips_dir = ['tornado', 'emdpy', '.git', 'doc']  # 略过这些不生成文档的目录
    skips_file = ['emd.py', ]
    skips_suffix = ['pyc', 'pyo', 'swp', 'md', 'sample']
    note1 = r'^""".*"""$'
    note2 = r"^'''.*'''$"

    def __init__(self, path='.'):
        """"""
        self.path = path

    def start(self, line):
        """start"""
        pass

    def end(self, line):
        """end"""
        pass

    def eline(self, line):
        """escape line"""
        line = line.replace('"""', '').replace("'''", '')
        if line:
            return line + '\n'
        return line

    def reader(self, filename, name):
        """reader"""
        docs = ['##FROM: {}\n'.format(name)]
        record = False
        note = "'''"
        for line in open(filename, 'r').readlines():
            line = line.strip()
            eline = self.eline(line)
            # 如果注释在一行内写完，就一三引号开始和结束为判断，内容不为空或者换行符
            if re.match(self.note1, line) or re.match(self.note2, line):
            #    pass
            #if (line.startswith('"""') or line.startswith("'''")) \
            #    and (line.endswith('"""') or line.endswith("'''")):
                docs.append(eline)
                continue
            # 找到注释开始的那一行，开始记录到docs
            if line.startswith('"""') or line.startswith("'''"):
                if line.startswith('"""'):
                    note = '"""'
                docs.append(eline)
                record = not record
                continue
            # 找到注释结束的那一行，停止记录到docs
            if line.endswith(note):  # or line.endswith("'''"):
                docs.append(eline)
                record = not record
                continue
            # 记录注释到docs
            if record:
                docs.append(self.eline(line))
        docs.append('######END for file {}\n'.format(name))
        return ''.join(filter(None, docs))

    def writer(self, content, name, path='', mode='w'):
        """writer"""
        if path and not os.path.exists(path):
            os.mkdir(path)
        filename = os.path.join(path, name.split('.')[0]) + '.md'
        if not os.path.exists(filename):
            os.mknod(filename)
            replace_doc = content
        else:
            replace_doc = self.replacement(filename, name, content)
        md = open(filename, mode)
        md.write(replace_doc)
        md.close()

    def replacement(self, filename, name, new):
        """把对应文档中的内容替换了，自己手写的文档只要不在FROM 和 END 中间，就会继续保留"""
        docs = []
        record = False
        for line in open(filename, 'r').readlines():
            if line.startswith('##FROM: {}'.format(name)):
                record = not record
                docs.append(line)
                continue
            if line.endswith('######End for file {}\n'.format(name)):
                record = not record
                docs.append(line)
                continue
            if record:
                docs.append(line)
        old = ''.join(docs)
        total = open(filename, 'r').read()
        if old in total:
            return total.replace(old, new)
        return total + new

    def worker(self):
        """"""
        for file_list in os.walk(self.path + os.sep):
            if self.skiper(file_list[0].replace(self.path, '')):
                continue
            for filename in file_list[-1]:
                if filename.split('.')[-1] in self.skips_suffix or filename in self.skips_file:
                    continue
                if filename == '__init__.py':
                    self.writer(self.reader(os.path.join(file_list[0], filename), filename), file_list[0] + '_init.md', 'doc')
                elif filename.endswith('.py'):
                    self.writer(self.reader(os.path.join(file_list[0], filename), filename), filename, 'doc')

    def skiper(self, name):
        """"""
        for skip in name.split('/'):
            if skip in self.skips_dir:
                return True
        for skip in self.skips_dir:
            if name.startswith(skip):
                return True
        return False


    def readme(self):
        """暂时还有问题"""
        docs = []
        record = False
        for line in open('README.md', 'r').readlines():
            if line.startswith('#Docs'):
                record = not record
                docs.append(line)
                continue
            if line.endswith('Over Docs'):
                record = not record
                docs.append(line)
                continue
            if record:
                docs.append(line)
        if docs:
            doc_list = [docs[0]] + map(self.github_url, os.walk(os.path.join(self.path, 'doc') + os.sep).next()[-1]) + [docs[-1]]
        else:
            doc_list = ['#Docs\n'] + map(self.github_url, os.walk(os.path.join(self.path, 'doc') + os.sep).next()[-1]) + ['##Over Docs\n']
        old = ''.join(docs)
        new = ''.join(doc_list)
        total = open('README.md', 'r').read()
        if old in total:
            replace_doc = total.replace(old, new)
        else:
            replace_doc = total + new
        readme_writer = open('README.md', 'w')
        readme_writer.write(replace_doc)
        readme_writer.close()

    def github_url(self, name):
        """"""
        try:
            url = [url for url in open('.git/config', 'r').readlines() if url.startswith('\turl')][0]
        except:
            url = '\turl = git@github.com:ryanduan/music_api.git'
        return '*  [{}](http://github.com/{}/blog/master/doc/{})\n'.format(
            name,
            url.split('=')[-1].split('@')[-1].split(':')[-1].split('.')[0],
            name)


if __name__ == '__main__':
    """
    Run itself
    '''for test '''
    """
    MDBuilder().worker()
    MDBuilder().readme()