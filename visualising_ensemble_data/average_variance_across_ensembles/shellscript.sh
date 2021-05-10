echo ffmpeg -f image2 -start_number 24 -framerate $1 -y -i $2 -c:v copy $3
ffmpeg -f image2 -start_number 24 -framerate $1 -y -i $2 -c:v copy $3 

# ffmpeg -f image2 -start_number 24 -r 24 -i max_%02d.png max.avi