import os, glob

# A function that returns the highest entry cookie for the result_id "id". 
# NOTE: This function is only ever called AFTER cookie_exists, so we assume a cookie does exist.
# INPUTS: id - the result id we want to find a cookie for
# OUTPUTS: integer - the maximum cookie found. If it is -1, the process has failed, if it is > 1, the process is still working
# OUTPUTS: boolean - if there are no cookies, the function will return false.
def get_max_cookie(file_path, id):
    cookies = glob.glob(os.path.abspath(file_path + id + "_cookie_*"))
    if cookies: # True unless there are no cookies
        max_cookie = 0
        for cookie in cookies:
            if "-1" in cookie:
                return -1
            cookie = int(cookie.split("cookie_")[1])
            if cookie > max_cookie:
                max_cookie = cookie
        return max_cookie
    else:
        return False

def get_cookie_info(file_path, id, current_cookie):
    try:
        current_cookie = os.path.abspath(file_path + id + "_cookie_" + str(current_cookie))
        f = open(current_cookie, 'r')
        cookie_info = f.read()
        f.close()
    except:
        print("Cookie: " + current_cookie + " could not be found.")
        return False
    # If the file is blank, this will return an empty string, which acts as "False" for the calling function
    print(" ".join(cookie_info.split()))
    return cookie_info

def cleanup_cookies(file_path, id):
    cookies = glob.glob(os.path.abspath(file_path + id + "_cookie_*"))
    for cookie in cookies:
        try:
            os.remove(cookie)
        except:
            print("Error while removing cookie: " + cookie)

# This function adds the groupfile name to the end of each header of a fasta file
# It is intended to be used to combine multiple fasta files into one large one, separated by their groups
# It also creates the groupfile.txt file.
def save_fasta_file(file_path, file, id, group_name):
    #save the file using the built in Flask method, so we can read it using python methods
    print(file_path)
    file.save(file_path + id + "tmp" + ".fa")

    read_file = open(file_path + id + "tmp" + ".fa" , 'r')
    write_file = open(file_path + id + '.fa', 'a+')
    group_file = open(file_path + id + '_groupfile.tsv', 'a+')
    
    # if the last line we wrote was a protein sequence, then we need to write a newline character before writing the next
    # header
    newline = False 
    for line in read_file.readlines():
        if ">" in line:
            write_file.write(">" + group_name + "_" + line[1:])
            #for the groupfile we want to replace the \n with a tab
            if newline:
                group_file.write('\n')
                newline=False
            group_file.write(">" + group_name + "_" + line.rstrip('\n')[1:] + "\t" + group_name)

        else:
            write_file.write(line)
            #for the groupfile we want the entire protein sequence to be on one line
            newline = True
    group_file.write("\n")
    read_file.close()
    write_file.close()
    group_file.close()

    #delete the temporary read-only file
    os.remove(file_path + id + "tmp" + ".fa")