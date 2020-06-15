#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#**************************************************
# 2020 text normalisation Python3 Lib, Prof. Charlotte Schubert Alte Geschichte, Leipzig


'''
DEF: A text normalization is everything done to equalize encoding, appearance 
and composition of a sequence of signs called a text. There are two goals of 
normalization. The first is a common ground of signs  and the second is a 
reduction of differences between two sequences of signs.  Not every 
normalization step is useful for every comparison task! Remember: 
Sometimes it is important to not equalize word forms and 
sometimes it is important. 
GPLv3 copyrigth
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http:#www.gnu.org/licenses/>.
'''
 
'''PYTHON3'''

import unicodedata, re

#globals
false = False
true = True
doUVlatin = false; 
analysisNormalform = "NFKD";
dispnormalform = "NFC";

notprivalpha = [];#["ἀΐω"];
#"de" Akzente richtig, oder falsch????
listofelusion = { "δ᾽":"δὲ","δ'":"δὲ", "ἀλλ’": "ἀλλά", "ἀνθ’": "ἀντί", "ἀπ’": "ἀπό", "ἀφ’": "ἀπό","γ’": "γε","γένοιτ’": "γένοιτο","δ’": "δέ","δι’": "διά","δύναιτ’": "δύναιτο","εἶτ’": "εἶτα","ἐπ’": "ἐπί","ἔτ’": "ἔτι","ἐφ’": "ἐπί","ἡγοῖντ’": "ἡγοῖντο","ἵν’": "ἵνα","καθ’": "κατά","κατ’": "κατά","μ’": "με","μεθ’": "μετά","μετ’": "μετά","μηδ’": "μηδέ","μήδ’": "μηδέ","ὅτ’": "ὅτε","οὐδ’": "οὐδέ","πάνθ’": "πάντα","πάντ’": "πάντα","παρ’": "παρά","ποτ’": "ποτε","σ’": "σε","ταῦθ’": "ταῦτα","ταῦτ’": "ταῦτα","τοῦτ’": "τοῦτο","ὑπ’": "ὑπό","ὑφ’": "ὑπό"}
satzzeichen = [".", ";", ",", ":", "!", "?", "·", ")", "("]
#original abschrift, Klammerbehandlungfließtext
#Inschriften Klammersystem
#https:#apps.timwhitlock.info/js/regex#
lueckeBestimmt = re.compile( r"\[[Ͱ-Ͼἀ-῾|◌̣ ]+\]" ) #l0
lueckeinZeile = re.compile( r"\[\-\-\-\]" ) #klasse l1
lueckeinZeile2 = re.compile( r"\[3\]" ) #lueckeinZeile, klasse l1
lueckeausZeile = re.compile( r"\[\-\-\-\-\-\-\]" ) #klasse l2
lueckeausZeile2 = re.compile( r"\[6\]" ) #Luecke im Umfang einer Zeile, Klasse l2
lueckeunbest = re.compile( r"\]\[" ) # Klasse l3

zeilenende = re.compile( r" \/ " ) # Klasse l4
zeilenendeDigit = re.compile( r" \/ \d+ " ) # Klasse l4
zeilenanfang = re.compile( r" \| " ) # Zeilenanfang, Klasse l5
zeilenanfangDigit = re.compile( r" \| \d+ " ) # Zeilenanfang, Klasse l5
aufabk = re.compile( r"\(\)" )  #Auflösung von Abkürzungen, Klasse l6
beschaedigt = re.compile( r"\[nurbuchstabenoderleer\]" ) #beschädigt oder undeutlich, klasse l7
getilgt = re.compile( r"\{\}" ) # Tilgung, Klasse l8
rasiert = re.compile( r"\[\[\]\]" ) #Rasur, Klasse l9
ueberschr = re.compile( r"\<\<\>\>" ) # Überschrieben, Klasse l10
tilgrewrite = re.compile( r"\<\<\[\[\]\]\>\>" ) #Tilgung Wiedereinfügung, Klasse l11
punktunter = "◌̣ "; #Punkt unter Buchstaben - Buchstabe nur Teilweise erhalten -- später, Klasse l12
anzgriechbuch = re.compile( r" \.+ " ) #Anzahl unbestimmabrer griechischen Bustaben, Klasse l13
anzlatbuchs = re.compile( r" \++ " )  #Anzahl unbestimmbarer römsicher Buchstaben, Klasse l14
korrdeseditors = re.compile( r"\<\>" ) #Korrektur des Editors, Klasse l15
#**************************************************
# Section 000
# basic UNICODE NORMAL FORM 
#**************************************************
def setAnaFormTO( fnew ):
    analysisNormalform = fnew

def setDisplFormTO( fnew ):
    dispnormalform = fnew

def normarrayk( aarray ):
	replacearray = {};
	for p in aarray:
		replacearray[ disambiguDIAkritika( unicodedata.normalize( analysisNormalform, p ) ) ] = aarray[ p ];
	return replacearray;

#def normatextwordbyword( text, wichnorm ):
#    spt = text.split( " " )
#    lele = len( spt )
#    for w in range( lele ):
#        nw = normatext( spt[ w ], wichnorm )
#        spt[ w ] = nw
#    return " ".join( spt )


def normatext( text, wichnorm ):
    spt = text.split( " " )
    for w in range( len( spt ) ):
        nw = sameuninorm( spt[ w ], wichnorm )
        spt[ w ] = nw;
    return " ".join( spt )

# def takes sting and normalform string (for example "NFD")
def sameuninorm( aword, wichnorm ):
    return unicodedata.normalize( wichnorm, aword ) 

