import pandas as pd
import numpy as np
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"

filename_raw = input("Enter a class to grade (i.e. class1 for class1.txt): ")

filename = filename_raw + ".txt"

num_error = 0

def check_data(data):
    value_in_data = data.split(',')
    #check len data
    if len(value_in_data) != 26:
        print("Invalid line of data: does not contain exactly 26 values: ")
        print(data)
        return False
    #check id
    id = value_in_data[0]
    if id[0] != "N" or len(id) != 9:
        print("Invalid line of data: N# is invalid: ")
        print(data)
        return False
    list_num_in_id = id[1:9]
    try:
        for num in list_num_in_id:
            num_check = int(num)
    except:
        print("Invalid line of data: N# is invalid: ")
        print(data)
        return False
    return True

def tinh_diem(data,key):
    data = data.strip()
    value_in_data = data.split(',')
    list_dap_an = key.split(',')
    list_cau_tra_loi = value_in_data[1:26]
    diem = 0
    mssv = value_in_data[0]
    for index,tra_loi in enumerate(list_cau_tra_loi):
        if tra_loi == "":
            continue
        else:
            if tra_loi == list_dap_an[index]:
                diem += 4
            else:
                diem -= 1
    return mssv,diem
def normal():
    num_error = 0
    list_diem = []
    list_mssv = []
    # try:
    with open(filename,'r') as f:
        print("Successfully opened " + filename)
        list_data = f.readlines()
    print("**** ANALYZING ****")
    for data in list_data:
        if check_data(data) == False:
            num_error += 1
        else:
            mssv,diem = tinh_diem(data,answer_key)
            list_diem.append(diem)
            list_mssv.append(mssv)
    if num_error == 0:
        print("No errors found!")
    print("**** REPORT ****")
    print("Total valid lines of data: "+ str(len(list_data)-num_error))
    print("Total invalid lines of data: "+str(num_error))
    f.close()
    print("Mean (average) score: " + str(sum(list_diem)/len(list_diem)))
    print("Highest score: "+ str(max(list_diem)))
    print("Lowest score: "+ str(min(list_diem)))
    print("Range of scores: "+ str(max(list_diem)- min(list_diem)))
    print(list_diem)
    list_diem_raw = list_diem
    list_diem = sorted(list_diem)
    print(list_diem)
    if len(list_diem)%2 == 0:
        median = (list_diem[int(len(list_diem)/2)] + list_diem[int(len(list_diem)/2)-1])/2
        print("Median score : "+ str(median))
    else:
        median = list_diem[int(len(list_diem)/2)]
        print("Median score : "+ str(median))
    filename_out = "output/"+filename_raw + "_grades.txt"
    with open(filename_out,"w") as f2:
        for index,diem in enumerate(list_diem_raw):
            f2.writelines(list_mssv[index]+","+str(diem)+"\n")
    f2.close()
    print("Saved in : " + filename_out)
    # except:
    #     print("File cannot be found")


def numpy_array_true(np_array):
    if np_array.shape[0] != 26:
        print("Invalid line of data: does not contain exactly 26 values: ")
        print(np_array)
        return False
    #check id
    id = np_array[0]
    if id[0] != "N" or len(id) != 9:
        print("Invalid line of data: N# is invalid: ")
        print(np_array)
        return False
    list_num_in_id = id[1:9]
    try:
        for num in list_num_in_id:
            num_check = int(num)
    except:
        print("Invalid line of data: N# is invalid: ")
        print(np_array)
        return False
    return True

def usage_pandas_and_numpy():
    answer_key_np = np.array(answer_key.split(","))
    num_error = 0
    list_np_diem_sv = np.array([])
    list_np_mssv = np.array([])
    try:
        data = pd.read_fwf(filename,header=None)
        print("**** ANALYZING ****")
        for index, row in data.iterrows():
            data_row = row[0] # data tung dong
            list_data_one_student = data_row.split(',')
            list_data_one_student_np = np.array(list_data_one_student)
            if numpy_array_true(list_data_one_student_np) == False:
                num_error += 1
            else:
                list_tra_loi = list_data_one_student_np[1:26]
                #lay cau tra loi bi bo qua
                so_cau_bo_qua = np.count_nonzero(list_tra_loi == "")
                list_check = list_tra_loi == answer_key_np
                so_cau_sai = np.count_nonzero(list_check == False) - so_cau_bo_qua
                so_cau_dung = 25 - so_cau_sai - so_cau_bo_qua
                so_diem = so_cau_dung*4 - so_cau_sai
                list_np_diem_sv = np.append(list_np_diem_sv,so_diem)
                list_np_mssv = np.append(list_np_mssv,list_data_one_student[0])

        list_np_diem_sv_raw = list_np_diem_sv
        tong_diem = 0
        max_diem = list_np_diem_sv[0]
        min_diem = list_np_diem_sv[0]
        for diem in list_np_diem_sv:
            if diem > max_diem:
                max_diem = diem
            if min_diem > diem:
                min_diem = diem
            tong_diem += diem
        if num_error == 0:
            print("No errors found!")
            # print(list_data_one_student_np.shape)

        print("**** REPORT ****")
        print("Total valid lines of data: " + str(len(data) - num_error))
        print("Total invalid lines of data: " + str(num_error))
        print("Mean (average) score: "+ str(tong_diem/list_np_diem_sv.shape[0]))
        print("Highest score : "+str(max_diem))
        print("Lowest score: "+ str(min_diem))
        print("Range of scores: "+ str(max_diem - min_diem))
        list_np_diem_sv = np.sort(list_np_diem_sv)
        if len(list_np_diem_sv) % 2 == 0:
            median = (list_np_diem_sv[int(len(list_np_diem_sv) / 2)] + list_np_diem_sv[int(len(list_np_diem_sv) / 2) - 1]) / 2
            print("Median score : " + str(median))
        else:
            median = list_np_diem_sv[int(len(list_np_diem_sv) / 2)]
            print("Median score : " + str(median))
        # data_write = data_write.reshape(20,2)
        dataframes = pd.DataFrame({"mssv":list_np_mssv,"diem":list_np_diem_sv_raw})
        filename_out = "outpandas/" + filename_raw +"_grades"+".txt"
        dataframes.to_csv(filename_out,header=None,index=None)
    except:
        print("loi")
if __name__ == '__main__':
    normal()
    usage_pandas_and_numpy()
