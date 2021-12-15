import matplotlib.pyplot as plt
import pandas as pd
import time
import os

# 一般不需要改变
temp_range = range(-30,120,10)  #测试的温度范围
temp_list = [str(i)+'.0°C' for i in temp_range]  #测试温度范围，字符形式
#temp_list = ['-30.0°C','-20.0°C','-10.0°C','0.0°C','10.0°C','20.0°C','30.0°C','40.0°C','50.0°C','60.0°C',
#             '70.0°C','80.0°C','90.0°C','100.0°C','110.0°C']
tablename = '@0result.csv'

# 需要每次设置
ref_list = ['10.13m_10.0%','10.08m_54.0%','10.12m_90.0%']  #数据文件夹
id_list = ['dis_accuracy','dis_precision','ref_accuracy','ref_precision']  #数据特征



class Excel_Combine():
    def __init__(self, temps, refs, filename, features):
        self.temp =[str(i)+'.0°C' for i in temps]
        self.temp_str = [str(i) for i in temps]
        self.ref = refs
        self.file = filename  #tablename
        self.fea = features   #features:dis_accuracy, PD, ....
        self.foldername = time.strftime("%Y-%m-%d~%H-%M-%S", time.localtime()) #获取字符串形式的本地时间
    def excel_process(self):
        os.mkdir(self.foldername)  #以本地时间创建文件夹
        for fea in self.fea:
            for ref in self.ref:
                fea_ref_df = pd.DataFrame()
                for temp in self.temp:
                    path = temp + '//' + ref + '//' + tablename
                    df = pd.read_csv(path,encoding='gbk')
                    mean_ = df[fea].mean()    #求各通道平均
                    list_ = list(df[fea]) + [mean_]
                    fea_ref_df[temp] = list_
                excel_name = self.foldername +'//'+ fea + '_' + ref + '.xlsx'
                fea_ref_df.to_excel(excel_name)  #excel存入文件夹
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
                if fea == 'dis_accuracy':
                    y_label += ' (mm)'
                elif fea == 'PD':
                    y_label += ' (%)'
                plt.ylabel(y_label)
                plt.savefig(self.foldername +'//'+ fea + ref + ".png", bbox_inches='tight')
                plt.clf()

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
        f.write('\n')
        f.write(str(Ranges))
        f.close()

        return Ranges


e_to_e = Excel_Combine(temp_range,ref_list,tablename,id_list)
e_to_e.excel_process()
e_to_e.draw_curve()
