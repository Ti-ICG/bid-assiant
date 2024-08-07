import preprocessing_lib

if __name__ == '__main__':
    #招标文件路径
    bid_path = r'E:\招标雷达\招标雷达\招投标参考文件（标书、招标文件）——内部学习参考使用\招标文件集合\附件4.招标文件（私有弹性云计算软件平台）.docx'  #附件4.招标文件（私有弹性云计算软件平台）.docx   6.25定稿-智能问答系统项目-物资类竞争性谈判文件.docx
    #需要检索的章节内容
    input_text = '技术内容'
    #处理后的文档保存路径
    output_path = 'E:\\招标雷达\\招标雷达\\标书拆分\\'
    #置信度阈值，最大值为1，越低相关性越小
    confidence=0.65

    #招标文件预处理
    preprocessing_lib.preprocess_docx(bid_path,output_path,confidence,input_text)