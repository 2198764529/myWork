import os
import sys
import csv
from json import dump,loads
from datetime import datetime,timezone
def process_files(directory, file_name):
    output_file = os.path.join(directory, "extracted_data.json")
    output_file_csv = os.path.join(directory, "extracted_data.csv")
    output_read_file_csv = os.path.join(directory, "extracted_read_data.csv")
    allJson = []
    allFindData = {} # 字典保存汇总数据
    # 递归搜索目录和子目录
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(file_name):
                json_file = os.path.join(root, file)
                json_content = ""
                # 从文件中读取JSON内容
                with open(json_file, "r",encoding='utf8') as f:
                    json_content = f.read()
                    print(json_file)
                    r = loads(json_content)['data']
                    if 'ridingOrders' in r:
                        r = r['ridingOrders']
                        allJson.extend(r)
    # 将数据保存到 CSV 文件
    with open(output_file_csv, 'w', newline='') as csv_file:
        
            csv_file_writer = csv.writer(csv_file)
            csv_file_writer.writerow(allJson[0].keys())  # 写入 CSV 头部
            for item in allJson:
                # 写入 extracted_data.csv
                csv_file_writer.writerow(item.values())

                # 写入 extracted_read_data.csv
                #开始时间和结束时间
                startDate = datetime.fromtimestamp(float(item['startTimestamp'])/1000)
                endDate = datetime.fromtimestamp(float(item['endTimestamp'])/1000)
                startTime = startDate.strftime("%H:%M")
                endTime = endDate.strftime("%H:%M")
                # 将差值转换为分钟
                CostMin = (endDate-startDate).total_seconds() // 60
                
                date = startDate.strftime("%Y/%m/%d")   # 提取日期

                if date not in allFindData: #若数据未写入汇总字典中,创建汇总词典
                    allFindData[date] = { 
                        'orderId':item['orderId'],
                        'startToEnd':"%s-%s"%(startTime,endTime),
                        'CostMin':CostMin,
                        'distanceMeter':item['distanceMeter'],
                        'findFlag':0,
                    }#写入汇总词典
                else: #若数据已写入汇总字典中,更新汇总词典
                    if item['orderId'] in allFindData[date]['orderId']: #利用 orderId 避免重复数据
                         continue
                    allFindData[date]['orderId'] += ';' + item['orderId']
                    allFindData[date]['startToEnd'] += ';' + "%s-%s"%(startTime,endTime)
                  
                    allFindData[date]['CostMin'] += CostMin
                    allFindData[date]['distanceMeter'] += item['distanceMeter']
                if (datetime(2023, 4, 17)<=startDate<=datetime(2023, 7, 11) or datetime(2023, 8, 25)<=startDate<=datetime(2023, 11, 17)) and CostMin>60: 
                     allFindData[date]['findFlag'] = 1
    with open(output_read_file_csv, 'w', newline='') as csv_file:
            csv_file_writer = csv.writer(csv_file)
            dates = allFindData.keys()
            # csv_file_writer.writerow(allFindData.keys())  # 写入 CSV 头部
            for k in allFindData:
                if allFindData[k].values():
                    csv_file_writer.writerow([k,]+list(allFindData[k].values()))
                    if allFindData[k]['findFlag']:
                        print(k,allFindData[k]['startToEnd'],allFindData[k]['CostMin'],allFindData[k]['distanceMeter'])
    dict
    with open(output_file, "w") as out_f:
         dump(allJson,out_f)





if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("请提供要搜索的目录路径和文件名。")
        directory_path = input("请输入要搜索的目录路径：")
        file_name_to_search = input("请输入要搜索的文件名：")
    else:
        directory_path = sys.argv[1]
        file_name_to_search = sys.argv[2]

    process_files(directory_path, file_name_to_search)
