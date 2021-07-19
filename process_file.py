# import pandas as pd
#import matplotlib.pyplot as plt
import datetime
def clean_vec(linevec):
    ret_l = list()
    for e in linevec:
        if e != ' ' and e != '':
            e = e.strip(" ")
            ret_l.append(e)
    return ret_l


def process_file(filename, ):
    f = open(filename, 'r')
    lines = f.readlines()
    cnt = 0
    ret_df = {}
    for line in lines:
        linevec = line.strip().split(" ")
        linevec = clean_vec(linevec)
        if cnt%2 == 0:
            if cnt == 0:
                cols = linevec
                for i in range(len(cols)):
                    ret_df[cols[i]] = []
        else:
            for i in range(len(cols)):
                if cols[i] != 'TIME':
                    ret_df[cols[i]].append(float(linevec[i]))
                else:
                    ret_df[cols[i]].append(datetime.datetime.strptime(linevec[i], '%H:%M:%S'))
        cnt += 1
                
    return ret_df


# new_df = pd.DataFrame(process_file("log_file.txt"))
# new_df = process_file("log_file.txt")

"""
def show_result(new_df, title='', figsize=(10, 20)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    ax.plot(list(range(len(new_df['RSS']))), new_df['RSS'], label='RSS', color='r')
    ax.plot(list(range(len(new_df['VSZ']))), new_df['VSZ'],label='VSZ', color='g')
    ax.set_xlabel('sample')
    ax.set_ylabel('Memory in MiB')
    ax.set_title(title)
    ax.legend()

    plt.show()
"""
