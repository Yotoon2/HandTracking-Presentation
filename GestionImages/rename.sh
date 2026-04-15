# Mini rename des photos

for photo in *.jpg; do
  base="${photo%.jpg}"
  convert "$photo" -rotate 0  "${base}_ncw.jpg"
  rm "$photo"
done
