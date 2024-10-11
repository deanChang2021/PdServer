import os,sys,logging

from PdBaseKits.tools.DataTools import DateTools

def setupLogger(task):
    st = DateTools()

    logPath =""

    if "win32" in sys.platform or "win64" in sys.platform:
        logPath="c:/portunid/task/log"
    else:
        logPath="/Users/admin/portunid/log"

    if not os.path.isdir(logPath):
        os.makedirs(logPath)


    date = st.getCurrDate()
    fileName = logPath+"/"+task+date+".log"

    logging.basicConfig(filename=fileName, level=logging.DEBUG, format='[%(filename)s:%(lineno)d][%(asctime)s][%(levelname)s] %(message)s')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.info("系统开始启动")