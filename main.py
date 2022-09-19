import pandas as pd
import threading

from utils.utils import *

if __name__ == '__main__':
    
    n = int(input('Enter Number of user to be scraped (enter -1 to scrap all significant users): '))
    threads = int(input('Enter number of threads : '))

    scroll_thread = threading.Thread(target=scroll_down,args=(n,))
    scrap_threads = [threading.Thread(target=scrap_data,args=(i,threads,n)) for i in range(threads)]
    
    scroll_thread.start()
    for i in scrap_threads:
        i.start()
    
    scroll_thread.join()
    for i in scrap_threads:
        i.join()

    df = pd.DataFrame(user_data)
    df.sort_values(by='user_rank',inplace=True)
    df.to_csv('./data.csv',index = False)
    
    print('Done')