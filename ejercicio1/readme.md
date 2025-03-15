
@sara9559ojeda ➜ /workspaces/PracticaCompiladores/ejercicio1 (main) $ echo "a=10; b=5+a2; c=(b-3)/2;" | java -cp ".:$ANTLR_JAR" org.antlr.v4.gui.TestRig MiGramatica programa -tokens [@0,0:0='a',,1:0] [@1,1:1='=',<'='>,1:1] [@2,2:3='10',,1:2] [@3,4:4=';',<';'>,1:4] [@4,6:6='b',,1:6] [@5,7:7='=',<'='>,1:7] [@6,8:8='5',,1:8] [@7,9:9='+',<'+'>,1:9] [@8,10:10='a',,1:10] [@9,11:11='',<'*'>,1:11] [@10,12:12='2',,1:12] [@11,13:13=';',<';'>,1:13] [@12,15:15='c',,1:15] [@13,16:16='=',<'='>,1:16] [@14,17:17='(',<'('>,1:17] [@15,18:18='b',,1:18] [@16,19:19='-',<'-'>,1:19] [@17,20:20='3',,1:20] [@18,21:21=')',<')'>,1:21] [@19,22:22='/',<'/'>,1:22] [@20,23:23='2',,1:23] [@21,24:24=';',<';'>,1:24] [@22,26:25='',,2:0]
Analisis Lexico
@sara9559ojeda ➜ /workspaces/PracticaCompiladores/ejercicio1 (main) $ echo "a=10; b=5+a*2; c=(b-3)/2;" | java -cp ".:$ANTLR_JAR" org.antlr.v4.gui.TestRig MiGramatica programa -tree (programa (expresion a = (expresion 10)) ; (expresion (expresion b = (expresion 5)) + (expresion (expresion a) * (expresion 2))) ; (expresion (expresion c = (expresion ( (expresion (expresion b) - (expresion 3)) ))) / (expresion 2)) ;)
PREGUNTAS
1. b
2. d
3. d