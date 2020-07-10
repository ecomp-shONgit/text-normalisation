//******************************************************************************
//
// 2020 text normalisation JavaScript Lib, 
// Prof. Charlotte Schubert Alte Geschichte, Leipzig
//
//******************************************************************************

/*
DEF: A text normalization is everything done to equalize encoding, appearance 
and composition of a sequence of signs called a text. There are two goals of 
normalization. The first is a common ground of signs  and the second is a 
reduction of differences between two sequences of signs.  Not every 
normalization step is useful for every comparison task! Remember: 
Sometimes it is important to not equalize word forms and 
sometimes it is important. 
*/


/*
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
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

//
"use strict"; 

//GLOBALS
let doUVlatin = false; 
const analysisNormalform = "NFKD";
const dispnormalform = "NFC";

let buchstGRI = {"Α":"A", "α":"a", "Β":"B", "β":"b", "Γ":"G", "γ":"g", "Δ":"D", "δ":"d", "Ε":"E", "ε":"e", "Ζ":"Z", "ζ":"z", "Η":"H", "η":"h", "Θ":"Th", "θ":"th", "Ι":"I", "ι":"i", "Κ": "K", "κ":"k", "Λ":"L", "λ":"l", "Μ":"M", "μ":"m", "Ν":"N", "ν":"n", "Ξ":"Xi", "ξ":"xi", "Ο":"O", "ο":"o", "Π":"P", "π":"p", "Ρ":"R", "ρ":"r", "Σ":"S", "σ":"s", "ς":"s", "Τ":"T", "τ":"t", "Υ":"U", "υ":"u", "Φ":"Ph", "φ":"ph", "Χ":"X", "χ":"x", "Ψ":"Ps", "ψ":"ps", "Ω":"O", "ω":"o"}
let LAGRI = {"A":"Α", "a":"α", "B":"Β", "b":"β", "G":"Γ", "g":"γ", "D":"Δ", "d":"δ", "E":"Ε", "e":"ε", "Z":"Ζ", "z":"ζ", "H":"Η", "h":"η", "Th":"Θ", "th":"θ", "I":"Ι", "i":"ι", "K":"Κ", "k":"κ","C":"Κ", "c":"κ", "Q":"Κ", "q":"κ", "L":"Λ", "l":"λ", "M":"Μ", "m":"μ", "N":"Ν", "n":"ν", "Xi":"Ξ", "xi":"ξ", "O":"Ο", "o":"ο", "P":"Π", "p":"π", "R":"Ρ", "r":"ρ", "S":"Σ", "s":"σ", "s":"ς", "T":"Τ", "t":"τ", "U":"Υ", "u":"υ", "Ph":"Φ", "ph":"φ", "F":"Φ", "f":"φ", "V":"Φ", "v":"φ", "X":"Χ", "x":"χ", "Ps":"Ψ", "ps":"ψ", "O":"Ω", "o":"ω"}
const groups = {"γγ":["n", "g"], "γκ":["n", "c"], "γξ":["n","x"], "γχ":["n", "ch"], "ηυ":["ē", "u"]}; //only small letters?
const behauchung = { "῾":"h" }; //missing other Hauch?
const buchsCoptic = {"ϐ": "B", "ϑ":"Th", "ϱ":"r", "ϰ":"k", "ϒ":"y", "ϕ":"ph", "ϖ":"p", "Ϝ":"W", "ϝ":"w", "Ϙ":"Q","ϙ":"q", "Ϟ":"ḳ", "ϟ":"ḳ", "Ϲ":"S", "Ⲥ":"S", "ⲥ":"s", "ϲ":"s", "Ͻ":"S", "ͻ":"s","Ϳ ":"j","ϳ":"j","Ͱ":"h","ͱ":"h","Ⲁ":"A","ⲁ":"a", 
"ϴ":"t","Ⲑ":"t","ⲑ":"t","ϵ":"e","϶":"e","Ϸ":"Sh","ϸ":"sh", "ϼ":"P","Ϡ":"S","ϡ":"S","Ⳁ":"S","ⳁ":"s",
"Ͳ":"Ss", "ͳ":"ss", "Ϻ":"S","ϻ":"s", "Ϣ":"š","ϣ":"š", "Ϥ":"F","ϥ":"f", "Ϧ":"X", "Ⳉ":"X",
"ϧ":"x","ⳉ":"x", "Ϩ":"H", "ϩ":"h", "Ϫ":"J", "ϫ":"j", "Ϭ":"C","ϭ":"c","Ϯ":"Di","ϯ":"di", 
"Ͼ":"S", "Ͽ":"S", "ͼ":"s", "ͽ":"s", "Ⲃ":"B","ⲃ":"b","Ⲅ":"G","ⲅ":"g", "Ⲇ":"D", "ⲇ":"d", "Ⲉ":"E", "ⲉ":"e", 
"Ⲋ":"St", "ⲋ":"st", "Ⲍ":"Z", "ⲍ":"z", "Ⲏ":"ê", "ⲏ":"ê", "Ⲓ":"I", "ⲓ":"i", "Ⲕ":"K", "ⲕ":"k", 
"Ⲗ":"L", "ⲗ":"l", "Ⲙ":"M", "ⲙ":"m", "Ⲛ":"N","ⲛ":"n", "Ⲝ":"ks", "ⲝ":"ks", "Ⲟ	":"O", "ⲟ":"o", 
"Ⲡ":"B", "ⲡ":"b", "Ⲣ":"R","ⲣ":"r", "Ⲧ":"T", "ⲧ":"t", "Ⲩ":"U", "ⲩ":"u", "Ⲫ":"F","ⲫ":"f","Ⲭ":"Kh", "ⲭ":"kh",
"Ⲯ":"Ps", "ⲯ":"ps", "Ⲱ":"ô", "ⲱ":"ô", "Ͷ":"W", "ͷ":"w"}; // 

//"de" Akzente richtig, oder falsch????
let listofelusion = { "δ᾽":"δὲ","δ'":"δὲ", "ἀλλ’": "ἀλλά", "ἀνθ’": "ἀντί", "ἀπ’": "ἀπό", "ἀφ’": "ἀπό","γ’": "γε","γένοιτ’": "γένοιτο","δ’": "δέ","δι’": "διά","δύναιτ’": "δύναιτο","εἶτ’": "εἶτα","ἐπ’": "ἐπί","ἔτ’": "ἔτι","ἐφ’": "ἐπί","ἡγοῖντ’": "ἡγοῖντο","ἵν’": "ἵνα","καθ’": "κατά","κατ’": "κατά","μ’": "με","μεθ’": "μετά","μετ’": "μετά","μηδ’": "μηδέ","μήδ’": "μηδέ","ὅτ’": "ὅτε","οὐδ’": "οὐδέ","πάνθ’": "πάντα","πάντ’": "πάντα","παρ’": "παρά","ποτ’": "ποτε","σ’": "σε","ταῦθ’": "ταῦτα","ταῦτ’": "ταῦτα","τοῦτ’": "τοῦτο","ὑπ’": "ὑπό","ὑφ’": "ὑπό"};
const cleanhtmltags = new RegExp( '\<[\w\/]*\>', 'g' );
const cleanhtmlformat1 = new RegExp( '&nbsp;', 'g' );
const regEbr1 = new RegExp( '<br/>', 'g' ); 
const regEbr2 = new RegExp( '<br>', 'g' );
const cleanNEWL = new RegExp( '\n', 'g' );
const cleanRETL = new RegExp( '\r', 'g' );
const cleanstrangehochpunkt = new RegExp( '‧', 'g' );
const cleanthisbinde = new RegExp( '—', 'g' );
const cleanthisleer = new RegExp( '\xa0', 'g' );
const cleanleerpunkt = new RegExp( ' \\.', 'g' );
const cleanleerdoppelpunkt = new RegExp( ' :', 'g' );
const cleanleerkoma = new RegExp( ' ,', 'g' );
const cleanleersemik = new RegExp( ' ;', 'g' );
const cleanleerausrufe = new RegExp( ' !', 'g' );
const cleanleerfrege = new RegExp( ' \\?', 'g' );

//breakdown typographic letiances "Bindestriche und Geviertstriche"
const cleanklbindstrichvollbreit = new RegExp( '－', 'g' );
const cleanklbindstrichkurz = new RegExp( '﹣', 'g' );
const cleanklgeviert = new RegExp( '﹘', 'g' );
const cleanviertelgeviert = new RegExp( '‐', 'g' );
const cleanziffbreitergeviert = new RegExp( '‒', 'g' );
const cleanhalbgeviert = new RegExp( '–', 'g' );
const cleangeviert = new RegExp( '—', 'g' );

const escspitzeL = new RegExp( '<', 'g' );
const escspitzeR = new RegExp( '>', 'g' );

let notprivalpha = [];//["ἀΐω"];

// array of unicode diacritics (relevant for polytonic greek)
const diacriticsunicodeRegExp = new Array( 
	new RegExp( '\u{0313}', 'g' ), 
	new RegExp( "\u{0314}", 'g' ), 
	new RegExp( "\u{0300}", 'g' ), 
	new RegExp( "\u{0301}", 'g' ), 
	new RegExp( "\u{00B4}", 'g' ), 
	new RegExp( "\u{02CA}", 'g' ), 
	new RegExp( "\u{02B9}", 'g' ), 
	new RegExp( "\u{0342}", 'g' ), 
	new RegExp( "\u{0308}", 'g' ), 
	new RegExp( "\u{0304}", 'g' ), 
	new RegExp( "\u{0306}", 'g' ),
    new RegExp( '’', 'g' ),
    new RegExp( '\'', 'g' ),
    new RegExp( '᾽', 'g' ),
    new RegExp( '´', 'g' ),
    new RegExp( "‘", 'g' )
);
const regJotaSub = new RegExp( '\u{0345}', 'g' );
// precompiled regular expressions
/*const strClean1 = new RegExp( '’', 'g' );
const strClean2 = new RegExp( '\'', 'g' );
const strClean3 = new RegExp( '᾽', 'g' );
const strClean4 = new RegExp( '´', 'g' );
const strClean5 = new RegExp( "‘", 'g' );*/
const numeringReg1 = new RegExp( '\[[0-9]+\]', 'g' );
const numeringReg2 = new RegExp( /\[[M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})]+\]/, 'g' );