vokaleGRI = {"ι":1,"υ":1,"ε":1,"ο":1,"α":1,"ω":1,"η":1}
buchstGRI = {"Α":"A", "α":"a", "Β":"B", "β":"b", "Γ":"G", "γ":"g", "Δ":"D", "δ":"d", "Ε":"E", "ε":"e", "Ζ":"Z", "ζ":"z", "Η":"H", "η":"h", "Θ":"Th", "θ":"th", "Ι":"I", "ι":"i", "Κ": "K", "κ":"k", "Λ":"L", "λ":"l", "Μ":"M", "μ":"m", "Ν":"N", "ν":"n", "Ξ":"Xi", "ξ":"xi", "Ο":"O", "ο":"o", "Π":"P", "π":"p", "Ρ":"R", "ρ":"r", "Σ":"S", "σ":"s", "ς":"s", "Τ":"T", "τ":"t", "Υ":"U", "υ":"u", "Φ":"Ph", "φ":"ph", "Χ":"X", "χ":"x", "Ψ":"Ps", "ψ":"ps", "Ω":"O", "ω":"o"}
buchstLAT = {"d":1, "g":1, "p":1, "t":1, "c":1, "k":1, "q":1, "qu":1, "ph":1, "th":1, "ch":1, "x":1, "z":1, "f":1, "v":1, "s":1, "m":1, "n":1, "l":1, "r":1, "a":1,"i":2,"e":3,"o":4,"u":5,"v":6, "y":7}
groups = {"γγ":["n", "g"], "γκ":["n", "c"], "γξ":["n","x"], "γχ":["n", "ch"], "ηυ":["ē", "u"]}; #only great letters??????? what is with that?
behauchung = { "῾":"h" };
buchsCoptic = {"ϐ": "B", "ϑ":"Th", "ϱ":"r", "ϰ":"k", "ϒ":"y", "ϕ":"ph", "ϖ":"p", "Ϝ":"W", "ϝ":"w", "Ϙ":"Q","ϙ":"q", "Ϟ":"ḳ", "ϟ":"ḳ", "Ϲ":"S", "Ⲥ":"S", "ⲥ":"s", "ϲ":"s", "Ͻ":"S", "ͻ":"s","Ϳ ":"j","ϳ":"j","Ͱ":"h","ͱ":"h","Ⲁ":"A","ⲁ":"a", 
"ϴ":"t","Ⲑ":"t","ⲑ":"t","ϵ":"e","϶":"e","Ϸ":"Sh","ϸ":"sh", "ϼ":"P","Ϡ":"S","ϡ":"S","Ⳁ":"S","ⳁ":"s",
"Ͳ":"Ss", "ͳ":"ss", "Ϻ":"S","ϻ":"s", "Ϣ":"š","ϣ":"š", "Ϥ":"F","ϥ":"f", "Ϧ":"X", "Ⳉ":"X",
"ϧ":"x","ⳉ":"x", "Ϩ":"H", "ϩ":"h", "Ϫ":"J", "ϫ":"j", "Ϭ":"C","ϭ":"c","Ϯ":"Di","ϯ":"di", 
"Ͼ":"S", "Ͽ":"S", "ͼ":"s", "ͽ":"s", "Ⲃ":"B","ⲃ":"b","Ⲅ":"G","ⲅ":"g", "Ⲇ":"D", "ⲇ":"d", "Ⲉ":"E", "ⲉ":"e", 
"Ⲋ":"St", "ⲋ":"st", "Ⲍ":"Z", "ⲍ":"z", "Ⲏ":"ê", "ⲏ":"ê", "Ⲓ":"I", "ⲓ":"i", "Ⲕ":"K", "ⲕ":"k", 
"Ⲗ":"L", "ⲗ":"l", "Ⲙ":"M", "ⲙ":"m", "Ⲛ":"N","ⲛ":"n", "Ⲝ":"ks", "ⲝ":"ks", "Ⲟ	":"O", "ⲟ":"o", 
"Ⲡ":"B", "ⲡ":"b", "Ⲣ":"R","ⲣ":"r", "Ⲧ":"T", "ⲧ":"t", "Ⲩ":"U", "ⲩ":"u", "Ⲫ":"F","ⲫ":"f","Ⲭ":"Kh", "ⲭ":"kh",
"Ⲯ":"Ps", "ⲯ":"ps", "Ⲱ":"ô", "ⲱ":"ô", "Ͷ":"W", "ͷ":"w"}; # 

spai1 = re.compile( "\u2002".encode("utf-8").decode("utf-8") );#enspacing
spai2 = re.compile( "\u2000".encode("utf-8").decode("utf-8") );#enquad
def sameallspacing( astr ):
    astr = re.sub( spai1, ' ', astr)
    astr = re.sub( spai2, ' ', astr)
    return astr

def disambiguDIAkritika( astr ):
    astr = "\u2019".join( astr.split( "\u0027" ) ) #typogra korrektes postroph;
    astr = "\u2019".join( astr.split( "'" ) )
    astr = "\u2019".join( astr.split( "\u1FBD" ) )
    return astr

def disambiguadashes( astring ):
    astring = re.sub( cleangeviert, '-', astring)
    astring = re.sub( cleanhalbgeviert, '-', astring)
    astring = re.sub( cleanziffbreitergeviert, '-', astring)
    astring = re.sub( cleanviertelgeviert, '-', astring)
    astring = re.sub( cleanklgeviert, '-', astring)
    astring = re.sub( cleanklbindstrichkurz, '-', astring)
    astring = re.sub( cleanklbindstrichvollbreit, '-', astring)
    return astring

def ExtractDiafromBuchst( buchst ):
    toitter = list( unicodedata.normalize( "NFKD", buchst ) );
    b = [];
    d = [];
    for t in range( len( toitter ) ):
        co =  toitter[t].lower( );
        if( co in buchstGRI or co in buchsCoptic or co in buchstLAT ):
            b.append( toitter[t] );
        else:
            d.append( toitter[t] );
    return ["".join( d ), "".join( b )];

def ExtractDiafromBuchstText( atext ):
    t = ""
    spli = atext.split( " " )
    lspli = len( spli )
    for i in range( lspli ):
        t +=  "[ "+", ".join( ExtractDiafromBuchst( spli[ i ] ) )+" ]"
    return t

def replaceBehauchung( adiakstring ):
    if( "῾" in adiakstring ):
        return "h"+adiakstring.replace( "῾","" );
    else:
        return adiakstring;

def Expandelision( aword ):
    if( aword in  listofelusion ):
        return listofelusion[ aword ]
    else:
        return aword
    

def ExpandelisionText( atext ):
    t = "";
    wds = atext.split( " " )
    lwds = len( wds )
    for w in range( lwds): 
        t += " "+ Expandelision(  wds[ w ] )
    return t

