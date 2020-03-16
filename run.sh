for j in 20 30 40 50 60 70
do
  echo "max =  $j"
  for i in 1 2 3 4 5
    do
       echo "    Welcome to the round $i"
       python SubMassive.py $j 3 $i > "$j$i".logbook
    done
done
