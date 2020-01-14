#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#**************************************************
# 2020 text normalisation Python3 Lib, Prof. Charlotte Schubert Alte Geschichte, Leipzig


'''
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


#**************************************************
# Section 00 
# basic UNICODE NORMAL FORM 
#**************************************************
def setAnaFormTO( fnew ):
    analysisNormalform = fnew

def setDisplFormTO( fnew ):
    dispnormalform = fnew

def normarrayk( aarray ):
	replacearray = {};
	for p in aarray:
		replacearray[ disambiguDIAkritika( p.normalize( analysisNormalform ) ) ] = aarray[ p ];
	return replacearray;

def normatext( text, wichnorm ):
    spt = text.split( " " )
    for w in range( len( spt ) ):
        nw = sameuninorm( spt[ w ], wichnorm );
        spt[ w ] = nw;
    return " ".join( spt )

# def takes sting and normalform string (for example "NFD")
def sameuninorm( aword, wichnorm ):
    return unicodedata.normalize( wichnorm, aword ) 


buchstGRI = {"Α":"A", "α":"a", "Β":"B", "β":"b", "Γ":"G", "γ":"g", "Δ":"D", "δ":"d", "Ε":"E", "ε":"e", "Ζ":"Z", "ζ":"z", "Η":"H", "η":"h", "Θ":"Th", "θ":"th", "Ι":"I", "ι":"i", "Κ": "K", "κ":"k", "Λ":"L", "λ":"l", "Μ":"M", "μ":"m", "Ν":"N", "ν":"n", "Ξ":"Xi", "ξ":"xi", "Ο":"O", "ο":"o", "Π":"P", "π":"p", "Ρ":"R", "ρ":"r", "Σ":"S", "σ":"s", "ς":"s", "Τ":"T", "τ":"t", "Υ":"U", "υ":"u", "Φ":"Ph", "φ":"ph", "Χ":"X", "χ":"x", "Ψ":"Ps", "ψ":"ps", "Ω":"O", "ω":"o"}#unvollständig!!!!ἀρχῆς
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

def ExtractDiafromBuchst( buchst ):
    toitter = list( unicodedata.normalize( "NFKD", buchst ) );
    b = [];
    d = [];
    for t in range( len( toitter ) ):
        co =  toitter[t].lower( );
        if( co in buchstGRI or co in buchsCoptic ):
            b.append( toitter[t] );
        else:
            d.append( toitter[t] );
    return ["".join( d ), "".join( b )];

def replaceBehauchung( adiakstring ):
    if( "῾" in adiakstring ):
        return "h"+adiakstring.replace( "῾","" );
    else:
        return adiakstring;

def TraslitAncientGreekLatin( astring ):
    wordlevel = delligaturen( unicodedata.normalize( "NFC", iotasubiotoad( unicodedata.normalize( "NFD" , astring.strip() ) ) ) ).split(" "); #care for iotasubscriptum, Ligature
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
            if( extracteBUCHST1+extracteBUCHST2 in groups and not "¨" in extractedida2 ): #wenn ein trema über dem zweiten buchstaben - diaresis keine Zusammenziehung (synresis)
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
# Section 0 
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
    astring = re.sub( cleangeviert, '-', astring)
    astring = re.sub( cleanhalbgeviert, '-', astring)
    astring = re.sub( cleanziffbreitergeviert, '-', astring)
    astring = re.sub( cleanviertelgeviert, '-', astring)
    astring = re.sub( cleanklgeviert, '-', astring)
    astring = re.sub( cleanklbindstrichkurz, '-', astring)
    astring = re.sub( cleanklbindstrichvollbreit, '-', astring)

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
        text = deluv( delklammern( sigmaistgleich( delgrkl( delligaturen( delinterp( delmakup( delumbrbine( deldiak(  text)))))))));
    else:
        text = delklammern( sigmaistgleich( delgrkl( delligaturen( delinterp( delmakup( delumbrbine( deldiak(  text  ) ) ) ) ) ) ) );
    return text;

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
    return text

# def takes string and replace html line breakes
def delumbrbine( text ):
    text = re.sub(regEbr1, "", text)
    text = re.sub(regEbr2, "", text);
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
    text = re.sub(regEkla14,"",text);
    return text

regEuv = re.compile( r"u" )
# def takes string and replaces u by v, used in classical latin texts
def deluv( text ):
    return re.sub( regEuv, "v", text );

# USAGE
def demUsage( ):
    #small greek/latin example
    atesttext = "&nbsp;&nbsp;\n<br/><br> <anny dsoid 920= 28>ἀλλ’ ἑτέραν τινὰ φύσιν ἄπειρον, ἐξ ἧς ἅπαντας γίνεσθαι τοὺς οὐρανοὺς καὶ τοὺς ἐν αὐτοῖς κόσμους· ἐξ ὧν δὲ ἡ γένεσίς ἐστι τοῖς οὖσι, καὶ τὴν φθορὰν εἰς ταῦτα γίνεσθαι κατὰ τὸ χρεών. διδόναι γὰρ αὐτὰ δίκην καὶ τίσιν ἀλλήλοις τῆς ἀδικίας κατὰ τὴν τοῦ χρόνου τάξιν, ποιητικωτέροις οὕτως ὀνόμασιν αὐτὰ λέγων· δῆλον δὲ ὅτι τὴν εἰς ἄλληλα μεταβολὴν τῶν τεττάρων στοιχείων οὗτος θεασάμενος οὐκ ἠξίωσεν ἕν τι τούτων ὑποκείμενον ποιῆσαι, ἀλλά τι ἄλλο παρὰ ταῦτα. οὗτος δὲ οὐκ ἀλλοιουμένου τοῦ στοιχείου τὴν γένεσιν ποιεῖ, ἀλλ’ ἀποκρινομένων τῶν ἐναντίων διὰ τῆς ἀιδίου κινή- σεως·"+" 1 Summá pecúniae, quam dedit in aerarium vel plebei Romanae vel dimissis militibus: denarium sexiens milliens.  "+"2 Opera fecit nova § aedem Martis, Iovis Tonantis et Feretri, Apollinis, díví Iúli, § Quirini, § Minervae, Iunonis Reginae, Iovis Libertatis, Larum, deum Penátium, § Iuventatis, Matris deum, Lupercal, pulvinar ad [11] circum, § cúriam cum chalcidico, forum Augustum, basilicam 35 Iuliam, theatrum Marcelli, § porticus . . . . . . . . . . , nemus trans Tiberím Caesarum. §  "+"3 Refécit Capitolium sacrasque aedes numero octoginta duas, theatrum Pompeí, aquarum rivos, viam Flaminiam.  Ϗ ϗ ϚϛȢȣꙊꙋἀἁἂἃἄἅἆἇἈἉἊἋἌἍἎἏἐἑἒἓἔἕἘἙἚἛἜἝἠἡἢἣἤἥἦἧἨἩἪἫἬἭἮἯἰἱἲἳἴἵἶἷἸἹἺἻἼἽἾἿὀὁὂὃὄὅὈὉὊὋὌὍὐὑὒὓὔὕὖὗὙὛὝὟὠὡὢὣὤὥὦὧὨὩὪὫὬὭὮὯὰάὲέὴήὶίὸόὺύὼώ	ᾀᾁᾂᾃᾄᾅᾆᾇᾈᾉᾊᾋᾌᾍᾎᾏᾐᾑᾒᾓᾔᾕᾖᾗᾘᾙᾚᾛᾜᾝᾞᾟᾠᾡᾢᾣᾤᾥᾦᾧᾨᾩᾪᾫᾬᾭᾮᾯᾰᾱᾲᾳᾴᾶᾷᾸᾹᾺΆᾼ᾽ι᾿῀῁ῂῃῄῆῇῈΈῊΉῌ῍῎῏ῐῑῒΐῖῗῘῙῚΊ῝῞῟ῠῡῢΰῤῥῦῧῨῩῪΎῬ῭΅`ῲῳῴῶῷῸΌῺΏῼ´῾ͰͱͲͳʹ͵Ͷͷͺͻͼͽ;Ϳ΄΅Ά·ΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϏϐϑϒϓϔϕϖϗϘϙϚϛϜϝϞϟϠϡϢϣϤϥϦϧϨϩϪϫϬϭϮϯϰϱϲϳϴϵ϶ϷϸϹϺϻϼϽϾϿ Αι αι γγ γκ γξ γχ ου Υι υι ἄϋλος αὐλός";

    #latin
    doUVlatin = true; 
    str1 = "Textinput 1:";
    print( str1 );
    print( atesttext );

    basicres = normatext( basClean( atesttext ), analysisNormalform );   
    str2 = "a) Text output basic norm:";
    print( str2 );
    print( basicres );

    diakdelled = deldiak( basicres );
    str3 = "b) Text output without diacritics:" ;
    print( str3 );
    print( diakdelled );

    interpdelled = delinterp( basicres );
    str4 = "c) Text output without punctuation:";
    print( str4 );
    print( interpdelled );

    ligdelled = delligaturen( basicres );
    str5 = "d) Text output without ligature:";
    print( str5 );
    print( ligdelled );

    umbrdelled = delumbrbine( basicres );
    str6 = "e) Text output without newline:";
    print( str6 );
    print( umbrdelled );

    grkldelled = delgrkl( basicres );
    str7 = "f) Text output equal case:";
    print( str7 );
    print( grkldelled );

    sidelled = sigmaistgleich( basicres );
    str8 = "g) Text output tailing sigma uniform:";
    print( str8 );
    print( sidelled );

    kladelled = delklammern( basicres );
    str9 = "h) Text output no brackets:";
    print( str9 );
    print( kladelled );

    uvdelled = deluv( basicres );
    str10 = "i) Text output latin u-v:";
    print( str10 );
    print( uvdelled );

    alldelled = delall( basicres );
    str11 = "j) Text output all deleted:";
    print( str11 );
    print( alldelled );   

    trans = TraslitAncientGreekLatin( basicres );
    str12 = "k) Text Transliteration (romanization of greek text):";
    print( str12 );
    print( trans ); 
    
if __name__ == "__main__":
    demUsage( )