def TraslitAncientGreekLatin( astring ):
    wordlevel = delligaturen( unicodedata.normalize( "NFC", iotasubiotoad( unicodedata.normalize( "NFD" , astring.strip() ) ) ) ).split(" "); #care for iotasubscriptum, Ligature
    #de δ’ !!!
    romanized = [];
    for w in range( len( wordlevel ) ):
        buchstlevel = list( wordlevel[ w ] );
        grouped = [];
        notlastdone = true;
        extractedida2 = "";
        extracteBUCHST2 = "";
        for b in range( 1, len( buchstlevel ) ):
            if( buchstlevel[ b-1 ] == "" ):
                continue;
            
            zwischenerg1 = ExtractDiafromBuchst( buchstlevel[ b-1 ] );
            zwischenerg2 = ExtractDiafromBuchst( buchstlevel[ b ] );
            extractedida1 = zwischenerg1[0];
            extractedida2 = zwischenerg2[0];
            extracteBUCHST1 = zwischenerg1[1];
            extracteBUCHST2 = zwischenerg2[1];
            if( extracteBUCHST1+extracteBUCHST2 in groups and not "¨" in extractedida2 ): #wenn kein trema über dem zweiten buchstaben - diaresis keine Zusammenziehung (synresis)
                gou = groups[ extracteBUCHST1+extracteBUCHST2 ];
                grouped.append( unicodedata.normalize( "NFC", gou[0]+replaceBehauchung(extractedida1)+gou[1]+replaceBehauchung(extractedida2) ) )
                buchstlevel[ b ] = "";#dealread in groupand revistible
                notlastdone = false;
            else:
                if( extracteBUCHST1 in buchstGRI ):
                    grouped.append( unicodedata.normalize( "NFC", buchstGRI[extracteBUCHST1]+replaceBehauchung(extractedida1) ) )
                else:
                    if( extracteBUCHST1 in buchsCoptic ):
                        grouped.append( unicodedata.normalize( "NFC", buchsCoptic[extracteBUCHST1]+replaceBehauchung(extractedida1) ) )
                    else:
                        #realy not - leave IT
                        grouped.append( buchstlevel[ b-1 ] );
                notlastdone = true;
        if( notlastdone ):
            if( extracteBUCHST2 in buchstGRI ):
                grouped.append( unicodedata.normalize( "NFC", buchstGRI[extracteBUCHST2]+replaceBehauchung(extractedida2) ) ) 
            else:
                if( extracteBUCHST2 in buchsCoptic ):
                    grouped.append( unicodedata.normalize( "NFC", buchsCoptic[extracteBUCHST2]+replaceBehauchung(extractedida2) ) ) 
                else:
                    #realy not - leave IT
                    grouped.append( buchstlevel[ len( buchstlevel )-1 ] );
        romanized.append( "".join( grouped ) );
    return " ".join( romanized );  

#**************************************************
# Section 00
# basic cleaning and string conversion via regexp 
#**************************************************

cleanhtmltags = re.compile( r"<.*?>" );
cleanhtmlformat1 = re.compile( '&nbsp;' )
regEbr1 = re.compile( "<br/>" ); 
regEbr2 = re.compile( "<br>" )
cleanNEWL = re.compile( '\\n' )
cleanRETL = re.compile( '\\r' )
cleanstrangehochpunkt =re.compile( r'‧' )
cleanthisbinde =re.compile( r'—' )
cleanthisleer =re.compile( '\xa0'.encode("utf-8").decode("utf-8") ) #byte string is not allowed - 
cleanleerpunkt =re.compile( r' \.' )
cleanleerdoppelpunkt =re.compile( r' :' )
cleanleerkoma =re.compile( r' ,' )
cleanleersemik =re.compile( r' ;' )
cleanleerausrufe =re.compile( r' !' )
cleanleerfrege =re.compile( r' \?' )

# breakdown typographic letiances "Bindestriche und Geviertstriche"
cleanklbindstrichvollbreit =re.compile( r'－' )
cleanklbindstrichkurz =re.compile( r'﹣' )
cleanklgeviert =re.compile( r'﹘' )
cleanviertelgeviert =re.compile( r'‐' )
cleanziffbreitergeviert =re.compile( r'‒' )
cleanhalbgeviert =re.compile( r'–' )
cleangeviert =re.compile( r'—' )

escspitzeL =re.compile( r'<' )
escspitzeR =re.compile( r'>' )

def spitzeklammernHTML( astr ):
    astr = re.sub( escspitzeL, '&lt;', astr )
    astr = re.sub( escspitzeR, '&gt;', astr )
    return astr


def basClean( astring ):
    astring = re.sub( cleanNEWL, " <br/>", astring )
    astring = re.sub( cleanRETL, " <br/>", astring)
    astring = re.sub( cleanstrangehochpunkt,"·", astring)
    astring = re.sub( cleanthisbinde," — ", astring)
    astring = re.sub( cleanthisleer, ' ', astring)
    astring = re.sub( cleanleerpunkt, '.', astring)
    astring = re.sub( cleanleerdoppelpunkt, ':', astring)
    astring = re.sub( cleanleerkoma, ',', astring)
    astring = re.sub( cleanleersemik, ';', astring)
    astring = re.sub( cleanleerausrufe, '!', astring)
    astring = re.sub( cleanleerfrege, '?', astring)
    astring = disambiguadashes( astring )

    # remove hyphens
    ws = astring.split(" ");
    ca = [];
    halfw = "";
    secondhalf = "";
    for w in range( len( ws ) ):
        if( "-" in ws[w] ):
            h = ws[w].split( "-" );
            halfw = h[0].replace(" ", "");
            secondhalf = h[1].replace(" ", "");
            if( "]" in secondhalf ): 
                hh = h[1].split("]");
                if( len( hh[1] ) > 1 ):
                    ca.append( halfw + hh[1] + " " + hh[0] + "]<br/>" );
                    halfw = "";
                    secondhalf = "";
        elif( "<br/>" != ws[w] and ws[w] != "" and ws[w] != " " and halfw != "" ):
            if( "]" in ws[w] ):
                secondhalf = ws[w].replace(" ", "");
            else:
                ca.append( halfw + ws[w].replace("<br/>", "") + " " + secondhalf + "<br/>" ); #trennstriche
                halfw = "";
                secondhalf = "";
        else:
            if( ws[w] != "" ): #remove mehrfache leerstellen
                ca.append( ws[w] );
    return " ".join( ca );


