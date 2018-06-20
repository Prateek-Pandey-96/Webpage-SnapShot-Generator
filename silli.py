# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 23:04:39 2018

@author: Prateek
"""
from selenium import webdriver
import math
import tempfile
import os
import requests
from PIL import *

chrome_path=r"C:\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

url="https://www.flipkart.com/espoir-lcs-8016-day-date-functioning-best-quality-watch-men/p/itmf3zhzkk3pby2g?pid=WATF3UYXBYFYGDFW&lid=LSTWATF3UYXBYFYGDFW3E3JV0&marketplace=FLIPKART&srno=b_1_1&otracker=hp_omu_Deals%20of%20the%20Day_1_Under%E2%82%B9999%2BExtra5%25Off_YZ5K5WFO9QTJ_0&fm=neo/merchandising&iid=00bc372a-d94b-431c-b5b3-5e94f6dfdcba.WATF3UYXBYFYGDFW.SEARCH&ppt=Store%20Browse&ppn=Store&ssid=oypl06ema80000001529405728005"
output_path='G:/scraping amazon/62.png'




def save_fullpage_screenshot(driver, url, output_path, tmp_prefix='selenium_screenshot', tmp_suffix='.png'):
    """
    Creates a full page screenshot using a selenium driver by scrolling and taking multiple screenshots,
    and stitching them into a single image.
    """
 
    # get the page
    driver.get(url)
 
    # get dimensions
    window_height = driver.execute_script('return window.innerHeight')
    scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    num = int( math.ceil( float(scroll_height) / float(window_height) ) )
 
    # get temp files
    tempfiles = []
    for i in range( 0,num ):
        fd,path = tempfile.mkstemp(prefix='{0}-{1:02}-'.format(tmp_prefix, i+1), suffix=tmp_suffix)
        os.close(fd)
        tempfiles.append(path)
        pass
 
    try:
        # take screenshots
        for i,path in enumerate(tempfiles):
            if i > 0:
                driver.execute_script( 'window.scrollBy(%d,%d)' % (0, window_height) )
             
            driver.save_screenshot(path)
            pass
         
        # stitch images together
        stiched = None
        for i,path in enumerate(tempfiles):
            img = Image.open(path)
             
            w, h = img.size
            y = i * window_height
             
            if i == ( len(tempfiles) - 1 ):
                img = img.crop((0, h-(scroll_height % h), w, h))
                w, h = img.size
                pass
             
            if stiched is None:
                stiched = Image.new('RGB', (w, scroll_height))
             
            stiched.paste(img, (
                0, # x0
                y, # y0
                w, # x1
                y + h # y1
            ))
            pass
        stiched.save(output_path)
    finally:
        # cleanup
        for path in tempfiles:
            if os.path.isfile(path):
                os.remove(path)
        pass
 
    return output_path


save_fullpage_screenshot(driver,url,output_path)





# =============================================================================
# //////////////////////////////////////////////////////////////////////////////////////////////////////
# =============================================================================



