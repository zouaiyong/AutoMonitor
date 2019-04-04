# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 10:12
# @Author  : zouay
# @Email   : zouaiyong@tuandai.com
# @File    : prettyTableDo.py
# @Software: PyCharm
from prettytable import PrettyTable

class PrettyTableDo:

    def getMsgForTableShowByListDict(self, listDictMsg, intPaddingLength):

        # listDictMsg: list集合数据,其元素未dict类型
        # 其内容例如:
        '''
        [{'org_name': '助成教育', 'rate': 100.0, 'org_id': 1941, 'shop_name': '助成教育思明分校', 'shop_id': 1290},
        {'org_name': '漳州伯乐教育', 'rate': 100.0, 'org_id': 2047, 'shop_name': '漳州伯乐教育', 'shop_id': 1398}]
        '''
        # 返回一个已经表格话的字符串类型数据

        if len(listDictMsg) != 0:

            if intPaddingLength <= 0:

                intPaddingLength = 0

            listTableTitle = list(listDictMsg[0].keys())
            strAlignTitle = listTableTitle[0]

            prettyTableContent = PrettyTable(listTableTitle)
            prettyTableContent.padding_width = intPaddingLength

            for listDictMsgItem in listDictMsg:
                listTableRowValue = []

                for listTitleItem in listTableTitle:
                    listTableRowValue.append(listDictMsgItem[listTitleItem])

                prettyTableContent.add_row(listTableRowValue)
        else:
            prettyTableContent = 'nothing value, may be the list is empty'
        return prettyTableContent.get_html_string(header=True,xhtml=True,attributes={'border':'1','cellspacing':'0', 'cellpadding':'0'})
        #return str(prettyTableContent)

if __name__ == "__main__":
    a = [{'org_name': '助成教育', 'rate': 100.0, 'org_id': 1941, 'shop_name': '助成教育思明分校', 'shop_id': 1290}]
    print(PrettyTableDo().getMsgForTableShowByListDict(a,1))