def ohnesatzzeichen( wliste ):
    lsatzz = len( satzzeichen )
    lwdl = len( wliste )
    for sa in range( lsatzz ):
        for w in range( lwdl ):
            wliste[ w ] = "".join( wliste[ w ].split( satzzeichen[ sa ]))
    return wliste;

def replaceOPENINGandCLOSING( astopen, astclose, strstr):
    no = strstr.split( astclose )
    NO = ""
    for n in no:
        NO += n.split( astopen )[0]
    return NO

#usage: replaceWordsfromarray( ["in", "cum", "et", "a", "ut"], stringggg )
def replaceWordsfromarray( arr, replacement,strstr ):
    for a in arr:
        strstr = strstr.replace( arr[a], replacement )
    return strstr

#**************************************************
# Section 0
# word leve conversions: 
# alpha privativum
# alpha copulativum
# Klammersysteme editorische
#**************************************************
def hasKEY( alist, thekey ): #fkt should move
    if( thekey in alist ):
        return True
    else:
        return False

def AlphaPrivativumCopulativum( aword ):
    if( not aword in notprivalpha ):
        buchs = list( delall( aword ) )
        if( len( buchs ) == 0 ):
            return aword
        if( buchs[0] == "α" ): #erste Buchstabe alpha
            if( hasKEY( vokaleGRI , buchs[1] ) ): # zweiter ein Vokal
                b2dia = ExtractDiafromBuchst(aword[1])[0]
                #console.log("lll",b2dia)
                if( "\u0308" in  b2dia ): #zweiter Buchstabe mit Trema, erste Buchstabe mit spiritus lenis
                    return aword[0] +" "+ aword[1:] 
                else:
                    return aword
            else:
                return aword
        else:
            return aword
    else:
        return aword
def AlphaPrivativumCopulativumText( atext ):
    t = ""
    spli = atext.split( " " )
    lspli = len( spli )
    for l in range( lspli ):
        #print(spli[ l ], AlphaPrivativumCopulativum( spli[ l ] ) )
        t += " "+AlphaPrivativumCopulativum( spli[ l ] )    
    return t

def testprivatalpha():
    #drittes Beispiel müsste raus genommen werden
    bsp = ["ἀϊδής", "ἀΐδιος", "ἀΐω", "ἀΐσθω", "ἀΐλιος", "Ἅιδης", "ἀϊών", "αἰών", "ἀΐσσω", "ἀΐδηλος", "ἀΐζηλος", "ἀΐσδηλος", "ἄϊδρις", "ἀϊστόω", "ἀΐσυλος", "αἴσῠλος", "ἄϋλος", "αὐλός", "ἀϊών", "αἰών", ];
    Strout = "";
    for b in range( len( bsp ) ):
        Strout += "Eingabe "+ bsp[ b ]+ " Ausgabe "+ AlphaPrivativumCopulativum( bsp[b] ) +"\n";    
    print( Strout )


#**************************************************
# Section 1 
# unicode related comparing and norming, handling of diacritics
#**************************************************

# array of unicode diacritics (relevant for polytonic greek)
diacriticsunicodeRegExp = [ 
	re.compile('\u0313'.encode("utf-8").decode("utf-8") ), 
	re.compile("\u0314".encode("utf-8").decode("utf-8") ), 
	re.compile("\u0300".encode("utf-8").decode("utf-8") ), 
	re.compile("\u0301".encode("utf-8").decode("utf-8")), 
	re.compile("\u00B4".encode("utf-8").decode("utf-8")), 
	re.compile("\u02CA".encode("utf-8").decode("utf-8")), 
	re.compile("\u02B9".encode("utf-8").decode("utf-8")), 
	re.compile("\u0342".encode("utf-8").decode("utf-8")), 
	re.compile("\u0308".encode("utf-8").decode("utf-8")), 
	re.compile("\u0304".encode("utf-8").decode("utf-8")), 
	re.compile("\u0306".encode("utf-8").decode("utf-8")) ]

# def takes string, splits it with jota subscriptum and joins the string again using jota adscriptum
regJotaSub = re.compile( '\u0345'.encode("utf-8").decode("utf-8") )
def iotasubiotoad( aword ):
 	return "ι".join( aword.split( u'\u0345' ) );

# def takes "one word"
def ohnediakritW( aword ):
    for dia in range( len( diacriticsunicodeRegExp ) ):
        aword = re.sub( diacriticsunicodeRegExp[ dia ], "", aword )
    return aword

def capitali( astring ):
    return astring.capitalize();

# precompiled regular expressions
strClean1 = re.compile( r'’' )
strClean2 = re.compile( r'\'' )
strClean3 = re.compile( r'᾽' )
strClean4 = re.compile( r'´' )

# def takes a string replaces some signs with regexp and oth
def nodiakinword( aword ):
    aword = re.sub(strClean1, "", aword)
    aword = re.sub(strClean2, "", aword)
    aword = re.sub(strClean3, "", aword)
    aword = re.sub(strClean4, "", aword)
    spt = unicodedata.normalize( analysisNormalform, aword )
    return iotasubiotoad( ohnediakritW( spt ) )

#**************************************************
# Section 2: deleting things that could be not same in two texts
#**************************************************

# def take a string and deletes diacritical signes, ligatures, remaining interpunction, line breaks, capital letters to small ones, equalizes sigma at the end of greek words, and removes brakets
def delall( text ):
    if( doUVlatin ): # convert u to v in classical latin text
        text = deluv( delklammern( sigmaistgleich( delgrkl( delligaturen( delinterp( delmakup( delumbrbine( delnumbering( delunknown( deldiak(  text)))))))))))
    else:
        text = delklammern( sigmaistgleich( delgrkl( delligaturen( delinterp( delmakup( delumbrbine( delnumbering( delunknown( deldiak(  text  ) ) ) ) ) ) ) )))
    return text

#del numbering
numeringReg1 = re.compile( r'\[([0-9\.\:\; ]+)\]' )
numeringReg2 = re.compile( r'\[[M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})]+\]' )
numeringReg3 = re.compile( r'\(([A-Za-z0-9\.\:\; ]+|([0-9\.\:\; ]+))\)' ) #runde klammern mit zahlen und buchstaben
     
def delnumbering( text ): #untested
    text = re.sub( numeringReg1, "", text)
    text = re.sub( numeringReg2, "", text)
    text = re.sub( numeringReg3, "", text)
    return text


