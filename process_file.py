# this is here due to the smaller pies having issues with
# some version requirments, need to create an virtual env
# for plotting on the pies
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    imported_work = True
except Exception as ex:
    imported_work = False

import datetime

# takes a line vector from a file
# and strips the white space from all elements
def clean_vec(linevec):
    ret_l = list()
    for e in linevec:
        if e != ' ' and e != '':
            e = e.strip(" ")
            ret_l.append(e)
    return ret_l

# new_df = pd.DataFrame(process_file("log_file.txt"))
# new_df = process_file("log_file.txt")
if imported_work:
    # will open a file produced from a ps command and
    # convert it into a dataframe
    def process_file(filename, ):
        f = open(filename, 'r')
        lines = f.readlines()
        cnt = 0
        ret_df = {}
        # go through the lines of the file
        for line in lines:
            # clean of surrounding whites space
            # and split on spaces
            linevec = line.strip().split(" ")

            # clean the elements from the line vector of surrounding white
            # space
            linevec = clean_vec(linevec)

            # if this is an even row
            if cnt%2 == 0:
                # if this is the first row grab the column names
                if cnt == 0:
                    cols = linevec
                    for i in range(len(cols)):
                        ret_df[cols[i]] = []
            else:  # for an odd row grab the data
                if linevec[0] == "PID":
                    break
                else:
                    for i in range(len(cols)):
                        if cols[i] in ["RSS", "VSZ", "%CPU", "%MEM"]:
                            ret_df[cols[i]].append(float(linevec[i]))
                        elif cols[i] == "ELAPSED":
                            ret_df[cols[i]].append(datetime.datetime.strptime(linevec[i], '%M:%S'))
                        else:
                            ret_df[cols[i]].append(linevec[i])
                cnt += 1
                
        return ret_df


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
else:
    def show_result(**kwargs):
        print("could not do needed import.....")
        return

    def process_file(**kwargs):
        pass
        
