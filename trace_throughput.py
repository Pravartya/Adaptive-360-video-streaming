# -*- coding: utf-8 -*-
"""trace-throughput.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jxKrIoTZeHniAvapki0V8hZCdWTTMEPA
"""

!pip install beautifulsoup4

!pip install html5lib

!pip install requests

import requests

url = 'https://reference.dashif.org/dash.js/nightly/samples/dash-if-reference-player/index.html?mpd=https%3A%2F%2Fdash.akamaized.net%2Fakamai%2Fbbb_30fps%2Fbbb_30fps.mpd&loop=true&autoPlay=true&drmToday=false&forceQualitySwitchSelected=false&drmPrioritiesEnabled=false&languageAudio=null&roleVideo=null&languageText=null&roleText=undefined&forceTextStreaming=false&debug.logLevel=4&debug.dispatchEvent=false&streaming.abandonLoadTimeout=10000&streaming.wallclockTimeUpdateInterval=100&streaming.manifestUpdateRetryInterval=100&streaming.cacheInitSegments=false&streaming.applyServiceDescription=true&streaming.eventControllerRefreshDelay=150&streaming.capabilities.filterUnsupportedEssentialProperties=true&streaming.capabilities.useMediaCapabilitiesApi=false&streaming.timeShiftBuffer.calcFromSegmentTimeline=false&streaming.timeShiftBuffer.fallbackToSegmentTimeline=true&streaming.metrics.maxListDepth=100&streaming.delay.liveDelayFragmentCount=NaN&streaming.delay.liveDelay=NaN&streaming.delay.useSuggestedPresentationDelay=true&streaming.protection.keepProtectionMediaKeys=false&streaming.protection.ignoreEmeEncryptedEvent=false&streaming.buffer.enableSeekDecorrelationFix=false&streaming.buffer.fastSwitchEnabled=true&streaming.buffer.flushBufferAtTrackSwitch=false&streaming.buffer.reuseExistingSourceBuffers=true&streaming.buffer.bufferPruningInterval=10&streaming.buffer.bufferToKeep=20&streaming.buffer.bufferTimeAtTopQuality=30&streaming.buffer.bufferTimeAtTopQualityLongForm=60&streaming.buffer.initialBufferLevel=NaN&streaming.buffer.stableBufferTime=12&streaming.buffer.longFormContentDurationThreshold=600&streaming.buffer.stallThreshold=0.3&streaming.buffer.useAppendWindow=true&streaming.buffer.setStallState=true&streaming.gaps.jumpGaps=true&streaming.gaps.jumpLargeGaps=true&streaming.gaps.smallGapLimit=1.5&streaming.gaps.threshold=0.3&streaming.gaps.enableSeekFix=true&streaming.utcSynchronization.enabled=true&streaming.utcSynchronization.useManifestDateHeaderTimeSource=true&streaming.utcSynchronization.backgroundAttempts=2&streaming.utcSynchronization.timeBetweenSyncAttempts=30&streaming.utcSynchronization.maximumTimeBetweenSyncAttempts=600&streaming.utcSynchronization.minimumTimeBetweenSyncAttempts=2&streaming.utcSynchronization.timeBetweenSyncAttemptsAdjustmentFactor=2&streaming.utcSynchronization.maximumAllowedDrift=100&streaming.utcSynchronization.enableBackgroundSyncAfterSegmentDownloadError=true&streaming.utcSynchronization.defaultTimingSource.scheme=urn%3Ampeg%3Adash%3Autc%3Ahttp-xsdate%3A2014&streaming.utcSynchronization.defaultTimingSource.value=https%3A%2F%2Ftime.akamai.com%2F%3Fiso%26ms&streaming.scheduling.defaultTimeout=500&streaming.scheduling.lowLatencyTimeout=0&streaming.scheduling.scheduleWhilePaused=true&streaming.text.defaultEnabled=true&streaming.liveCatchup.maxDrift=NaN&streaming.liveCatchup.playbackRate=NaN&streaming.liveCatchup.playbackBufferMin=0.5&streaming.liveCatchup.enabled=null&streaming.liveCatchup.latencyThreshold=60&streaming.liveCatchup.mode=liveCatchupModeDefault&streaming.lastBitrateCachingInfo.enabled=true&streaming.lastBitrateCachingInfo.ttl=360000&streaming.lastMediaSettingsCachingInfo.enabled=true&streaming.lastMediaSettingsCachingInfo.ttl=360000&streaming.cacheLoadThresholds.video=50&streaming.cacheLoadThresholds.audio=5&streaming.trackSwitchMode.audio=alwaysReplace&streaming.trackSwitchMode.video=neverReplace&streaming.selectionModeForInitialTrack=highestSelectionPriority&streaming.fragmentRequestTimeout=10000&streaming.retryIntervals.MPD=500&streaming.retryIntervals.XLinkExpansion=500&streaming.retryIntervals.MediaSegment=1000&streaming.retryIntervals.InitializationSegment=1000&streaming.retryIntervals.BitstreamSwitchingSegment=1000&streaming.retryIntervals.IndexSegment=1000&streaming.retryIntervals.FragmentInfoSegment=1000&streaming.retryIntervals.license=1000&streaming.retryIntervals.other=1000&streaming.retryIntervals.lowLatencyReductionFactor=10&streaming.retryAttempts.MPD=3&streaming.retryAttempts.XLinkExpansion=1&streaming.retryAttempts.MediaSegment=3&streaming.retryAttempts.InitializationSegment=3&streaming.retryAttempts.BitstreamSwitchingSegment=3&streaming.retryAttempts.IndexSegment=3&streaming.retryAttempts.FragmentInfoSegment=3&streaming.retryAttempts.license=3&streaming.retryAttempts.other=3&streaming.retryAttempts.lowLatencyMultiplyFactor=5&streaming.abr.movingAverageMethod=slidingWindow&streaming.abr.ABRStrategy=abrDynamic&streaming.abr.additionalAbrRules.insufficientBufferRule=true&streaming.abr.additionalAbrRules.switchHistoryRule=true&streaming.abr.additionalAbrRules.droppedFramesRule=true&streaming.abr.additionalAbrRules.abandonRequestsRule=false&streaming.abr.bandwidthSafetyFactor=0.9&streaming.abr.useDefaultABRRules=true&streaming.abr.useDeadTimeLatency=true&streaming.abr.limitBitrateByPortal=false&streaming.abr.usePixelRatioInLimitBitrateByPortal=false&streaming.abr.maxBitrate.audio=-1&streaming.abr.maxBitrate.video=-1&streaming.abr.minBitrate.audio=-1&streaming.abr.minBitrate.video=-1&streaming.abr.maxRepresentationRatio.audio=1&streaming.abr.maxRepresentationRatio.video=1&streaming.abr.initialBitrate.audio=-1&streaming.abr.initialBitrate.video=-1&streaming.abr.initialRepresentationRatio.audio=-1&streaming.abr.initialRepresentationRatio.video=-1&streaming.abr.autoSwitchBitrate.audio=true&streaming.abr.autoSwitchBitrate.video=true&streaming.abr.fetchThroughputCalculationMode=abrFetchThroughputCalculationMoofParsing&streaming.cmcd.enabled=false&streaming.cmcd.sid=null&streaming.cmcd.cid=null&streaming.cmcd.rtp=null&streaming.cmcd.rtpSafetyFactor=5&streaming.cmcd.mode=query&errors.recoverAttempts.mediaErrorDecode=5'
r = requests.get(url)