// precompiled regular expressions of the relevant ligatures 
const regEstigma = new RegExp( '\u{03DA}', 'g' ); 
const regEstigmakl = new RegExp( '\u{03DB}', 'g' );
const regEomikonyplsi = new RegExp( 'ȣ', 'g' );
const regEomikonyplsiK = new RegExp( 'Ȣ', 'g' );
const regEUk = new RegExp( 'Ꙋ', 'g' );
const regEuk = new RegExp( 'ꙋ', 'g' );
const regEkai = new RegExp( 'ϗ', 'g' );
const regEKai = new RegExp( 'Ϗ', 'g' );
const regEl1 = new RegExp( '\u{0223}', 'g' );
const regEl2 = new RegExp( '\u{0222}', 'g' );

const regEdoppelP = new RegExp( ':', 'g' );
const regEeinfahP = new RegExp( '\\.', 'g' );
const regEkomma = new RegExp( ',', 'g' );
const regEsemiK = new RegExp( ';', 'g' );
const regEhochP = new RegExp( '·', 'g' );
const regEausr = new RegExp( '!', 'g' );
const regEfarge = new RegExp( '\\?', 'g' );
const regEan1 = new RegExp( '“', 'g' );
const regEan5 = new RegExp( '„', 'g' );
const regEan2 = new RegExp( '”', 'g' );
const regEan3 = new RegExp( '"', 'g' );
const regEan4 = new RegExp( "'", 'g' );
const regEan6 = new RegExp( '(\s*)[\∶|\⋮|\·|\⁙|;]+(\s*)', 'g' );


const regU1 = new RegExp( "†", 'g' );
const regU2 = new RegExp( "\\*", 'g' );
const regU3 = new RegExp( "⋖", 'g' );
const regU4 = new RegExp( "#", 'g' ); 

const regEtailingsig = new RegExp( "ς", 'g' );

const regEkla1 = new RegExp( "\\(", 'g' );
const regEkla2 = new RegExp( "\\)", 'g' );
const regEkla3 = new RegExp( "\\{", 'g' );
const regEkla4 = new RegExp( "\\}", 'g' );
const regEkla5 = new RegExp( "\\[", 'g' );
const regEkla6 = new RegExp( "\\]", 'g' );
const regEkla7 = new RegExp( "\\<", 'g' );
const regEkla8 = new RegExp( "\\>", 'g' );
const regEkla9 = new RegExp( "⌈", 'g' );
const regEkla10 = new RegExp( "⌉", 'g' );
const regEkla11 = new RegExp( "‹", 'g' );
const regEkla12 = new RegExp( "›", 'g' );
const regEkla13 = new RegExp( "«", 'g' );
const regEkla14 = new RegExp( "»", 'g' );
const regEkla15 = new RegExp( "⟦", 'g' );
const regEkla16 = new RegExp( "⟧", 'g' );
const regEkla17 = new RegExp( '\u{3008}', 'g' );
const regEkla18 = new RegExp( '\u{3009}', 'g' );
const regEkla19 = new RegExp( '\u{2329}', 'g' );
const regEkla20 = new RegExp( '\u{232A}', 'g' );
const regEkla21 = new RegExp( '\u{27E8}', 'g' );
const regEkla22 = new RegExp( '\u{27E9}', 'g' );

const regEuv = new RegExp( "u", 'g' );

//original abschrift, Klammerbehandlungfließtext
//Inschriften Klammersystem
//https://apps.timwhitlock.info/js/regex#
const lueckeBestimmt = new RegExp( /\[[Ͱ-Ͼἀ-῾|◌̣ ]+\]/, 'g' ); //l0
const lueckeinZeile = new RegExp( /\[\-\-\-\]/, 'g' ); //klasse l1
const lueckeinZeile2 = new RegExp(/\[3\]/, 'g' ); //lueckeinZeile, klasse l1
const lueckeausZeile = new RegExp( /\[\-\-\-\-\-\-\]/, 'g' ); //klasse l2
const lueckeausZeile2 = new RegExp( /\[6\]/, 'g' ); //Luecke im Umfang einer Zeile, Klasse l2
const lueckeunbest = new RegExp( /\]\[/, 'g' ); // Klasse l3

const zeilenende = new RegExp( / \/ /, 'g' ); // Klasse l4
const zeilenendeDigit = new RegExp( / \/ \d+ /, 'g' ); // Klasse l4
const zeilenanfang = new RegExp( / \| /, 'g' ); // Zeilenanfang, Klasse l5
const zeilenanfangDigit = new RegExp( / \| \d+ /, 'g' ); // Zeilenanfang, Klasse l5
const aufabk = new RegExp( /\(\)/, 'g' );  //Auflösung von Abkürzungen, Klasse l6
const beschaedigt = new RegExp( /\[nurbuchstabenoderleer\]/, 'g' ); //beschädigt oder undeutlich, klasse l7
const getilgt = new RegExp( /\{\}/, 'g' ); // Tilgung, Klasse l8
const rasiert = new RegExp( /\[\[\]\]/, 'g' ); //Rasur, Klasse l9
const ueberschr = new RegExp( /\<\<\>\>/, 'g' ); // Überschrieben, Klasse l10
const tilgrewrite = new RegExp( /\<\<\[\[\]\]\>\>/, 'g' ); //Tilgung Wiedereinfügung, Klasse l11
const punktunter = "◌̣ "; //Punkt unter Buchstaben - Buchstabe nur Teilweise erhalten -- später, Klasse l12
const anzgriechbuch = new RegExp( / \.+ /, 'g' ); //Anzahl unbestimmabrer griechischen Bustaben, Klasse l13
const anzlatbuchs = new RegExp( / \++ /, 'g' );  //Anzahl unbestimmbarer römsicher Buchstaben, Klasse l14
const korrdeseditors = new RegExp( /\<\>/, 'g' ); //Korrektur des Editors, Klasse l15

