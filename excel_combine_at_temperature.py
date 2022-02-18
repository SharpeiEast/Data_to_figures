


import matplotlib.pyplot as plt
import pandas as pd
import time
import os
import shutil
from math import sqrt

# 一般不需要改变
temp_range = range(-30,120,10)  #测试的温度范围
temp_list = [str(i)+'.0°C' for i in temp_range]  #测试温度范围，字符形式
#temp_list = ['-30.0°C','-20.0°C','-10.0°C','0.0°C','10.0°C','20.0°C','30.0°C','40.0°C','50.0°C','60.0°C',
#             '70.0°C','80.0°C','90.0°C','100.0°C','110.0°C']
tablename = '@0result.csv'

# 需要每次设置
ref_list = ['26.76m_10.0%']  #数据文件夹
id_list = ['PD','peak_rms','peak_mean','rms_mean']  #数据特征
# id_list = ['dis_accuracy','dis_precision','ref_accuracy','ref_precision']


class Excel_Combine():
    def __init__(self, temps, refs, filename, features):
        self.temp =[str(i)+'.0°C' for i in temps]
        self.temp_str = [str(i) for i in temps]
        self.ref = refs
        self.transmittance = 0.4  # 光筛透过率
        self.file = filename  #tablename
        self.fea = features   #features:dis_accuracy, PD, ....
        self.foldername = time.strftime("%Y-%m-%d~%H-%M-%S", time.localtime()) #获取字符串形式的本地时间
    def excel_process(self):
        os.mkdir(self.foldername)  #以本地时间创建文件夹
        fig_name = ''
        for fea in self.fea:
            for ref in self.ref:
                fea_ref_df = pd.DataFrame()
                fig_name += (fea + '_' + ref)
                plt.figure(num=fig_name, figsize=(15, 9))
                legend_list = []
                for temp in self.temp:
                    path = temp + '//' + ref + '//' + tablename
                    df = pd.read_csv(path,encoding='gbk')
                    laserIDnum = [i for i in range(len(df['laserID']))]
                    df_sort = df.sort_values(by=['laserID'], ascending=[True]) # 按照雷达通道id排序，否则有时候输出的图片x左边轴雷达id是逆序
                    laserID_str = [str(id) for id in df_sort['laserID']]
                    plt.plot(laserID_str, df_sort[fea])
                    mean_ = df[fea].mean()    #求各通道平均
                    list_ = list(df[fea]) + [mean_]
                    fea_ref_df[temp] = list_
                    legend_list.append(temp)
                excel_name = self.foldername +'//'+ fea + '_' + ref + '.xlsx'
                fea_ref_df.to_excel(excel_name)  #excel存入文件夹
                plt.title(fea + '_' + ref)

                plt.xlabel('LaserID')
                y_label = fea
                if fea in ['dis_accuracy', 'dis_precision']:
                    y_label += ' (cm)'
                elif fea in ['PD', 'ref_accuracy', 'ref_precision']:
                    y_label += ' (%)'
                plt.ylabel(y_label)
                plt.legend(legend_list)
                plt.savefig(self.foldername +'//'+ fea + ref + 'LaserID' + ".png", bbox_inches='tight')
                plt.clf()
        return 0
    def draw_curve(self):
        Ranges = {}
        for fea in self.fea:
            ref_y = []
            fig_name = 'multi_ref'  #不会显示图中，仅用于区分
            legend_list = []
            Range = 0
            for ref in self.ref:
                excel_name = self.foldername +'//' + fea + '_' + ref + '.xlsx'
                df = pd.read_excel(excel_name)
                y = [ float(format(df.iloc[-1,i], '.3f')) for i in range(1,df.shape[1])]
                Range =max(Range, max(y) - min(y))
                print(fea + '_' + ref + '--------result of laser_id in average: ',y)  #输出POD、或者其他什么东西的各通道均值
                plt.figure(figsize=(7.5, 6.0))
                plt.plot(self.temp_str,y)
                plt.title(fea + ref)
                plt.xlabel("Temperature (℃)")
                y_label = fea
                if fea in ['dis_accuracy','dis_precision']:
                    y_label += ' (cm)'
                elif fea in ['PD', 'ref_accuracy', 'ref_precision']:
                    y_label += ' (%)'
                plt.ylabel(y_label)
                plt.savefig(self.foldername +'//'+ fea + ref + ".png", bbox_inches='tight')
                plt.clf()

                if fea == 'peak_rms':
                    y_dis = [sqrt(yi) * float(ref[:5]) / self.transmittance for yi in y]
                    plt.figure(figsize=(7.5, 6.0))
                    plt.plot(self.temp_str, y_dis)
                    plt.title(fea + ref + ' Equivalent Distance')
                    plt.xlabel("Temperature (℃)")
                    y_label = 'Equivalent Distance'
                    plt.ylabel(y_label)
                    plt.savefig(self.foldername + '//' + '00hushi---' + fea + ref + 'E_D' + ".png", bbox_inches='tight')
                    plt.clf()
                    print(fea + '_' + ref + 'E_D' + '--------result of laser_id in average: ', y_dis)  # 输出POD、或者其他什么东西的各通道均值

                figbox = plt.figure(figsize=(20, 12))
                plt.title(fea + '~' + ref,fontsize=20)
                boxplot = df.boxplot(column=self.temp)
                plt.xlabel("Temperature (℃)",fontsize = 20)
                y_label = fea
                if fea in ['dis_accuracy','dis_precision']:
                    y_label += ' (cm)'
                elif fea in ['PD', 'ref_accuracy', 'ref_precision']:
                    y_label += ' (%)'
                plt.ylabel(y_label,fontsize = 20)
                plt.xticks(fontsize = 15)
                plt.yticks(fontsize = 15)
                figbox.savefig(self.foldername + '//' + ref[:-1] + '_' + fea + "_boxplot.png", bbox_inches='tight')
                figbox.clf()



                ref_y.append(y)
                fig_name += ref
                legend_list.append(ref)
            plt.figure(num=fig_name, figsize=(7.5, 6.0))
            for y_ in ref_y:
                plt.plot(self.temp_str, y_, linewidth=2.0, linestyle='--')
            plt.legend(legend_list)
            plt.xlabel('temperature (℃)')
            y_label = fea

            if fea in ['dis_accuracy','dis_precision']:
                y_label += ' (cm)'
            elif fea in[ 'PD', 'ref_accuracy','ref_precision']:
                y_label += ' (%)'
            plt.ylabel(y_label)
            plt.savefig(self.foldername + '//' + '00hushi---' + fea +  ".png", bbox_inches='tight')
            plt.clf()

            Ranges[fea] = Range
        print('各特征极差：',Ranges)
        f = open(self.foldername + '//' + '00hushi---Ranges.txt','a')
        # f.write('\n')
        f.write(str(Ranges))
        f.close()
        return Ranges
    def mycopyfile(self,srcfile,dstpath):  # 复制函数，复制一份文件在指定文件夹
        if not os.path.isfile(srcfile):
            print("%s not exist!" % (srcfile))
        else:
            fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
            if not os.path.exists(dstpath):
                os.makedirs(dstpath)  # 创建路径，这个地方会创建一个空文件夹，在这里倒是没什么用
            shutil.copy(srcfile, dstpath + fname)  # 复制文件
            print("copy %s -> %s" % (srcfile, dstpath + fname))
    def figure_movement2(self):  #将每个目标板测得的文件复制一份然后挪到指定文件夹，本函数中指定文件夹是创建的以本地时间为名称的文件夹，它只能移动文件，不移动文件夹
        for ref in self.ref:
            for file in os.listdir(ref):
                if os.path.isfile(os.path.join(ref, file)) == True:
                    Excel_Combine.mycopyfile(self,ref + '//' + file, self.foldername + '//' + ref[:-1] + '_')
                else:
                    print(ref + '//' + file + ' ：这不是个文件，可能是个文件夹？')
        return 0


    def figure_movement(self): #这个函数没有启用，是一个重命名函数
        for ref in self.ref:
            for file in os.listdir(ref):
                if os.path.isfile(os.path.join(ref,file)) == True:
                    prefix = ref[:-1] + '_'
                    prefix_len = len(prefix)
                    # new_name = file.replace(file, prefix + file)
                    # os.rename(os.path.join(ref, file), os.path.join(self.foldername, new_name))
                    origin_name = file.replace(file, file[prefix_len:])
                    os.rename(os.path.join(ref, file), os.path.join(ref, origin_name))

                else:
                    print(0)
        #     for fea in self.fea:
        # #         print(fea)
        # #     print(ref[:-1])
        #
        # for root, dirs, files in os.walk(self.ref[0]):
        #     for file in files:
        #         Excel_Combine.mycopyfile()

        return 0

e_to_e = Excel_Combine(temp_range,ref_list,tablename,id_list)
e_to_e.excel_process()
e_to_e.draw_curve()
e_to_e.figure_movement2()
# e_to_e.figure_movement()
