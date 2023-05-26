import csv

filename = 'theory_ex_flooding.csv'

def get_data_from_csv():
    p_axis = []
    d_zero_msg_2_expected_axis = []
    d_zero_msg_5_expected_axis = []
    with open(filename, newline='') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      for row in reader:
        p_axis.append(float(row[0]))
        d_zero_msg_2_expected_axis.append(float(row[1]))
        d_zero_msg_5_expected_axis.append(float(row[2]))
    return p_axis, d_zero_msg_2_expected_axis, d_zero_msg_5_expected_axis