//**************************************************
// Section 0000
// helper
//**************************************************
const ronum = {//not perfect
"i" :1, 
"ii" :1, 
"iii" :1, 
"iiii" :1, 
"iv" :1, 
"v" :1, 
"vii" :1, 
"viii" :1, 
"ix" :1, 
"x" :1, 
"xi" :1, 
"xii" :1, 
"xiii" :1, 
"xiv" :1, 
"xv" :1, 
"xvi" :1, 
"xvii" :1, 
"xviii" :1, 
"xix" :1, 
"xx" :1, 
"xxi" :1, 
"xxii" :1, 
"xxiii" :1, 
"xxiv" :1, 
"xxv" :1, 
"xxvi" :1, 
"xxvii" :1, 
"xxviii" :1, 
"xxix" :1, 
"xxx" :1, 
"xxxi" :1, 
"xxxii" :1, 
"xxxiii" :1, 
"xxxiv" :1, 
"xxxv" :1, 
"xxxvi" :1, 
"xxxvii" :1, 
"xxxviii" :1, 
"xxxix" :1, 
"xl" :1, 
"xli" :1, 
"xlii" :1, 
"xliii" :1, 
"xliv" :1, 
"xlv" :1, 
"xlvi" :1, 
"xlvii" :1, 
"xlviii" :1, 
"xlix" :1, 
"l" :1, 
"li" :1, 
"lii" :1, 
"liii" :1, 
"liv" :1, 
"lv" :1, 
"lvi" :1, 
"lvii" :1, 
"lviii" :1, 
"lix" :1, 
"lx" :1, 
"lxi" :1, 
"lxii" :1, 
"lxiii" :1, 
"lxiv" :1, 
"lxv" :1, 
"lxvi" :1, 
"lxvii" :1, 
"lxviii" :1, 
"lxix" :1, 
"lxx" :1, 
"lxxi" :1, 
"lxxii" :1, 
"lxxiii" :1, 
"lxxiv" :1, 
"lxxv" :1, 
"lxxvi" :1, 
"lxxvii" :1, 
"lxxviii" :1, 
"lxxix" :1, 
"lxxx" :1, 
"lxxxi" :1, 
"lxxxii" :1, 
"lxxxiii" :1, 
"lxxxiv" :1, 
"lxxxv" :1, 
"lxxxvi" :1, 
"lxxxvii" :1, 
"lxxxviii" :1, 
"lxxxix" :1, 
"xc" :1, 
"xci" :1, 
"xcii" :1, 
"xciii" :1, 
"xciv" :1, 
"xcv" :1, 
"xcvi" :1, 
"xcvii" :1, 
"xcviii" :1, 
"xcix" :1, 
"c":1
};

const grnum = {//not perfect
"α" :1, 
"β" :1, 
"γ" :1, 
"δ" :1, 
"ε" :1, 
"ϛ" :1, 
"ζ" :1, 
"η" :1, 
"θ" :1, 
"ι" :1, 
"ια" :1, 
"ιβ" :1, 
"ιγ" :1, 
"ιδ" :1, 
"ιε" :1, 
"ιϛ" :1, 
"ιζ" :1, 
"ιη" :1, 
"ιθ" :1, 
"κ" :1, 
"κα" :1, 
"κβ" :1, 
"κγ" :1, 
"κδ" :1, 
"κε" :1, 
"κϛ" :1, 
"κζ" :1, 
"κη" :1, 
"κθ" :1, 
"λ" :1, 
"λα" :1, 
"λβ" :1, 
"λγ" :1, 
"λδ" :1, 
"λε" :1, 
"λϛ" :1, 
"λζ" :1, 
"λη" :1, 
"λθ" :1, 
"μ" :1, 
"μα" :1, 
"μβ" :1, 
"μγ" :1, 
"μδ" :1, 
"με" :1, 
"μϛ" :1, 
"μζ" :1, 
"μη" :1, 
"μθ" :1, 
"ν" :1, 
"να" :1, 
"νβ" :1, 
"νγ" :1, 
"νδ" :1, 
"νε" :1, 
"νϛ" :1, 
"νζ" :1, 
"νη" :1, 
"νθ" :1, 
"ξ" :1, 
"ξα" :1, 
"ξβ" :1, 
"ξγ" :1, 
"ξδ" :1, 
"ξε" :1, 
"ξϛ" :1, 
"ξζ" :1, 
"ξη" :1, 
"ξθ" :1, 
"ο" :1, 
"οα" :1, 
"οβ" :1, 
"ογ" :1, 
"οδ" :1, 
"οε" :1, 
"οϛ" :1, 
"οζ" :1, 
"οη" :1, 
"οθ" :1, 
"π" :1, 
"πα" :1, 
"πβ" :1, 
"πγ" :1, 
"πδ" :1, 
"πε" :1, 
"πϛ" :1, 
"πζ" :1, 
"πη" :1, 
"πθ" :1, 
"ϟ" :1, 
"ϟα" :1, 
"ϟβ" :1, 
"ϟγ" :1, 
"ϟδ" :1, 
"ϟε" :1, 
"ϟϛ" :1, 
"ϟζ" :1, 
"ϟη" :1, 
"ϟθ" :1, 
"ρ" : 1
};

function isnumber( maybe ){
    //do romannumbers
    const maymay = parseInt(maybe);
    if( !isNaN( maymay ) ){
        return true;
    } else if( maybe in ronum ){
        return true;     
    } else if( maybe in grnum ){
        return true;
    }
    return false;
}
//******************************************************************************
// Section 000
// basic UNICODE NORMAL FORM / TRANSLITERATION
//******************************************************************************
function setAnaFormTO( fnew ){
    analysisNormalform = fnew;
}

function setDisplFormTO( fnew ){
    dispnormalform = fnew;
}

function normarrayk( aarray ){
	let replacearray = new Object( );
	for( let p in aarray ){
		replacearray[  disambiguDIAkritika( p.normalize( analysisNormalform ) ) ] = aarray[ p ];
	}
	return replacearray;
}

function normarrayksiguv( aarray ){
	let replacearray = new Object( );
	for( let p in aarray ){
		replacearray[ sigmaistgleich( deluv( disambiguDIAkritika( p.normalize( analysisNormalform ) ) ) )] = aarray[ p ];
	}
	return replacearray;
}

function normarrayval( aarray ){ // by reference ????
    for( let p in aarray ){
        
        aarray[ p ] = disambiguDIAkritika( aarray[ p ].normalize( analysisNormalform ));
    }
}

function normarrayvalsiguv( aarray ){ // by reference ????
    for( let p in aarray ){
        
        aarray[ p ] = sigmaistgleich(deluv(disambiguDIAkritika( aarray[ p ].normalize( analysisNormalform ))));
    }
}

