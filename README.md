```
Usage: python3 .\game_of_life.py {-s|--size} <SIZE> [PATTERN]
Play Conway's Game of Life.
Example: 'python3 .\game_of_life.py -r -s 10'

        -s, --size <SIZE>               set the size of the board

Pattern Options:
        -r, --rand                      populate the board with random cells
        -l, --load [FILE]               load pattern from file
        --bee                           stable beehive pattern
        --blinker                       oscillating blinker
        --pulsar                        oscillating pulsar
        --glider                        glider spaceship
```


#Examples:

##Bee Hive Pattern
```
[ ][X][X][ ]
[X][ ][ ][X]
[ ][X][X][ ]
```

##Blinker Pattern:
```
[ ][ ][ ]    	[ ][x][ ]
[X][X][X]  =>	[ ][X][ ] 
[ ][ ][ ]    	[ ][X][ ]
```