# precompiled regular expressions of the relevant ligatures 
regEstigma = re.compile( '\u03DA'.encode("utf-8").decode("utf-8") ) 
regEstigmakl = re.compile( '\u03DB'.encode("utf-8").decode("utf-8") )
regEomikonyplsi = re.compile( r'ȣ' )
regEomikonyplsiK = re.compile( r'Ȣ' )
regEUk = re.compile( r'Ꙋ' )
regEuk = re.compile( r'ꙋ' )
regEkai = re.compile( r'ϗ' )
regEKai = re.compile( r'Ϗ' )
regEl1 = re.compile( '\u0223'.encode("utf-8").decode("utf-8") )
regEl2 = re.compile( '\u0222'.encode("utf-8").decode("utf-8") )
regEl3 = re.compile( '\u03DB'.encode("utf-8").decode("utf-8") )
# def take a string and replaces all occorences of a regular expression
def delligaturen( text ):
    text = re.sub( regEstigma, "στ", text)
    text = re.sub( regEstigmakl, "στ", text)
    text = re.sub( regEUk, "Υκ", text)
    text = re.sub( regEuk, "υκ", text)
    text = re.sub( regEomikonyplsi, "ου", text)
    text = re.sub( regEomikonyplsiK, "ου", text)
    text = re.sub( regEkai, "καὶ", text)
    text = re.sub( regEKai, "Καὶ", text)
    text = re.sub( regEl1, "\u039F\u03C5".encode("utf-8").decode("utf-8"), text)
    text = re.sub( regEl2, "\u03BF\u03C5".encode("utf-8").decode("utf-8"), text)
    text = re.sub( regEl3, "\u03C3\u03C4".encode("utf-8").decode("utf-8"), text);
    return text

# def takes string and splits it into words, than normalizes each word, joins the string again
def deldiak( text ):
    spt = text.split( " " ); #seperate words
    for wi in range( len( spt ) ):
        spt[ wi ] = nodiakinword( spt[ wi ] );
    return  " ".join( spt );

regEdoppelP = re.compile( r':' )
regEeinfahP = re.compile( r'\.' )
regEkomma = re.compile( r',' )
regEsemiK = re.compile( r';' )
regEhochP = re.compile( r'·' )
regEausr = re.compile( r'!' )
regEfarge = re.compile( r'\\?' )
regEan1 = re.compile( r'“' )
regEan5 = re.compile( r'„' )
regEan2 = re.compile( r'”' )
regEan3 = re.compile( r'"' )
regEan4 = re.compile( r"'" )
regpipe = re.compile( r"|" )
# def takes a string and replaces interpunction
def delinterp( text ):
    text = re.sub(regEdoppelP, "", text)
    text = re.sub(regEeinfahP, "", text)
    text = re.sub(regEkomma, "", text)
    text = re.sub(regEsemiK, "", text)
    text = re.sub(regEhochP, "", text)
    text = re.sub(regEausr, "", text)
    text = re.sub(regEfarge, "", text)
    text = re.sub(regEan1, "", text)
    text = re.sub(regEan2, "", text)
    text = re.sub(regEan3, "", text)
    text = re.sub(regEan4, "", text)
    text = re.sub(regEan5, "", text)
    text = re.sub(regpipe, "", text)
    return text

# function takes a string and replaces some unknown signs
regU1 = re.compile( r"†" )
regU2 = re.compile( r"\*" )
regU3 = re.compile( r"⋖" )
regU4 = re.compile( r"#" ) 
def delunknown( text ):
    text = re.sub(regU1, "", text)
    text = re.sub(regU2, "", text)
    text = re.sub(regU3, "", text)
    text = re.sub(regU4, "", text)
    return text

# def takes string and replace html line breakes
def delumbrbine( text ):
    text = re.sub(regEbr1, "", text)
    text = re.sub(regEbr2, "", text)
    return text

def umbrtospace( text ):
    text = re.sub(cleanNEWL, " ", text)
    text = re.sub(cleanRETL, " ", text)
    text = re.sub(regEbr1, " ", text)
    text = re.sub(regEbr2, " ", text);
    return text

# first version, a little more...
def delmakup( text ):
    text = re.sub(cleanhtmltags, "", text)
    text = re.sub(cleanhtmlformat1, "", text)
    return text
# ...
def delgrkl( text ):
    return text.lower();

# def takes string and converts tailing sigma to inline sigma (greek lang)
regEtailingsig = re.compile( r"ς" )
def sigmaistgleich( text ):
    return re.sub(regEtailingsig, "σ", text);

regEkla1 = re.compile( r"\(" )
regEkla2 = re.compile( r"\)" )
regEkla3 = re.compile( r"\{" )
regEkla4 = re.compile( r"\}" )
regEkla5 = re.compile( r"\[" )
regEkla6 = re.compile( r"\]" )
regEkla7 = re.compile( r"<" )
regEkla8 = re.compile( r">" )
regEkla9 = re.compile( r"⌈" )
regEkla10 = re.compile( r"⌉" )
regEkla11 = re.compile( r"‹" )
regEkla12 = re.compile( r"›" )
regEkla13 = re.compile( r"«" )
regEkla14 = re.compile( r"»" )
regEkla15 = re.compile( r"⟦" )
regEkla16 = re.compile( r"⟧" )
regEkla17 = re.compile( '\u3008'.encode("utf-8").decode("utf-8") )
regEkla18 = re.compile( '\u3009'.encode("utf-8").decode("utf-8") )
regEkla19 = re.compile( '\u2329'.encode("utf-8").decode("utf-8") )
regEkla20 = re.compile( '\u232A'.encode("utf-8").decode("utf-8") )
regEkla21 = re.compile( '\u27E8'.encode("utf-8").decode("utf-8") )
regEkla22 = re.compile( '\u27E9'.encode("utf-8").decode("utf-8") )

# def take sstring and replaces the brakets

