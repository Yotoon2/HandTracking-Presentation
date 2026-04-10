# Mini script pour rotater des images

for photo in *.jpg; do
  base="${photo%.jpg}"
  convert "$photo" -rotate 90  "${base}_rot90.jpg"
  convert "$photo" -rotate 180 "${base}_rot180.jpg"
  convert "$photo" -rotate 270 "${base}_rot270.jpg"
done