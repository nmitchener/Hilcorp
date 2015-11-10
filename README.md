# Hilcorp
Hilcorp correlation project

Pyhton script that transforms data from this format:

```
tagname_1  TS_1  value
tagname_2  TS_1  value
tagname_3  TS_1  value  
.........  ...   .....
tagname_N  TS_1  value
.........  ...   .....
tagname_1  TS_N  value
tagname_2  TS_N  value
.........  ...   .....
```

------------------------------------>into this format:

```
tagname_1  TS_1  value
tagname_1  TS_2  value
........   ...   ......
tagname_1  TS_N  value
tagname_2  TS_1  value
tagname_2  TS_2  value
........   ...   ......
tagname_2  TS_N  value
........   ...   ......
```