def delklammern( text ):
    text = re.sub(regEkla1, "",text)
    text = re.sub(regEkla2, "",text)
    text = re.sub(regEkla3, "",text)
    text = re.sub(regEkla4,"",text)
    text = re.sub(regEkla5,"",text)
    text = re.sub(regEkla6,"",text)
    text = re.sub(regEkla7,"",text)
    text = re.sub(regEkla8,"",text)
    text = re.sub(regEkla9,"",text)
    text = re.sub(regEkla10,"",text)
    text = re.sub(regEkla11,"",text)
    text = re.sub(regEkla12,"",text)
    text = re.sub(regEkla13,"",text)
    text = re.sub(regEkla14,"",text)
    text = re.sub(regEkla15,"",text)
    text = re.sub(regEkla16,"",text)
    text = re.sub(regEkla17,"",text)
    text = re.sub(regEkla18,"",text)
    text = re.sub(regEkla19,"",text)
    text = re.sub(regEkla20,"",text)
    text = re.sub(regEkla21,"",text)
    text = re.sub(regEkla22,"",text);
    return text

def deledklammern( text ):
    text = re.sub(regEkla1, "",text)
    text = re.sub(regEkla2, "",text)
    text = re.sub(regEkla3, "",text)
    text = re.sub(regEkla4,"",text)
    text = re.sub(regEkla5,"",text)
    text = re.sub(regEkla6,"",text)
    text = re.sub(regEkla9,"",text)
    text = re.sub(regEkla10,"",text)
    text = re.sub(regEkla11,"",text)
    text = re.sub(regEkla12,"",text)
    text = re.sub(regEkla13,"",text)
    text = re.sub(regEkla14,"",text)
    text = re.sub(regEkla15,"",text)
    text = re.sub(regEkla16,"",text)
    text = re.sub(regEkla17,"",text)
    text = re.sub(regEkla18,"",text)
    text = re.sub(regEkla19,"",text)
    text = re.sub(regEkla20,"",text)
    text = re.sub(regEkla21,"",text)
    text = re.sub(regEkla22,"",text);
    return text

regEuv = re.compile( r"u" )
# def takes string and replaces u by v, used in classical latin texts
def deluv( text ):
    return re.sub( regEuv, "v", text );

def Trennstricheraus( wliste ): #\n version
    ersterteil = ""
    zweiterteil = ""
    neueWLISTE = []
    lele = len( wliste )
    for w in range( lele ):
        if( len( ersterteil ) == 0 ):
            if( "-" in wliste[ w ] ):
                eUNDz = wliste[ w ].split( "-" )
                if( len( eUNDz[1] ) > 0 ):
                    zweiohnenewline = eUNDz[1].split( "\n" )
                    neueWLISTE.append(eUNDz[0]+zweiohnenewline[len(zweiohnenewline)-1 ])
                else:
                    ersterteil = eUNDz[0]
                #print(eUNDz.length, eUNDz)
            else: #nix - normales wort
                neueWLISTE.append( wliste[ w ] )			
        else: # es gab eine Trennung und die ging über zwei Listenzellen
            if( not "[" in wliste[ w ] and not "]" in wliste[ w ] ):
                zweiteralsliste = wliste[ w ].split( "\n" )
                #print("split", zweiteralsliste, wliste[ w ], ersterteil+zweiteralsliste[ zweiteralsliste.length-1 ])
                neueWLISTE.append(ersterteil+zweiteralsliste[ len(zweiteralsliste)-1 ] )
                ersterteil = ""
            else: #klammern behandeln
                #wenn ich hier kein append auf der neune Wortliste mache, dann lösche ich damit die geklammerten sachen
                if( "[" in wliste[ w ] and "]" in wliste[ w ] ): #klammern in einem Wort
                    zweiteralsliste = wliste[ w ].split( "]" )
                    neueWLISTE.append( ersterteil+zweiteralsliste[1].substring(1, len(zweiteralsliste[1])-1) )
                    #print("NO SPLIT", ersterteil+zweiteralsliste[1].substring(1, zweiteralsliste[1].length-1))
                elif( "[" in wliste[ w ] ):
                    zweiteralsliste = wliste[ w ].split( "[" )
                    neueWLISTE.append( ersterteil+"".join( zweiteralsliste ) )
                else: #nur schließende Klammer
                    zweiteralsliste = wliste[ w ].split( "]" )
                    neueWLISTE.append( ersterteil+zweiteralsliste[1] )
                    #print("NO SPLIT", ersterteil+zweiteralsliste[1].substring(1, zweiteralsliste[1].length-1))
    if(ersterteil != "" and zweiterteil == "" ):
        neueWLISTE.append( ersterteil+"-" )
    return neueWLISTE


def Interpunktiongetrennt( wliste ):
    neuewliste = []
    for sa in range( len( satzzeichen ) ):
        for w in range( len( wliste ) ):
            if( satzzeichen[ sa ] in wliste[ w ] ):
                neuewliste.append( "".join( wliste[ w ].split( satzzeichen[ sa ] ) ) )
                neuewliste.append( satzzeichen[ sa ] )
            else:
                neuewliste.append(  wliste[ w ] )
        wliste = neuewliste
        neuewliste = []
    return wliste


def UmbruchzuLeerzeichen( atext ):
	return " ".join(  atext.split("\n") )

def iotasubiotoadL( wliste ):
    lwdl = len( wliste )
    for w in range( lwdl ):
        wliste[ w ] = iotasubiotoad( wliste[ w ] )	
    return wliste

#function to use with greek text maybe
def GRvorbereitungT( dtext ):
    diewo =  disambiguDIAkritika( unicodedata.normalize( analysisNormalform, delnumbering( dtext ) ).lower() ).split( " " )
    #diewo = iotasubiotoadL( diewo )
    diewo = UmbruchzuLeerzeichen( " ".join(Trennstricheraus( diewo ) ) ).split( " " )
    diewo = Interpunktiongetrennt( diewo )
    #diewo = Klammernbehandeln( diewo )
    return diewo

#******************************************************************************
# Section 3: edition klammerung
#******************************************************************************
def hervKLAMMSYS( stringtomani ): #RUN ON NFC/NFKC
    out = ""
    startindex = 0
    for m in re.finditer( lueckeBestimmt, stringtomani ):
        out += stringtomani[ startindex : m.start() ] + "<b>"+m.group(0)+"</b>"      
        startindex = m.end()+1
    out += stringtomani[ startindex : len(stringtomani) ]
    return out

def delKLAMMSYS( stringtomani ): #RUN ON NFC/NFKC
    out = ""
    startindex = 0
    for m in re.finditer( lueckeBestimmt, stringtomani ):
        out += stringtomani[ startindex : m.start() ]      
        startindex = m.end()+1
    out += stringtomani[ startindex : len(stringtomani) ]
    return out

