set ITEMS;
/* set of items as "ItemX" */

param n integer;
/* number of items */

param c integer;
/* capacity at each second */

param l{i in ITEMS} integer;
/* value of each item */

param d{i in ITEMS} integer;
/* weight of each item */

param s{i in ITEMS} integer;
/* starting second of each item */

param t{i in ITEMS} integer;
/* final second of each activity */

param s_min := min{i in ITEMS} s[i];
/* initial second of the instance */

param s_max := max{i in ITEMS} t[i];
/* final second of the instance */

var X{i in ITEMS} binary;
/* 1 if item i has been selected and 0 otherwise */

var Y{i in ITEMS, j in s_min..s_max} binary;
/* 1 if the item i is selected and uses the second j; 0  otherwise */

maximize profit: sum{i in ITEMS} X[i]*l[i];
/* our goal is to maximize the profit */

s.t. SEC{i in ITEMS, j in s[i]..t[i]}: X[i] <= Y[i,j];
/* this guarantees that Yij will be 1 iff Xi is active and uses the second j */ 

s.t. CAP{j in s_min..s_max}: sum{i in ITEMS} Y[i,j]*d[i] <= c;
/* for each second, the sum of all items selected at that second cant exceed our cap c */ 

end;