// function takes sting and normalform string (for example "NFD")
/*function normatextwordbyword( text, wichnorm ){
    let spt = text.split( " " );
    const lele = spt.length;
    for( let w = 0; w < lele; w++ ){
        let nw = normatext( spt[ w ], wichnorm );
        spt[ w ] = nw;
    }
    return spt.join( " " )
}*/

function normatext( text, wichnorm ){
    return text.normalize( wichnorm );
}

const spai1 = new RegExp( '\u{2002}', 'g' );//enspacing
const spai2 = new RegExp( '\u{2000}', 'g' );//enquad
function sameallspacing( astr ){
    astr = astr.replace( spai1, ' ' );
    astr = astr.replace( spai2, ' ' );
    return astr;
}

function disambiguDIAkritika( astr ){
    astr = astr.split( "\u0027" ).join( "\u2019" ); //typogra korrektes postroph;
    astr = astr.split( "'" ).join( "\u2019" );
    astr = astr.split( "\u1FBD" ).join( "\u2019" );
    return astr;
}

function disambiguadashes( astring ){
    astring = astring.replace( cleangeviert, '-' );
    astring = astring.replace( cleanhalbgeviert, '-' );
    astring = astring.replace( cleanziffbreitergeviert, '-' );
    astring = astring.replace( cleanviertelgeviert, '-' );
    astring = astring.replace( cleanklgeviert, '-' );
    astring = astring.replace( cleanklbindstrichkurz, '-' );
    astring = astring.replace( cleanklbindstrichvollbreit, '-' );
    return astring;
}

function ExtractDiafromBuchst( buchst ){ //input as string
    let toitter = buchst.normalize( "NFKD" ).split( "" );
    let b = [];
    let d = [];
    for( let t in toitter ){
        let co =  toitter[t].toLowerCase( );
        if( buchstGRI[ co ] || buchsCoptic[ co ] || buchstLAT[ co ] ){
            b.push( toitter[t] );
        } else {
            d.push( toitter[t] );
        }
    }
    return [d.join(""), b.join("")];
}

function ExtractDiafromBuchstText( atext ){
    let t = "";
    let spli = atext.split( " " );
    for( let i in spli ){
        t += JSON.stringify( ExtractDiafromBuchst( spli[ i ] ) );
    }
    return t;
}

function replaceBehauchung( adiakstring ){
    if( adiakstring.indexOf( "῾" ) !== -1 ){
        return "h"+adiakstring.replace( "῾","" );
    } else {
        return adiakstring;
    }
}

//replace a elision
function Expandelision( aword ){
    //if word in listofelusion
    let t = listofelusion[ aword ];
    if( t ){
        return t;
    } else {
        return aword;
    }
}

function ExpandelisionText( atext ){
    let t = "";
    let wds = atext.split( " " );
    for( let w in wds ){
        t += " "+ Expandelision(  wds[ w ] );
    }
    return t;
}

function TranslitLatinGreekLetters( astring ){

    //
    let wordlevel = delligaturen( astring.trim().normalize( "NFC" ) ).split(" ");
    let greekenized = [ ];
    for( let w in wordlevel ){
        let buchstlevel = Expandelision( wordlevel[ w ] ).split("");
        const lele = len( buchstlevel );
        let perword = [];
        let extractedida2 = "";
        let extracteBUCHST2 = "";
        for( let b = 1; b < lele; b+=1 ){
            
            let zwischenerg1 = ExtractDiafromBuchst( buchstlevel[ b-1 ] );
            let zwischenerg2 = ExtractDiafromBuchst( buchstlevel[ b ] );
            //console.log(zwischenerg1, zwischenerg2);
            let extractedida1 = zwischenerg1[0];
                extractedida2 = zwischenerg2[0];
            let extracteBUCHST1 = zwischenerg1[1];
                extracteBUCHST2 = zwischenerg2[1];
            //console.log("o1", buchstlevel[ b-1 ], "o2", buchstlevel[ b ], "e1", extracteBUCHST1, "d1", extractedida1, "e2", extracteBUCHST2, "d2", extractedida2);
            if( LAGRI[ extracteBUCHST1+extracteBUCHST2 ] && extracteBUCHST1 !== "" && extracteBUCHST2 !== "" ){
                perword.push( LAGRI[ extracteBUCHST1+extracteBUCHST2 ]+extractedida1+extractedida2 );
            } else {
                if( LAGRI[extracteBUCHST1] ){
                    perword.push( LAGRI[ extracteBUCHST1 ]+extractedida1 );
                } else {
                    perword.push( buchstlevel[ b-1 ] );
                }
            }
        }
        if( LAGRI[ extracteBUCHST2 ] ){
            
            perword.push( LAGRI[ extracteBUCHST2 ]+extractedida2 );
        } else {
            perword.push( buchstlevel[ lele-1 ] );
        }
        greekenized.push( perword.join( "" ) );
    }
    //return astring;
    return greekenized.join( " " );
}

function TraslitAncientGreekLatin( astring ){
    //if( notgreek ){
    //    return astring;
    //}
    //console.log(astring);
    let wordlevel = delligaturen( iotasubiotoad( astring.trim().normalize( "NFD" ) ).normalize( "NFC" ) ).split(" "); //care for iotasubscriptum, Ligature
    //console.log(wordlevel);
    //de !!!
    let romanized = [];
    for( let w in wordlevel ){
        
        let buchstlevel = Expandelision( wordlevel[ w ] ).split("");
        //console.log(buchstlevel);
        let grouped = [];
        let notlastdone = true;
        let extractedida2 = "";
        let extracteBUCHST2 = "";
        const lele = len( buchstlevel );
        for( let b = 1; b < lele; b+=1 ){
            if( buchstlevel[ b-1 ] === "" ){
                continue;
            }
            let zwischenerg1 = ExtractDiafromBuchst( buchstlevel[ b-1 ] );
            let zwischenerg2 = ExtractDiafromBuchst( buchstlevel[ b ] );
            let extractedida1 = zwischenerg1[0];
                extractedida2 = zwischenerg2[0];
            let extracteBUCHST1 = zwischenerg1[1];
                extracteBUCHST2 = zwischenerg2[1];
            //console.log(zwischenerg1, zwischenerg2);
            if( groups[extracteBUCHST1+extracteBUCHST2] && extractedida2.indexOf( "¨" ) === -1 ){ //wenn kein trema über dem zweiten buchstaben - diaresis keine Zusammenziehung (synresis)
                let gou = groups[ extracteBUCHST1+extracteBUCHST2 ];
                grouped.push( (gou[0]+replaceBehauchung(extractedida1)+gou[1]+replaceBehauchung(extractedida2)).normalize( "NFC" ) );
                buchstlevel[ b ] = "";//delet alread in groupand revistible
                notlastdone = false;
            } else {
                if( buchstGRI[extracteBUCHST1] ){
                    grouped.push( (buchstGRI[extracteBUCHST1]+replaceBehauchung(extractedida1)).normalize( "NFC" ) );
                } else {
                    if( buchsCoptic[extracteBUCHST1] ){
                        grouped.push( (buchsCoptic[extracteBUCHST1]+replaceBehauchung(extractedida1)).normalize( "NFC" ) );
                    } else {
                        //realy not - leave IT
                        grouped.push( buchstlevel[ b-1 ] );
                    }
                }
                notlastdone = true;
            }
        }
        if( notlastdone ){
            if( buchstGRI[extracteBUCHST2] ){
                    grouped.push( (buchstGRI[extracteBUCHST2]+replaceBehauchung(extractedida2)).normalize( "NFC" ) );
                } else {
                    if( buchsCoptic[extracteBUCHST2] ){
                        grouped.push( (buchsCoptic[extracteBUCHST2]+replaceBehauchung(extractedida2)).normalize( "NFC" ) );
                    } else {
                        //realy not - leave IT
                        grouped.push( buchstlevel[ buchstlevel.length-1 ] );
                    }
                }
        }
        romanized.push( grouped.join("") );
    }
    return romanized.join( " " );  
}

