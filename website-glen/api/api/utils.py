import os, glob
#DEVELOPMENT
file_path = 'api/api/tmp/' 
#PRODUCTION
#file_path = 'api/tmp/'


# A function that returns the highest entry cookie for the result_id "id". 
# NOTE: This function is only ever called AFTER cookie_exists, so we assume a cookie does exist.
# INPUTS: id - the result id we want to find a cookie for
# OUTPUTS: integer - the maximum cookie found. If it is -1, the process has failed, if it is > 1, the process is still working
# OUTPUTS: boolean - if there are no cookies, the function will return false.
def get_max_cookie(id):
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