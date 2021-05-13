echo ffmpeg -f image2 -start_number 24 -framerate $1 -y -i $2 -c:v copy $3
ffmpeg -f image2 -start_number 24 -framerate $1 -y -i $2 -c:v copy $3
# ffmpeg -f image2 -start_number 24 -framerate $1 -y -i $2 -c:v mpeg4 $3
# -pix_fmt yuv420p

# ffmpeg -f image2 -start_number 24 -r 8 -y -i bob01/max_%02d.png -c:v copy max.avi