//******************************************************************************
// Section 00 
// basic cleaning and string conversion via regexp 
//******************************************************************************
function spitzeklammernHTML( astr ){
    return astr.replace( escspitzeL, '&lt;' ).replace( escspitzeR, '&gt;' );
}

//basic equalisation and hypenation reversion
function basClean( astring ){
    astring = astring.replace(cleanNEWL, " <br/>").replace(cleanRETL, " <br/>").replace(cleanstrangehochpunkt,"·").replace(cleanthisbinde," — ").replace( cleanthisleer, ' ').replace( cleanleerpunkt, '.').replace( cleanleerdoppelpunkt, ':').replace( cleanleerkoma, ',').replace( cleanleersemik, ';').replace( cleanleerausrufe, '!').replace( cleanleerfrege, '?').replace(cleangeviert, '-').replace(cleanhalbgeviert, '-').replace(cleanziffbreitergeviert, '-').replace(cleanviertelgeviert, '-').replace(cleanklgeviert, '-').replace(cleanklbindstrichkurz, '-').replace(cleanklbindstrichvollbreit, '-');

    // remove hyphens
    let ws = astring.split(" ");
        let ca = [];
        let halfw = "";
        let secondhalf = "";
        for( let w in ws ){
            if( ws[w].indexOf( "-" ) !== -1 ){
                let h = ws[w].split( "-" );
                halfw = h[0].replace(" ", "");
                secondhalf = h[1].replace(" ", "");
                if( secondhalf.indexOf("]") !== -1 ){ 
                    let hh = h[1].split("]");
                    if( hh[1].length > 1 ){
                        ca.push( halfw + hh[1] + " " + hh[0] + "]<br/>" );
                        halfw = "";
                        secondhalf = "";
                    }
                }
            } else if ( "<br/>" !== ws[w] && ws[w] !== "" && ws[w] !== " " && halfw !== "" ){
                if( ws[w].indexOf("]") !== -1 ){
                
                    secondhalf = ws[w].replace(" ", "");
                } else {
                    ca.push( halfw + ws[w].replace("<br/>", "") + " " + secondhalf + "<br/>" ); //trennstriche
                    halfw = "";
                    secondhalf = "";
                }
            } else {
                if( ws[w] !== "" ){ //remove mehrfache leerstellen
                    ca.push( ws[w] );
                }
            }
        }
        return ca.join( " " );
}

function ohnesatzzeichen( wliste ){
	for(let sa in satzzeichen ){
		for( let w in wliste){
			wliste[ w ] = wliste[ w ].split( satzzeichen[ sa ] ).join( "" );
		}
	}
	return wliste;
}

//usage: replaceWordsfromarray( ["in", "cum", "et", "a", "ut"], " ", stringggg )
function replaceWordsfromarray( arr, replacement, strstr ){
    for( let a in arr){
        strstr = strstr.replace( arr[a], replacement );
    }
    return strstr
}
//******************************************************************************
// Section 0
// word leve conversions: 
// alpha privativum
// alpha copulativum
// Klammersysteme
//******************************************************************************

function AlphaPrivativumCopulativum( aword ){ //just works on NFC and NFKC
    if( notprivalpha.includes( aword ) === false ){
        let buchs = delall( aword ).split( "" );
        if( buchs[0] === "α" ){ //erste Buchstabe alpha
            if( hasKEY( vokaleGRI , buchs[1] ) ){ // zweiter ein Vokal
                let b2dia = ExtractDiafromBuchst(aword[1])[0];
                //let b1dia = ExtractDiafromBuchst(aword[0])[0]; 
                //console.log(  "zweiter vokal", ""b2dia, b2dia.indexOf(  "\u0308" )) 
                //insert the https://de.wikipedia.org/wiki/Unicodeblock_Kombinierende_diakritische_Zeichen
                if( b2dia.indexOf( "\u0308" ) !== -1  ){ //zweiter Buchstabe mit Trema, erste Buchstabe mit spiritus lenis
                    return aword[0] +" "+ aword.slice(1) ;
                } else { //
                    return aword;
                }
            } else {
                return aword;
            }
        } else {
            return aword;
        }
    } else {
        return aword;
    }
        
}

function AlphaPrivativumCopulativumText( atext ){
    let t = "";
    let spli = atext.split( " " );
    for( let l in spli ){
        t += " "+AlphaPrivativumCopulativum( spli[ l ] );
    }
    return t;
}


//KLAMMERSYSTEME HIER BEHANDELN

//******************************************************************************
// Section 1 
// unicode related comparing and norming, handling of diacritics
//******************************************************************************

// function takes string, splits it with jota subscriptum and joins the string again using jota adscriptum
function iotasubiotoad( aword ){
 	return aword.split( "\u0345" ).join( "ι" );
}

// function takes "one word"
function ohnediakritW( aword ){
    for( let dia in diacriticsunicodeRegExp ){
		aword = aword.replace( diacriticsunicodeRegExp[ dia ], "" );
	}
	return aword;
}

function capitali( astring ) {
    return astring.charAt(0).toUpperCase() + astring.slice(1).toLowerCase();
}

// function takes a string replaces some signs with regexp and oth
function nodiakinword( aword ){
    //let spt = ((aword.replace(strClean1, "").replace(strClean2, "").replace(strClean3, "").replace(strClean4, "")).normalize( analysisNormalform ));
    //return iotasubiotoad( ohnediakritW( spt ) );
    return iotasubiotoad( ohnediakritW( aword.normalize( analysisNormalform ) ) );
}

//******************************************************************************
// Section 2: deleting things that could be not same in two texts
//******************************************************************************

// function take a string and deletes diacritical signes, ligatures, remaining interpunction, line breaks, capital letters to small ones, equalizes sigma at the end of greek words, and removes brakets
function delall( text ){
    if( doUVlatin ){ // convert u to v in classical latin text
        text = deluv( delklammern( sigmaistgleich( delgrkl( delumbrbine( delligaturen( delinterp( delmakup( delnumbering( delunknown( deldiak(  text)))))))))));
    } else {
        text = delklammern( sigmaistgleich( delgrkl( delumbrbine( delligaturen( delinterp( delmakup( delnumbering( delunknown( deldiak(  text  ) ) ) ) ) ) ) ) ) );
    }
    return text;
}

//run this before the klammern deletion
function delnumbering( text ){ //untested
    return text.replace( numeringReg1,"" ).replace( numeringReg2,"" );
}

// function take a string and replaces all occorences of a regular expression
function delligaturen( text ){
    return text.replace( regEstigma, "στ").replace( regEstigmakl, "στ").replace( regEUk, "Υκ").replace( regEuk, "υκ").replace(regEomikonyplsi, "ου").replace(regEomikonyplsiK, "ου").replace(regEkai, "καὶ").replace(regEKai, "Καὶ").replace(regEl1, "\u039F\u03C5" ).replace(regEl2, "\u03BF\u03C5" );
}

// function takes string and splits it into words, than normalizes each word, joins the string again
function deldiak( text ){
    let spt = text.split( " " ); //seperate words
    const lele = spt.length;
    for( let wi = 0; wi < lele; wi++ ){
        spt[ wi ] = nodiakinword( spt[ wi ] );
    }
    return  spt.join( " " );
}    

// function takes a string and replaces interpunction
function delinterp( text ){
    return text.replace(regEdoppelP, "").replace(regEeinfahP, "").replace(regEkomma, "").replace(regEsemiK, "").replace(regEhochP, "").replace(regEausr, "").replace(regEfarge, "").replace(regEan1, "").replace(regEan2, "").replace(regEan3, "").replace(regEan4, "").replace(regEan5, "").replace(regEan6, "");
}

