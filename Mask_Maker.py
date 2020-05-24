"""
This is a Python 3 program to build optical gratings or masks to be \
professionally printed on 35mm slides.

Usage: python mask_maker.py

Date: 2020-05-24

For tutorial & doc visit:
    https://www.erellaz.com

Documentation:
For making slides, page size and dpi are not relevant. Film recorders only use 
the pixel information.
In 2020, the maximum definition of standard professional recorders is 
8192x5462 pixels. The ratio is 8192/5462=1.499

Slides are either 22.5 x 33.75 standard, or 24 x 36, both ratios are 1.5.

Slide recorders should accept PNG, which is lossless compressed.
"""
#______________________________________________________________________________

from PIL import Image, ImageDraw
import os

imagesizepixels=(8192,5462) # max pixel resolution of professional standard recorders
slidesize=(36,24)# slide size
outputdir=r"D:\masks"

white=(255, 255, 255)
black=(0, 0, 0)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)


#______________________________________________________________________________
# Make color Schlieren gratings 
# Warning: when the LPI is such the line width in number of pixel divded by 3
# is not an integer, the green line is extended to adjust.
# lpi is the number of lines per inches
slide_in_inches=slidesize[1]/25.4
for lpi in range(10,280,20): #lpi start, lpi end, lpi step
    #Convert LPI to pixel
    nbr_lines=int(lpi*slide_in_inches)
    line_width_pixel=int(imagesizepixels[1]/(2*nbr_lines))
    npfilename=os.path.join(outputdir,"Schlieren_"+str(lpi)+"lpi.png")
    im = Image.new('RGB',imagesizepixels,green)
    draw = ImageDraw.Draw(im)
    alpmm=(nbr_lines+1)/slidesize[1]
    alpi=alpmm*25.4
    print("Desired LPI:",lpi," yields ",nbr_lines+1,"lines of width ", line_width_pixel, "pixels. Actual lpi:",alpi,"Lines per mm:",alpmm)
    
    #for i in range(nbr_lines+1): # draw horizontal lines
    i=0
    line_pos=int(line_width_pixel/2)
    while (line_pos<imagesizepixels[1]):
        line_pos=i*2*line_width_pixel+int(line_width_pixel/2)
        i+=1
        draw.line((0,line_pos,imagesizepixels[0],line_pos), fill=black, width=line_width_pixel)
        color_line_width_pixel=int(line_width_pixel/3)
        line_pos=line_pos+int(line_width_pixel/2+color_line_width_pixel/2)
        draw.line((0,line_pos,imagesizepixels[0],line_pos), fill=red, width=color_line_width_pixel)
        line_pos=line_pos+color_line_width_pixel
        draw.line((0,line_pos,imagesizepixels[0],line_pos), fill=blue, width=color_line_width_pixel)
        line_pos=line_pos+color_line_width_pixel
        draw.line((0,line_pos,imagesizepixels[0],line_pos), fill=green, width=color_line_width_pixel)
        
    im.save(npfilename)

#______________________________________________________________________________
# Make pinhole
pixel_in_micron=slidesize[1]*1000/imagesizepixels[1]
center_x=int(imagesizepixels[0]/2)
center_y=int(imagesizepixels[1]/2)
for radius_micron in range(50,1050,100): #slit size in Micron
    im = Image.new('RGB',imagesizepixels,black)
    draw = ImageDraw.Draw(im)
    radius_pixel=int((imagesizepixels[1]*radius_micron)/(1000*slidesize[1]))
    print("Desired slit size:",radius_micron," yields ",radius_pixel, "pixels. Actual pinhole size:",radius_pixel*pixel_in_micron,"microns, ",radius_pixel*pixel_in_micron/(1000*25.4),"inches")
    draw.ellipse((center_x-radius_pixel,center_y-radius_pixel,center_x+radius_pixel,center_y+radius_pixel), fill=white, outline=white)
    npfilename=os.path.join(outputdir,"Pin_Hole_"+str(radius_micron)+"micron.png") 
    im.save(npfilename)
#______________________________________________________________________________
# Make slit
pixel_in_micron=slidesize[1]*1000/imagesizepixels[1]
center_y=int(imagesizepixels[1]/2)
for slit_micron in range(100,2100,100): #slit size in Micron
    im = Image.new('RGB',imagesizepixels,black)
    draw = ImageDraw.Draw(im)
    slitpixel=int((imagesizepixels[1]*slit_micron)/(1000*slidesize[1]))
    print("Desired slit size:",slit_micron," yields ",slitpixel, "pixels. Actual slit size:",slitpixel*pixel_in_micron,"microns, ",slitpixel*pixel_in_micron/(1000*25.4),"inches")
    draw.line((0,center_y,imagesizepixels[0],center_y), fill=white, width=slitpixel)
    npfilename=os.path.join(outputdir,"Slit_"+str(slit_micron)+"micron.png") 
    im.save(npfilename)

    
#______________________________________________________________________________
# Make some Ronchi gratings 
# lpi is the number of lines per inches
slide_in_inches=slidesize[1]/25.4
for lpi in range(10,280,20): #lpi start, lpi end, lpi step
    #Convert LPI to pixel
    nbr_lines=int(lpi*slide_in_inches)
    line_width_pixel=int(imagesizepixels[1]/(2*nbr_lines))
    npfilename=os.path.join(outputdir,"Ronchi_"+str(lpi)+"lpi.png")
    im = Image.new('RGB',imagesizepixels,white)
    draw = ImageDraw.Draw(im)
    alpmm=(nbr_lines+1)/slidesize[1]
    alpi=alpmm*25.4
    print("Desired LPI:",lpi," yields ",nbr_lines+1,"lines of width ", line_width_pixel, "pixels. Actual lpi:",alpi,"Lines per mm:",alpmm)
    
    #for i in range(nbr_lines+1): # draw horizontal lines
    i=0
    line_pos=int(line_width_pixel/2)
    while (line_pos<imagesizepixels[1]):
        line_pos=i*2*line_width_pixel+int(line_width_pixel/2)
        i+=1
        draw.line((0,line_pos,imagesizepixels[0],line_pos), fill=black, width=line_width_pixel)
        
    im.save(npfilename)
    
