# -*- coding: utl-8 -*-

"""
#markdown text builder
"""

__author__ = 'awang'

import os, os.path


class MDBuilder(object):
    """

    """

    def __init__(self, path='.'):
        """"""
        self.path = path

    def builder(self, filename):
        """"""
        docs = ['##FROM: {}\n'.format(filename)]
        record = False
        for line in open(filename, 'r').readlines():
            if line.startswith('"""') or line.startswith("'''"):
                record = not record
                continue
            if line.endswith('"""\n') or line.endswith("'''\n"):
                record = not record
                continue
            if record
                docs.append(line)
        docs.append('######End for file {}\n'.format(filename))
        return ''.join(docs)

    def element(self):
        """"""
        return os.walk(self.path + os.sep)

    def writer(self, content, name, path='', mode='w'):
        """"""
        md = open(os.path.join(path, name.split('.')[0]) + '.md', mode)
        md.write(content)
        md.close()

    def checker(self, content, name, path):
        """"""
        old_content = []
        for line in open(os.path.join(path, name), 'r').readlines():
            if line.startswith('##FROM: {}'.format())
        raise

    def factory(self):
        """"""
        for file_list in os.walk(self.path + os.sep):
            for filename in file_list[-1]:
                if filename == '__init__.py':
                    self.writer(self.builder(os.path.join(file_list[0], filename)), 'README.md', mode='a')
                elif filename.endswith('.py'):
                    self.writer(self.builder(os.path.join(file_list[0], filename)), 'README.md', mode='a')

