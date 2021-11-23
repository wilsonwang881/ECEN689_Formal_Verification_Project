spin -a main.pml
gcc -DVECTORSZ=6000 -o model pan.c
./model