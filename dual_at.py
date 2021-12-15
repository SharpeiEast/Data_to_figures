


import matplotlib.pyplot as plt
import pandas as pd
import time
import os

# 一般不需要改变
temp_range = range(-30,120,10)  #测试的温度范围
temp_list = [str(i) for i in temp_range]  #测试温度范围，字符形式
tablename = '.xlsx'
title_of_figures={'dis_accuracy': 'Accuracy of distance measurements within ' + str(temp_range[0]) + ' ~ ' + str(temp_range[-1])+  '℃'
                     ,'dis_precision': 'Precision of distance measurement within ' + str(temp_range[0]) + ' ~ ' + str(temp_range[-1])+  '℃'
                     ,'ref_accuracy': 'Accuracy of reflectivity measurements within ' + str(temp_range[0]) + ' ~ ' + str(temp_range[-1])+  '℃'
                     ,'ref_precision': 'Precision of reflectivity measurement within ' + str(temp_range[0]) + ' ~ ' + str(temp_range[-1])+  '℃'
                     ,'PD': 'Probability of detection within' + str(temp_range[0]) + ' ~ ' + str(temp_range[-1])+  '℃'
                  }


# 需要每次设置
folders = ['2021-11-29~17-13-13','2021-11-29~14-37-19']  #数据文件夹
line_type = ['-','--']
line_style = {folders[i]:line_type[i] for i in range(2)}  #作图所用的雷达线型
id_list = ['dis_accuracy','dis_precision','ref_accuracy','ref_precision']  #数据特征
dist_ref = [['10.64m_10.0%','11.18m_54.0%','10.82m_94.0%'],['10.38m_10.0%','10.26m_54.0%','10.54m_94.0%']]  # 数据文件名称
dist_ref_dict = {folders[i]:dist_ref[i] for i in range(len(folders))}

R_names = ['ex1r','efs2']
Rnames = {folders[i]:R_names[i] for i in range(2)} #文件夹对应的雷达名称



class Dual_lidar():
    def __init__(self, folder_list, feature_list, tempstr_list, dist_ref_dict, tabletype, Rnames, lines,figure_titles):
        self.temp_str = tempstr_list    # char type temperature, eg: -10.0℃
        self.fea = feature_list         # index of table, eg: 'dis_accuracy','dis_precision'
        self.folder = folder_list       # folder names, eg: '2021-11-29~17-13-13','2021-11-29~14-37-19'
        self.suffix = dist_ref_dict     # distance and reflection of test scenarios, eg: 10.64m_10.0%
        self.R_names = Rnames          # sn index of lidar, eg: xxxx.....xxxx
        self.file_type = tabletype      # type of file, eg: xlsx, csv
        self.line_style = lines         # type of line, eg: '-', '--'
        self.FT = figure_titles         # title of figure, eg: 'dis_accuracy': 'Accuracy of distance measurements'
        self.foldername = time.strftime("%Y-%m-%d~%H-%M-%S", time.localtime()) #获取字符串形式的本地时间
    def dual_draw(self):
        os.mkdir(self.foldername + '_dual_lidar')
        for path1 in self.fea:
            legend_list = []
            plt.figure(num='dual_lidar', figsize=(7.5, 6))
            legends = []
            for path2 in self.folder:

                for path3 in self.suffix[path2]:
                    file_path = path2 + '//' + path1 + '_' + path3 + self.file_type   ## 读取雷达数据
                    data_frame = pd.read_excel(file_path)
                    y_ = data_frame.iloc[-1].tolist() #提取data frame最后一行
                    y_.pop(0)
                    #print(y_)
                    plt.plot(self.temp_str, y_, linewidth=2.0, linestyle=self.line_style[path2])
                    legend_list.append(path3 + '_' + self.R_names[path2])
            plt.title(path1)
            if self.FT.__contains__(path1):
                plt.title(self.FT[path1])
            plt.xlabel("Temperature (℃)")
            y_label = path1
            if path1 == 'dis_accuracy':
                y_label += ' (mm)'
            elif path1 == 'PD':
                y_label += ' (%)'
            plt.ylabel(y_label)
            plt.legend(legend_list)
            plt.savefig(self.foldername + '_dual_lidar' + '//' + '000hushi---' + path1 + ".png", bbox_inches='tight')
            plt.clf()
        return 0

dual_lidar = Dual_lidar(folders,id_list,temp_list,dist_ref_dict,tablename,Rnames,line_style,title_of_figures)
dual_lidar.dual_draw()