# USAGE
def demUsage( ):

    atesttext = "„[IX]” ⁙ ἀλλ’ ἑτέραν τινὰ φύσιν ἄπειρον', ἐξ ἧς ἅπαντας γίνεσθαι τοὺς οὐρανοὺς καὶ τοὺς ἐν αὐτοῖς κόσμους· ἐξ ὧν δὲ ἡ γένεσίς ἐστι τοῖς οὖσι, καὶ τὴν φθορὰν εἰς ταῦτα γίνεσθαι κατὰ τὸ χρεών. διδόναι γὰρ αὐτὰ δίκην καὶ τίσιν ἀλλήλοις τῆς ἀδικίας κατὰ τὴν τοῦ χρόνου τάξιν, ποιητικωτέροις οὕτως ὀνόμασιν αὐτὰ λέγων· δῆλον δὲ ὅτι τὴν εἰς ἄλληλα μεταβολὴν τῶν τεττάρων στοιχείων οὗτος θεασάμενος οὐκ ἠξίωσεν ἕν τι τούτων ὑποκείμενον ποιῆσαι, ἀλλά τι ἄλλο παρὰ ταῦτα. οὗτος δὲ οὐκ ἀλλοιουμένου τοῦ στοιχείου τὴν γένεσιν ποιεῖ, ἀλλ’ ἀποκρινομένων τῶν ἐναντίων διὰ τῆς ἀιδίου κινή- σεως· 1 Summá pecúniae, quam dedit in [bla bla bla] aerarium vel plebei Romanae vel dimissis militibus=> denarium sexiens milliens. 2 Opera fecit nova § aedem Martis, Iovis Tonantis et Feretri, Apollinis, díví Iúli, § Quirini, § Minervae, Iunonis Reginae, Iovis Libertatis, Larum, deum Penátium, § Iuventatis, Matris deum, Lupercal, pulvinar ad [11] circum, § cúriam cum chalcidico, forum Augustum, basilicam 35 Iuliam, theatrum Marcelli, § porticus . . . . . . . . . . , nemus trans Tiberím Caesarum. § 3 Refécit Capitolium sacrasque aedes numero octoginta duas, theatrum Pompeí, aquarum rivos, viam Flaminiam.  Ϗ ϗ ϚϛȢȣꙊꙋἀἁἂἃἄἅἆἇἈἉἊἋἌἍἎἏἐἑἒἓἔἕἘἙἚἛἜἝἠἡἢἣἤἥἦἧἨἩἪἫἬἭἮἯἰἱἲἳἴἵἶἷἸἹἺἻἼἽἾἿὀὁὂὃὄὅὈὉὊὋὌὍὐὑὒὓὔὕὖὗὙὛὝὟὠὡὢὣὤὥὦὧὨὩὪὫὬὭὮὯὰάὲέὴήὶίὸόὺύὼώ	ᾀᾁᾂᾃᾄᾅᾆᾇᾈᾉᾊᾋᾌᾍᾎᾏᾐᾑᾒᾓᾔᾕᾖᾗᾘᾙᾚᾛᾜᾝᾞᾟᾠᾡᾢᾣᾤᾥᾦᾧᾨᾩᾪᾫᾬᾭᾮᾯᾰᾱᾲᾳᾴᾶᾷᾸᾹᾺΆᾼ᾽ι᾿῀῁ῂῃῄῆῇῈΈῊΉῌ῍῎῏ῐῑῒΐῖῗῘῙῚΊ῝῞῟ῠῡῢΰῤῥῦῧῨῩῪΎῬ῭΅`ῲῳῴῶῷῸΌῺΏῼ´῾ͰͱͲͳʹ͵Ͷͷͺͻͼͽ;Ϳ΄΅Ά·ΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϏϐϑϒϓϔϕϖϗϘϙϚϛϜϝϞϟϠϡϢϣϤϥϦϧϨϩϪϫϬϭϮϯϰϱϲϳϴϵ϶ϷϸϹϺϻϼϽϾϿ Αι αι γγ γκ γξ γχ ου Υι υι ἄϋλος αὐλός  τί φῄς; γραφὴν σέ τις, ὡς ἔοικε, γέγραπται οὐ γὰρ ἐκεῖνό γε καταγνώσομαι, ὡς σὺ ἕτερον. δ̣[ὲ κ]αὶ"
    
    ree =  "\033[33;2;47m" # Green Text
    defo = "\033[m" # reset to the defaults

    #latin
    doUVlatin = true; 
    print(ree+"Textinput 1:",defo)
    print( atesttext )
    
    #normed in analysis form
    testnorm = normatext( atesttext, analysisNormalform )
    
    disa = disambiguDIAkritika( testnorm )
    print( ree+"a) Disambuguation of diacritics (takes a string, replaces diakritica to have them equaly encoded, return string):" ,defo)
    print( disa )

    ex = ExtractDiafromBuchstText( testnorm )
    print( ree+"b) Separation of diakritics  (takes array of letters and returns array of array of diakritica and array of letters):" ,defo)
    print( ex )

    basicres =  basClean( atesttext )  
    print( ree+"c) Text output basic norm (basic equalization and hypenation reversal):" ,defo)
    print( basicres )

    translitbsp = TraslitAncientGreekLatin( basicres )
    print( ree+"d) Text transliteration (takes greek utf8 string and returns transliterated latin utf8 string):" ,defo)
    print( translitbsp ); 

    expeli = ExpandelisionText( testnorm )
    print( ree+"e) Elusion expansion (given a text, if this is an elusion it will be expanded):",defo)
    print( expeli )

    spiekla = spitzeklammernHTML( testnorm )
    print( ree+"f) Spitze Klammern zu html (escapes spitze klammern to html encoding):" ,defo)
    print( spiekla )

    al = AlphaPrivativumCopulativumText( atesttext ) #Normal form composed!!!
    print( ree+"g) Alpha privativum  / copulativum (takes utf8 greek and splits the alpha privativum and copulativum from wordforms):",defo)
    print( al )

    jo = iotasubiotoad( testnorm ) #Normal form composed!!!
    print( ree+"h) JOTA (takes greek utf8 string and repleces jota subscriptum with jota ad scriptum):",defo)
    print( jo )

    diakdelled = deldiak( basicres )
    print( ree+"i) Text output without diacritics (replaces diacritics):</b>" ,defo)
    print( diakdelled )

    numb = delnumbering( testnorm )
    print( ree+"j) Text output without numbering (takes string return string without the edition numbering i.e. [2]):" ,defo)
    print( numb )
    
    unk = delunknown( testnorm )
    print( ree+"k) Text output without some signs (delete some to the programmer unknown signs: †, *,⋖,#):" ,defo)
    print( unk )

    mark = delmakup( testnorm )
    print( ree+"l) Text output without markup (input a string and get it pack with markup removed):" ,defo)
    print( mark )

    interpdelled = delinterp( basicres )
    print( ree+"m) Text output without punctuation (takes string and returns the string without):" ,defo)
    print( interpdelled )

    ligdelled = delligaturen( basicres )
    print( ree+"n) Text output without ligature (takes a string return string with ligatures turned to single letters):" ,defo)
    print( ligdelled )

    umbrdelled = delumbrbine( basicres )
    print( ree+"o) Text output without newline (input string and get it back with linebreaks removed):" ,defo)
    print( umbrdelled )

    grkldelled = delgrkl( basicres )
    print( ree+"p) Text output equal case (input a string and get it bach with all small case letters):" ,defo)
    print( grkldelled )

    sidelled = sigmaistgleich( basicres )
    print( ree+"q) Text output tailing sigma uniform (equalize tailing sigma):" ,defo)
    print( sidelled )

    kladelled = delklammern( basicres )
    print( ree+"r) Text output no brackets (input stringa nd get it back with no brackets):" ,defo)
    print( kladelled )

    uvdelled = deluv( basicres )
    print( ree+"s) Text output latin u-v (repaces all u with v):" ,defo)
    print( uvdelled )

    alldelled = delall( basicres )
    print( ree+"t) Text output all deleted (deletes UV, klammern, sigma, grkl, umbrüche, ligaturen, interpunktion, edition numbering, unknown signs, diakritika):" ,defo)
    print( alldelled )

    tre = Trennstricheraus( testnorm.split( " " ) )
    print( ree+"u) Text output no hypens (input array of words removes hyphenation):" ,defo)
    print( tre )

    comb = GRvorbereitungT( atesttext );
    print( ree+"v) Text output a combination of steps (diacritics disambiguation, normalization, hyphenation removal, linebreak to space, punctuation separation and bracket removal):" ,defo)
    print( comb )
    
    #klammsys = delKLAMMSYS( atesttext );
    klammsys = hervKLAMMSYS( atesttext );
    print( ree+"w) Editions Klammerung (delet leidener Klammersystem):" ,defo)
    print( klammsys )   