// function takes a string and replaces some unknown signs
function delunknown( text ){
    return text.replace(regU1, "").replace(regU2, "").replace(regU3, "").replace(regU4, "");
}


// function takes string and replace html line breakes
function delumbrbine( text ){
    return text.replace(regEbr1, "").replace(regEbr2, "");
}

function umbrtospace( text ){
    text = text.replace(cleanNEWL, " ");
    text = text.replace(cleanRETL, " ");
    text = text.replace(regEbr1, " ");
    text = text.replace(regEbr2, " ");
    return text;
}

//more to come
function delmakup( text ){
    return text.replace(cleanhtmltags, "").replace(cleanhtmlformat1, "");
}

// ...
function delgrkl( text ){
    return text.toLowerCase();
}

// function takes string and converts tailing sigma to inline sigma (greek lang)
function sigmaistgleich( text ){
    return text.replace(regEtailingsig, "σ");
}


// function take sstring and replaces the brakets -- do not run this before the Klammersystem fkt
function delklammern( text ){
    return text.replace(regEkla1, "").replace(regEkla2, "").replace(regEkla3, "").replace(regEkla4,"").replace(regEkla5,"").replace(regEkla6,"").replace(regEkla7,"").replace(regEkla8,"").replace(regEkla9,"").replace(regEkla10,"").replace(regEkla11,"").replace(regEkla12,"").replace(regEkla13,"").replace(regEkla14,"").replace(regEkla15,"").replace(regEkla16,"").replace(regEkla17,"").replace(regEkla18,"").replace(regEkla19,"").replace(regEkla20,"").replace(regEkla21,"").replace(regEkla22,"");
}

function deledklammern( text ){
    return text.replace(regEkla1, "").replace(regEkla2, "").replace(regEkla3, "").replace(regEkla4,"").replace(regEkla5,"").replace(regEkla6,"").replace(regEkla9,"").replace(regEkla10,"").replace(regEkla11,"").replace(regEkla12,"").replace(regEkla13,"").replace(regEkla14,"").replace(regEkla15,"").replace(regEkla16,"").replace(regEkla17,"").replace(regEkla18,"").replace(regEkla19,"").replace(regEkla20,"").replace(regEkla21,"").replace(regEkla22,"");
}
// function takes string and replaces u by v, used in classical latin texts
function deluv( text ){
    return text.replace( regEuv, "v" );
}

//some bundels
function Trennstricheraus( wliste ){
	let ersterteil = "";
	let zweiterteil = "";
	let neueWLISTE = [];
    const lele = wliste.length;
	for(let w = 0; w < lele; w++){
		if( ersterteil.length === 0 ){
			if( wliste[ w ].indexOf( "-" ) !== -1 ){
				let eUNDz = wliste[ w ].split( "-" );
				if( eUNDz[1].length > 0 ){
					let zweiohnenewline = eUNDz[1].split( "\n" );
			 		neueWLISTE.push( eUNDz[0]+zweiohnenewline[ zweiohnenewline.length-1 ] );
				} else {
					ersterteil = eUNDz[0];
				}
				//console.log(eUNDz.length, eUNDz);
			} else { //nix - normales wort
				neueWLISTE.push( wliste[ w ] );
			}
		} else { // es gab eine Trennung und die ging über zwei Listenzellen
			if( wliste[ w ].indexOf( "[" ) === -1 && wliste[ w ].indexOf( "]" ) === -1){
				let zweiteralsliste = wliste[ w ].split( "\n" );
				//console.log("split", zweiteralsliste, wliste[ w ], ersterteil+zweiteralsliste[ zweiteralsliste.length-1 ]);
				neueWLISTE.push( ersterteil+zweiteralsliste[ zweiteralsliste.length-1 ] );
				ersterteil = "";
			} else { //klammern behandeln
					 //wenn ich hier kein push auf der neune Wortliste mache, dann lösche ich damit die geklammerten sachen

				if( wliste[ w ].indexOf( "[" ) !== -1 && wliste[ w ].indexOf( "]" ) !== -1 ){ //klammern in einem Wort
					let zweiteralsliste = wliste[ w ].split( "]" );
				
					neueWLISTE.push( ersterteil+zweiteralsliste[1].substring(1, zweiteralsliste[1].length-1) );
					//console.log("NO SPLIT", ersterteil+zweiteralsliste[1].substring(1, zweiteralsliste[1].length-1));
				} else if( wliste[ w ].indexOf( "[" ) !== -1 ){
					let zweiteralsliste = wliste[ w ].split( "[" );
					neueWLISTE.push( ersterteil+zweiteralsliste.join("") );
				} else { //nur schließende Klammer
					let zweiteralsliste = wliste[ w ].split( "]" );
					neueWLISTE.push( ersterteil+zweiteralsliste[1] );
					//console.log("NO SPLIT", ersterteil+zweiteralsliste[1].substring(1, zweiteralsliste[1].length-1));
				}
			}
		}
	}
	return neueWLISTE;
}

function UmbruchzuLeerzeichen( atext ){
	atext = atext.split("\n").join( " " );
	return atext;
}

function Interpunktiongetrennt( wliste ){
    let neuewliste = [];
    for( let sa in satzzeichen ){
        for(let w in wliste ){
            if( wliste[ w ].indexOf( satzzeichen[ sa ] ) !== -1 ){
                neuewliste.push( wliste[ w ].split( satzzeichen[ sa ] ).join( "" ) );
                neuewliste.push( satzzeichen[ sa ] );
            } else {
                neuewliste.push(  wliste[ w ] );
            }
        }
        wliste = neuewliste;
        neuewliste = [];
    }
	return wliste;
}

/*function Klammernbehandeln( wliste ){
	let neueWliste = [];
	for(let w in wliste ){
		// wenn die eckigen KLammern in einem Wort sthen, dann werte es als Zählung - einfahcste Weise
		if( (wliste[w].indexOf("]") !== 0 && wliste[w].indexOf("[") !== 0) ){
			neueWliste.push(wliste[w]);
		}
	}
	return neueWliste;
}*/

function iotasubiotoadL( wliste ){
	for( let w in wliste){
		wliste[ w ] = iotasubiotoad( wliste[ w ] );
	}
	return wliste;
}

//function to use with greek text maybe
function GRvorbereitungT( dtext ){
	let diewo =  disambiguDIAkritika( delnumbering(dtext).normalize( analysisNormalform ).toLowerCase() ).split( " " );
		//diewo = iotasubiotoadL( diewo );
		diewo = UmbruchzuLeerzeichen( Trennstricheraus( diewo ).join( " " ) ).split( " " );
		diewo = Interpunktiongetrennt( diewo );
		//diewo = Klammernbehandeln( diewo );
	return diewo;
} 

const unterPu = new RegExp( "◌̣ ", 'g' )
function delUnterpunkt( text ){
    return text.replace( unterPu, "" );
}

//******************************************************************************
// USAGE
//******************************************************************************
function mach(){
    demUsage( document.getElementById( "inp").value ); 
}

