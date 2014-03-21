# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 13:32:22 2014

@author: stuart
"""
import bz2

import requests
import progressbar

def download(url, filename):
    CHUNK_SIZE = 1024 * 1024 # 1MB

    #Open file and get total size
    r = requests.get(url, stream=True)
    total_size = int(r.headers['content-length'])
    #Create a progressbar
    print "Downloading data:"
    pbar = progressbar.ProgressBar(widgets=[progressbar.Percentage(), progressbar.Bar()], maxval=total_size).start()
    pos = 0
    #Open the file and read and decompress chunk by chunk:
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
            f.write(chunk)
            #position is len of downloaded file
            pos += len(chunk)
            pbar.update(pos)
    pbar.finish()

def download_unbzip(url, filename):
    CHUNK_SIZE = 1024 * 1024 # 1MB

    #Open file and get total size
    r = requests.get(url, stream=True)
    total_size = int(r.headers['content-length'])
    #Create a progressbar
    print "Downloading and decompressing data:"
    pbar = progressbar.ProgressBar(widgets=[progressbar.Percentage(), progressbar.Bar()], maxval=total_size).start()
    #Create a stream bz2 decompressor
    bz = bz2.BZ2Decompressor()
    #Initial postition of file is 0
    pos = 0
    #Open the file and read and decompress chunk by chunk:
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
            f.write(bz.decompress(chunk))
            #position is len of downloaded (compressed) file
            pos += len(chunk)
            pbar.update(pos)
    pbar.finish()


#Download the files
download('http://files.figshare.com/1425846/gband_image_00200.fits', 'data/gband_image_00200.fits')
download('http://files.figshare.com/1425877/Fieldline_surface_Slog_p30_0_A20r2_r60__B005_00400.vtp', 'data/Fieldline_surface_Slog_p30-0_A20r2_r60__B005_00400.vtp')
download_unbzip('http://cadair.com/Slog_p30-0_A20r2_B005_00400.gdf.bz2', 'data/Slog_p30-0_A20r2_B005_00400.gdf')
