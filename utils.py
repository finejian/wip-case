import datetime

__formater_mdy_hm = r"%d/%m/%Y %H:%M"
__formater_dmy_hm = r"%m/%d/%Y %H:%M"
__formater_ymd_hm = r"%Y/%m/%d %H:%M"

def formatDatetime(dt):
    dts = dt.split("/")
    if len(dts) != 3:
        return ""

    dt = dt[:16]
    if len(dts[0]) <= 2:
        try:
            return datetime.datetime.strptime(dt, __formater_mdy_hm).strftime(__formater_ymd_hm)
        except:
            return datetime.datetime.strptime(dt, __formater_dmy_hm).strftime(__formater_ymd_hm)

    # 2018/02/27
    return datetime.datetime.strptime(dt, __formater_ymd_hm).strftime(__formater_ymd_hm)

def __test():
    print(formatDatetime("22/05/2018 15:09"))
    print(formatDatetime("02/02/2017 16:54"))
    print(formatDatetime("2017/01/02 16:54"))
    print(formatDatetime("2017/01/02 16:54:12"))
    print(formatDatetime("05/22/2018 02:54 PM"))


if __name__ == '__main__':
    __test()