function demUsage( atesttext ){
    //small greek/latin example
    if( atesttext === undefined ){
    atesttext = "„[IX]” ⁙ ἀλλ’ ἑτέραν τινὰ φύσιν ἄπειρον', ἐξ ἧς ἅπαντας γίνεσθαι τοὺς οὐρανοὺς καὶ τοὺς ἐν αὐτοῖς κόσμους· ἐξ ὧν δὲ ἡ γένεσίς ἐστι τοῖς οὖσι, καὶ τὴν φθορὰν εἰς ταῦτα γίνεσθαι κατὰ τὸ χρεών. διδόναι γὰρ αὐτὰ δίκην καὶ τίσιν ἀλλήλοις τῆς ἀδικίας κατὰ τὴν τοῦ χρόνου τάξιν, ποιητικωτέροις οὕτως ὀνόμασιν αὐτὰ λέγων· δῆλον δὲ ὅτι τὴν εἰς ἄλληλα μεταβολὴν τῶν τεττάρων στοιχείων οὗτος θεασάμενος οὐκ ἠξίωσεν ἕν τι τούτων ὑποκείμενον ποιῆσαι, ἀλλά τι ἄλλο παρὰ ταῦτα. οὗτος δὲ οὐκ ἀλλοιουμένου τοῦ στοιχείου τὴν γένεσιν ποιεῖ, ἀλλ’ ἀποκρινομένων τῶν ἐναντίων διὰ τῆς ἀιδίου κινή- σεως· 1 Summá pecúniae, quam dedit in [bla bla bla] aerarium vel plebei Romanae vel dimissis militibus=> denarium sexiens milliens. 2 Opera fecit nova § aedem Martis, Iovis Tonantis et Feretri, Apollinis, díví Iúli, § Quirini, § Minervae, Iunonis Reginae, Iovis Libertatis, Larum, deum Penátium, § Iuventatis, Matris deum, Lupercal, pulvinar ad [11] circum, § cúriam cum chalcidico, forum Augustum, basilicam 35 Iuliam, theatrum Marcelli, § porticus . . . . . . . . . . , nemus trans Tiberím Caesarum. § 3 Refécit Capitolium sacrasque aedes numero octoginta duas, theatrum Pompeí, aquarum rivos, viam Flaminiam.  Ϗ ϗ ϚϛȢȣꙊꙋἀἁἂἃἄἅἆἇἈἉἊἋἌἍἎἏἐἑἒἓἔἕἘἙἚἛἜἝἠἡἢἣἤἥἦἧἨἩἪἫἬἭἮἯἰἱἲἳἴἵἶἷἸἹἺἻἼἽἾἿὀὁὂὃὄὅὈὉὊὋὌὍὐὑὒὓὔὕὖὗὙὛὝὟὠὡὢὣὤὥὦὧὨὩὪὫὬὭὮὯὰάὲέὴήὶίὸόὺύὼώ	ᾀᾁᾂᾃᾄᾅᾆᾇᾈᾉᾊᾋᾌᾍᾎᾏᾐᾑᾒᾓᾔᾕᾖᾗᾘᾙᾚᾛᾜᾝᾞᾟᾠᾡᾢᾣᾤᾥᾦᾧᾨᾩᾪᾫᾬᾭᾮᾯᾰᾱᾲᾳᾴᾶᾷᾸᾹᾺΆᾼ᾽ι᾿῀῁ῂῃῄῆῇῈΈῊΉῌ῍῎῏ῐῑῒΐῖῗῘῙῚΊ῝῞῟ῠῡῢΰῤῥῦῧῨῩῪΎῬ῭΅`ῲῳῴῶῷῸΌῺΏῼ´῾ͰͱͲͳʹ͵Ͷͷͺͻͼͽ;Ϳ΄΅Ά·ΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϏϐϑϒϓϔϕϖϗϘϙϚϛϜϝϞϟϠϡϢϣϤϥϦϧϨϩϪϫϬϭϮϯϰϱϲϳϴϵ϶ϷϸϹϺϻϼϽϾϿ Αι αι γγ γκ γξ γχ ου Υι υι ἄϋλος αὐλός  τί φῄς; γραφὴν σέ τις, ὡς ἔοικε, γέγραπται οὐ γὰρ ἐκεῖνό γε καταγνώσομαι, ὡς σὺ ἕτερον. δ̣[ὲ κ]αὶ";
    }
    let atttext = "";

    //latin
    doUVlatin = true; 
    let str1 = "<b>Textinput 1:</b>";
    atttext = atttext + "<br/>"+ str1+"<br/>"+ atesttext;
    //normed in analysis form
    let testnorm = normatext( atesttext, analysisNormalform );
    
    let disa = disambiguDIAkritika( testnorm ); 
    let disades = "<b>a) Disambuguation of diacritics (takes a string, replaces diakritica to have them equaly encoded, return string):</b>";
    atttext = atttext + "<br/><br/>"+ disades+"<br/>"+ disa;

    let ex = ExtractDiafromBuchstText( testnorm );
    let exdes = "<b>b) Separation of diakritics  (takes array of letters and returns array of array of diakritica and array of letters):</b>";
    //console.log(exdes);
    //console.log(ex);
    atttext = atttext + "<br/><br/>"+ exdes+"<br/>"+ ex ;

    let basicres =  basClean( atesttext );   
    let str2 = "<b>c) Text output basic norm (basic equalization and hypenation reversal):</b>";
    atttext = atttext + "<br/><br/>"+ str2+"<br/>"+ basicres;

    let translitbsp = TraslitAncientGreekLatin( basicres );
    let str12 = "<b>d) Text transliteration (gr-la) (takes greek utf8 string and returns transliterated latin utf8 string):</b>";
    //console.log( translitbsp );
    //console.log( str12 );   
    atttext = atttext + "<br/><br/>"+ str12+"<br/>"+ translitbsp; 

    
    let translitLAGR = TranslitLatinGreekLetters( basicres );
    let str12x = "<b>d2) Text transliteration (la-gr) (takes latin utf8 string and returns transliterated greek utf8 string):</b>";
    //console.log( translitbsp );
    //console.log( str12 );   
    atttext = atttext + "<br/><br/>"+ str12x+"<br/>"+ translitLAGR; 

    let expeli = ExpandelisionText( testnorm );
    let desexpeli = "<b>e) Elusion expansion (given a text, if this is an elusion it will be expanded):</b>";
    //console.log( desexpeli );
    //console.log( expeli );
    atttext = atttext + "<br/><br/>"+ desexpeli+"<br/>"+ expeli; 

    let spiekla = spitzeklammernHTML( testnorm );
    let desspiekla = "<b>f) Spitze Klammern zu html (escapes spitze klammern to html encoding):</b>";
    //console.log( desspiekla );
    //console.log( spiekla );   
    atttext = atttext + "<br/><br/>"+ desspiekla+"<br/>"+ spiekla;

    let al = AlphaPrivativumCopulativumText( atesttext ); //Normal form composed!!!
    let desal = "<b>g) Alpha privativum  / copulativum (takes utf8 greek and splits the alpha privativum and copulativum from wordforms):</b>";
    //console.log( desal );
    //console.log( al );   
    atttext = atttext + "<br/><br/>"+ desal+"<br/>"+ al;

    let jo = iotasubiotoad( testnorm ); //Normal form composed!!!
    let desjo = "<b>h) JOTA (takes greek utf8 string and repleces jota subscriptum with jota ad scriptum):</b>";
    //console.log( desjo );
    //console.log( jo );   
    atttext = atttext + "<br/><br/>"+ desjo+"<br/>"+ jo;

    let diakdelled = deldiak( basicres );
    let str3 = "<b>i) Text output without diacritics (replaces diacritics):</b>" ;
    //console.log( str3 );
    //console.log( diakdelled );
    atttext = atttext + "<br/><br/>"+ str3+"<br/>"+ diakdelled;

    let numb = delnumbering( testnorm );
    let desnumb = "<b>j) Text output without numbering (takes string return string without the edition numbering i.e. [2]):</b>" ;
    console.log( desnumb );
    console.log( numb );
    atttext = atttext + "<br/><br/>"+ desnumb +"<br/>"+ numb;
    
    let unk = delunknown( testnorm );
    let desunk = "<b>k) Text output without some signs (delete some to the programmer unknown signs: †, *,⋖,#):</b>" ;
    //console.log( desunk );
    //console.log( unk );
    atttext = atttext + "<br/><br/>"+ desunk +"<br/>"+ unk;

    let mark = delmakup( testnorm );
    let desmark = "<b>l) Text output without markup (input a string and get it pack with markup removed):</b>" ;
    //console.log( desmark );
    //console.log( mark );
    atttext = atttext + "<br/><br/>"+ desmark +"<br/>"+ mark;

    let interpdelled = delinterp( basicres );
    let str4 = "<b>m) Text output without punctuation (takes string and returns the string without):</b>";
    //console.log( str4 );
    //console.log( interpdelled );
    atttext = atttext + "<br/><br/>"+ str4+"<br/>"+ interpdelled;

    let ligdelled = delligaturen( basicres );
    let str5 = "<b>n) Text output without ligature (takes a string return string with ligatures turned to single letters):</b>";
    //console.log( str5 );
    //console.log( ligdelled );
    atttext = atttext + "<br/><br/>"+ str5+"<br/>"+ ligdelled;

    let umbrdelled = delumbrbine( basicres );
    let str6 = "<b>o) Text output without newline (input string and get it back with linebreaks removed):</b>";
    //console.log( str6 );
    //console.log( umbrdelled );
    atttext = atttext + "<br/><br/>"+ str6+"<br/>"+ umbrdelled;

    let grkldelled = delgrkl( basicres );
    let str7 = "<b>p) Text output equal case (input a string and get it bach with all small case letters):</b>";
    //console.log( str7 );
    //console.log( grkldelled );
    atttext = atttext + "<br/><br/>"+ str7+"<br/>"+ grkldelled;

    let sidelled = sigmaistgleich( basicres );
    let str8 = "<b>q) Text output tailing sigma uniform (equalize tailing sigma):</b>";
    //console.log( str8 );
    //console.log( sidelled );
    atttext = atttext + "<br/><br/>"+ str8+"<br/>"+ sidelled;

    let kladelled = delklammern( basicres );
    let str9 = "<b>r) Text output no brackets (input stringa nd get it back with no brackets):</b>";
    //console.log( str9 );
    //console.log( kladelled );
    atttext = atttext + "<br/><br/>"+ str9+"<br/>"+ kladelled;

    let uvdelled = deluv( basicres );
    let str10 = "<b>s) Text output latin u-v (repaces all u with v):</b>";
    //console.log( str10 );
    //console.log( uvdelled );
    atttext = atttext + "<br/><br/>"+ str10+"<br/>"+ uvdelled;

    let alldelled = delall( basicres );
    let str11 = "<b>t) Text output all deleted (deletes UV, klammern, sigma, grkl, umbrüche, ligaturen, interpunktion, edition numbering, unknown signs, diakritika):</b>";
    //console.log( alldelled );
    //console.log( str11 );
       
    atttext = atttext + "<br/><br/>"+ str11+"<br/>"+ alldelled;

    let tre = Trennstricheraus( testnorm.split( " " ) );
    let destre = "<b>u) Text output no hypens (input array of words removes hyphenation):</b>";
    //console.log( destre ); 
    //console.log( tre );
    atttext = atttext + "<br/><br/>"+ destre+"<br/>"+ tre;


    let comb = GRvorbereitungT( atesttext );
    let descomb = "<b>v) Text output a combination of steps (diacritics disambiguation, normalization, hyphenation removal, linebreak to space, punctuation separation and bracket removal):</b>";
    //console.log( descomb );
    //console.log( comb );       
    atttext = atttext + "<br/><br/>"+ descomb+"<br/>"+ comb;
   

   document.getElementById( "erg").innerHTML = atttext;
}

