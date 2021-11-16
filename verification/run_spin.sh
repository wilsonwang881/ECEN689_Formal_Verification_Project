spin -a main.pml
gcc -DVECTORSZ=2048 -o model pan.c
./model