import requests 
from bs4 import BeautifulSoup 
    
def getdata(url): 
    r = requests.get(url) 
    return r.text 
    
htmldata = getdata(url) 
soup = BeautifulSoup(htmldata, 'html.parser') 
for item in soup.find_all('img'):
    print(1)

!pip install selenium

!pip install webdriver-manager



# driver = webdriver.Chrome('/kaggle/input/drivers/chromedriver')

!apt-get update

!apt install chromium-chromedriver -y

!cp /usr/lib/chromium-browser/chromedriver /usr/bin



import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("window-size=1200x600")



driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.maximize_window()

chrome_options

driver

driver.get("https://reference.dashif.org/dash.js/nightly/samples/dash-if-reference-player/index.html")

# driver.find_element_by_name("btnK").send_keys(Keys.ENTER)  
# time.sleep(3)

text_box = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div[1]/input')
print("Element is visible? " + str(text_box.is_displayed()))

button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[1]/input')))

driver.implicitly_wait(20)
text_box = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div[1]/input')
print("Element is visible? " + str(text_box.is_displayed()))

from selenium.webdriver.common.action_chains import ActionChains
text_box = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div[1]/input')
driver.implicitly_wait(10)
ActionChains(driver).move_to_element(text_box).send_keys("https://github.com/Pravartya/MTP-2/blob/main/new%20original%20mpd/myvideo.mpd").perform()
time.sleep(3)