def testprivatalpha():
    #drittes Beispiel müsste raus genommen werden
    bsp = ["ἀλλ’", "ἀϊδής", "ἀΐδιος", "ἀΐω", "ἀΐσθω", "ἀΐλιος", "Ἅιδης", "ἀϊών", "αἰών", "ἀΐσσω", "ἀΐδηλος", "ἀΐζηλος", "ἀΐσδηλος", "ἄϊδρις", "ἀϊστόω", "ἀΐσυλος", "αἴσῠλος", "ἄϋλος", "αὐλός", "ἀϊών", "αἰών", ];
    Strout = "";
    for b in range(len(bsp )):
        print( "Eingabe "+ bsp[b]+ " Ausgabe "+ AlphaPrivativumCopulativum( bsp[b] ) )


    
if __name__ == "__main__":
    demUsage( )


##******************************************************************************
## FKT
##******************************************************************************
'''
All Fkt in this Script with short introduction
setAnaFormTO( formstring ) #setter for global variable of analysis normal form
setDisplFormTO( formstring ) #setter for the global variable of display normal form
disambiguDIAkritika( string ) # return String replaced of diakrit
normarrayk( array ) # normalizes the key strings of a dictiopnary 
normatextwordbyword( text, wichnorm ) #splits the text into words and calls norm fkt
normatext( text, wichnorm ) #calles norm fkt on whole string
disambiguDIAkritika( astr ) # takes a string, replaces diakritica to have them equaly encoded, return string
ExtractDiafromBuchst( buchst ) # takes array of letters and returns array of array of diakritica and array of letters
replaceBehauchung( adiakstring ) # replaces behauchung in the transliteration of greek to latin
Expandelision( aword ) # given a word, if this is an elusion it will be expanded
TraslitAncientGreekLatin( astring ) # takes greek utf8 string and returns transliterated latin utf8 string
spitzeklammernHTML # ascapes spitze klammern to html encoding
basClean( astring ) # basic equalisation and hypenation reversal
AlphaPrivativumCopulativum( aword ) # takes a word utf8 greek and splits the alpha privativum and copulativum from wordform
iotasubiotoad( aword ) # takes greek utf8 string and repleces jota subscriptum with jota ad scriptum
ohnediakritW( aword ) # replaces diakritica
capitali( astring ) # first letter capitalized rest lowercase
nodiakinword( astring ) # combination of diakrica removal and jota subscriptum conversion
delall( text ) #deletes UV, klammern, sigma, grkl, umbrüche, ligaturen, interpunktion, edition numbering, unknown signs, diakritika
delnumbering( text ) #takes string return string without the edition numbering i.e. [2]
delligaturen( text ) # takes a string return string with ligatures turned to single letters
deldiak( text ) #like nodiakinword()
delinterp( text ) #takes string and returns the string without
delunknown( text ) # delete some to the programmer unknown signs
delumbrbine( text ) # input string and get it back with linebreaks removed
delmakup( text ) #input a string and get it pack with markup removed
delgrkl( text ) #input a string and get it bach with all small case letters
sigmaistgleich( text ) #equalize tailing sigma
delklammern( text ) # input stringa nd get it back with no brackets
deluv( text ) # repaces all u with v
Trennstricheraus( array of words ) #input array of words removes hyphenation
UmbruchzuLeerzeichen( text ) # input a string and get back a string with newlines replaces by spaces
Interpunktiongetrennt( wordlist ) #input array of words and have the interpunction separated from each word
iotasubiotoadL( wordlist ) # same as iotasubiotoad but on array of words
GRvorbereitungT( text ) # input a string and get a combination of diakritica disambiguation, normalization, hyphenation removal, linebreak to space, interpunktion separation and klammern removal
hervKLAMMSYS( text ) # input a string, mark all editorial signs
'''

#eof
