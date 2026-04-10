# Mini rename des photos

for photo in *.jpg; do
  base="${photo%.jpg}"
  convert "$photo" -rotate 0  "${base}_raav.jpg"
  rm "$photo"
done