import time
but_clk = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div[1]/span/button[3]')
driver.implicitly_wait(10)
ActionChains(driver).move_to_element(but_clk).click(but_clk).perform()

# l.text

# l.text.split(' | ')[2]

# l = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/div[4]/div/div[1]/div/div[1]")
l = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/div[4]/div/div[1]/div/div[7]")
l.text.split(' | ')

start_time = time.time()
end_time = start_time + 29
cur_time = start_time
prev_time = cur_time-1

# (cur_time -start_time , end_time-start_time)

download_time = []
l = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/div[4]/div/div[1]/div/div[7]")
while(cur_time  < end_time):

    if cur_time >= prev_time + 1:
#         print(prev_time - start_time)
        prev_time = cur_time
        try:
            download_time.append( l.text.split(' | ')[1] )
        except:
            print("skip")
            ;
    cur_time = time.time()
download_time

# Commented out IPython magic to ensure Python compatibility.
def connect_server():
    import os
    import pathlib
    
    path = path = (str(pathlib.Path().parent.resolve())).split('/')
    if "MTP-2" not in path and "MTP-2" not in os.listdir("."):
        os.system("git clone https://github.com/Pravartya/MTP-2.git")
    if "MTP-2" not in path:
#         %cd MTP-2
    os.system("ls")
    os.system("git config --global user.email 'harishdewangan7@gmail.com'")
    os.system("git config --global user.name 'Pravartya'")







# Commented out IPython magic to ensure Python compatibility.
# %%time
# connect_server()

!ls

import os

os.system("ls")

# Commented out IPython magic to ensure Python compatibility.
# %cd new original mpd

len(download_time)

!ls

import os
import numpy as np

throughput = []
# for i in range(0, len(download_time)):

chunk_size = []
for i in range(0, 9):

    size = os.path.getsize(f'\'1_00{1+i}\'.m4s')
    chunk_size.append(size)
    throughput.append(size / float(download_time[i]))
for i in range(9, len(download_time)):

    size = os.path.getsize(f'\'1_0{1+i}\'.m4s')
    chunk_size.append(size)
    throughput.append(size / float(download_time[i]))
throughput

len(throughput)

from PIL import Image
import matplotlib.pyplot as plt
target_ = np.array(throughput)
#     pred_ = np.array(pred_)
target = target_ + 0
# pred = pred_ + 0
x = range(len(target))
plt.rcParams.update({'font.size': 20})
plt.rcParams.update({'xtick.labelsize': 20})
plt.rcParams.update({'ytick.labelsize': 20})

if len(target) < 200:
    x_len = 20
elif len(target) < 400:
    x_len = 30
else:
    x_len = 40
fig, ax = plt.subplots(figsize=(x_len, 10), dpi=80)
ax.xaxis.label.set_size(30)
ax.yaxis.label.set_size(30)

plt.xlabel("Chunk No")
plt.ylabel("Throughput (bits/secs)")


# conf interval
#     ci = 1.5 * np.std(target)/np.mean(target)
ci = 0.05 * np.std(target)/np.mean(np.abs(target))
ax.plot(x,target, 'b', label='Throughput')
#     ax.plot(x,pred, 'r', label='Predicted QoE')
ax.fill_between(x, (target-ci), (target+ci), color='b', alpha=.1)
ax.legend(loc='upper right', fontsize=20)

fig.savefig('Throughput.png', dpi=100)



!ls

# Commented out IPython magic to ensure Python compatibility.
# %cd new original mpd

throughput

chunk_size

# pathlib.Path('web_mpd').parent.resolve()

# import pathlib
    
# path = (str(pathlib.Path('web_mpd').resolve())).split('/')
# path

# !ls

# file_list = os.listdir(".")
# file_list

# file_list = os.listdir(".")
# if ~('traces' in file_list):
#     os.system("mkdir 'traces'")
# !ls

# %cd traces

import matplotlib.pyplot as plt
plt.ylim([0,5])
plt.plot(throughput)
plt.show()







dat = {'throughput' : list(throughput)}
# my_file.write(dat)
dat['throughput'] = str(dat['throughput'])
import json
f_name = f'throughput.jason'
f = open(f_name,  "w")
json.dump(dat, f)

dat = {'chunk_size' : list(chunk_size)}
# my_file.write(dat)
dat['chunk_size'] = str(dat['chunk_size'])
import json
f_name = f'chunk_size.jason'
f = open(f_name,  "w")
json.dump(dat, f)

dat['throughput']

dat['chunk_size']