function testprivatalpha(){
    //drittes Beispiel müsste raus genommen werden
    let bsp = ["ἀλλ’", "ἀϊδής", "ἀΐδιος", "ἀΐω", "ἀΐσθω", "ἀΐλιος", "Ἅιδης", "ἀϊών", "αἰών", "ἀΐσσω", "ἀΐδηλος", "ἀΐζηλος", "ἀΐσδηλος", "ἄϊδρις", "ἀϊστόω", "ἀΐσυλος", "αἴσῠλος", "ἄϋλος", "αὐλός", "ἀϊών", "αἰών", ];
    let Strout = "";
    for( let b in bsp ){
        Strout += "Eingabe "+ bsp[b]+ " Ausgabe "+ AlphaPrivativumCopulativum( bsp[b] ) +"<br>";

    }
     document.getElementById( "mata").innerHTML = Strout; 
}

//******************************************************************************
// FKT
//******************************************************************************
/*
All Fkt in this Script with short introduction

setAnaFormTO( formstring ) //setter for global variable of analysis normal form

setDisplFormTO( formstring ) //setter for the global variable of display normal form

disambiguDIAkritika( string ) // return String replaced of diakrit

normarrayk( array ) // normalizes the key strings of a dictiopnary 

normatextwordbyword( text, wichnorm ) //splits the text into words and calls norm fkt

normatext( text, wichnorm ) //calles norm fkt on whole string

disambiguDIAkritika( astr ) // takes a string, replaces diakritica to have them equaly encoded, return string

ExtractDiafromBuchst( buchst ) // takes array of letters and returns array of array of diakritica and array of letters

replaceBehauchung( adiakstring ) // replaces behauchung in the transliteration of greek to latin

Expandelision( aword ) // given a word, if this is an elusion it will be expanded

TraslitAncientGreekLatin( astring ) // takes greek utf8 string and returns transliterated latin utf8 string

TranslitLatinGreekLetters( astring ) // takes latin utf8 string and returns transliterated greek utf8 string

spitzeklammernHTML // ascapes spitze klammern to html encoding

basClean( astring ) // basic equalisation and hypenation reversal

AlphaPrivativumCopulativum( aword ) // takes a word utf8 greek and splits the alpha privativum and copulativum from wordform

iotasubiotoad( aword ) // takes greek utf8 string and repleces jota subscriptum with jota ad scriptum

ohnediakritW( aword ) // replaces diakritica

capitali( astring ) // first letter capitalized rest lowercase

nodiakinword( astring ) // combination of diakrica removal and jota subscriptum conversion

delall( text ) //deletes UV, klammern, sigma, grkl, umbrüche, ligaturen, interpunktion, edition numbering, unknown signs, diakritika

delnumbering( text ) //takes string return string without the edition numbering i.e. [2]

delligaturen( text ) // takes a string return string with ligatures turned to single letters

deldiak( text ) //like nodiakinword()

delinterp( text ) //takes string and returns the string without

delunknown( text ) // delete some to the programmer unknown signs

delumbrbine( text ) // input string and get it back with linebreaks removed

delmakup( text ) //input a string and get it pack with markup removed

delgrkl( text ) //input a string and get it bach with all small case letters

sigmaistgleich( text ) //equalize tailing sigma

delklammern( text ) // input stringa nd get it back with no brackets

deluv( text ) // repaces all u with v

Trennstricheraus( array of words ) //input array of words removes hyphenation

UmbruchzuLeerzeichen( text ) // input a string and get back a string with newlines replaces by spaces

Interpunktiongetrennt( wordlist ) //input array of words and have the interpunction separated from each word

Klammernbehandeln( wordlist ) // same as delklammern but on array of words

iotasubiotoadL( wordlist ) // same as iotasubiotoad but on array of words

GRvorbereitungT( text ) // input a string and get a combination of diakritica disambiguation, normalization, hyphenation removal, linebreak to space, interpunktion separation and klammern removal


*/
//eof
