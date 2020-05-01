<?php

//******************************************************************************
//
// 2020 text normalisation JavaScript Lib, 
// Prof. Charlotte Schubert Alte Geschichte, Leipzig
//
//******************************************************************************

/*
DEF: A text normalization is everything done to equalize encoding, appearance 
and composition of a sequence of signs called a text. There are two goals of 
reduction of differences between two sequences of signs.  Not every 
normalization step is useful for every comparison task! Remember=> 
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
along with this program.  If not, see <http=>//www.gnu.org/licenses/>.
*/

declare( strict_types = 1 );
//include 'strdist.php';

/* MULTI BYTE STRING */
if( function_exists('mb_internal_encoding') ) {
    mb_internal_encoding("UTF-8"); //IF extension MBSTRING is installed UTF8 Strings are computable
    mb_regex_encoding("UTF-8");
} else {
    error_log("No mbstring extension - dist will fail on UTF 8 strings!", 1);//IF NOT - THROW A WARNING
}

//GLOBALS
$doUVlatin = false; 
$analysisNormalform = Normalizer::FORM_KD; //"NFKD";
$dispnormalform = Normalizer::FORM_C;//"NFC";

$buchstGRI = array("Α"=>"A", "α"=>"a", "Β"=>"B", "β"=>"b", "Γ"=>"G", "γ"=>"g", "Δ"=>"D", "δ"=>"d", "Ε"=>"E", "ε"=>"e", "Ζ"=>"Z", "ζ"=>"z", "Η"=>"H", "η"=>"h", "Θ"=>"Th", "θ"=>"th", "Ι"=>"I", "ι"=>"i", "Κ"=> "K", "κ"=>"k", "Λ"=>"L", "λ"=>"l", "Μ"=>"M", "μ"=>"m", "Ν"=>"N", "ν"=>"n", "Ξ"=>"Xi", "ξ"=>"xi", "Ο"=>"O", "ο"=>"o", "Π"=>"P", "π"=>"p", "Ρ"=>"R", "ρ"=>"r", "Σ"=>"S", "σ"=>"s", "ς"=>"s", "Τ"=>"T", "τ"=>"t", "Υ"=>"U", "υ"=>"u", "Φ"=>"Ph", "φ"=>"ph", "Χ"=>"X", "χ"=>"x", "Ψ"=>"Ps", "ψ"=>"ps", "Ω"=>"O", "ω"=>"o");//unvollständig!!!!ἀρχῆς
$vokaleGRI = ["ι"=>1,"υ"=>1,"ε"=>1,"ο"=>1,"α"=>1,"ω"=>1,"η"=>1];
$buchstLAT = array("d"=>1, "g"=>1, "p"=>1, "t"=>1, "c"=>1, "k"=>1, "q"=>1, "qu"=>1, "ph"=>1, "th"=>1, "ch"=>1, "x"=>1, "z"=>1, "f"=>1, "v"=>1, "s"=>1, "m"=>1, "n"=>1, "l"=>1, "r"=>1, "a"=>1,"i"=>2,"e"=>3,"o"=>4,"u"=>5,"v"=>6, "y"=>7);
$groups = array("γγ"=>array("n", "g"), "γκ"=>array("n", "c"), "γξ"=>array("n","x"), "γχ"=>array("n", "ch"), "ηυ"=>array("ē", "u")); //only great letters??????? what is with that?
$behauchung = array( "῾"=>"h" ); //missing other Hauch???
$buchsCoptic = array("ϐ"=> "B", "ϑ"=>"Th", "ϱ"=>"r", "ϰ"=>"k", "ϒ"=>"y", "ϕ"=>"ph", "ϖ"=>"p", "Ϝ"=>"W", "ϝ"=>"w", "Ϙ"=>"Q","ϙ"=>"q", "Ϟ"=>"ḳ", "ϟ"=>"ḳ", "Ϲ"=>"S", "Ⲥ"=>"S", "ⲥ"=>"s", "ϲ"=>"s", "Ͻ"=>"S", "ͻ"=>"s","Ϳ "=>"j","ϳ"=>"j","Ͱ"=>"h","ͱ"=>"h","Ⲁ"=>"A","ⲁ"=>"a", 
"ϴ"=>"t","Ⲑ"=>"t","ⲑ"=>"t","ϵ"=>"e","϶"=>"e","Ϸ"=>"Sh","ϸ"=>"sh", "ϼ"=>"P","Ϡ"=>"S","ϡ"=>"S","Ⳁ"=>"S","ⳁ"=>"s",
"Ͳ"=>"Ss", "ͳ"=>"ss", "Ϻ"=>"S","ϻ"=>"s", "Ϣ"=>"š","ϣ"=>"š", "Ϥ"=>"F","ϥ"=>"f", "Ϧ"=>"X", "Ⳉ"=>"X",
"ϧ"=>"x","ⳉ"=>"x", "Ϩ"=>"H", "ϩ"=>"h", "Ϫ"=>"J", "ϫ"=>"j", "Ϭ"=>"C","ϭ"=>"c","Ϯ"=>"Di","ϯ"=>"di", 
"Ͼ"=>"S", "Ͽ"=>"S", "ͼ"=>"s", "ͽ"=>"s", "Ⲃ"=>"B","ⲃ"=>"b","Ⲅ"=>"G","ⲅ"=>"g", "Ⲇ"=>"D", "ⲇ"=>"d", "Ⲉ"=>"E", "ⲉ"=>"e", 
"Ⲋ"=>"St", "ⲋ"=>"st", "Ⲍ"=>"Z", "ⲍ"=>"z", "Ⲏ"=>"ê", "ⲏ"=>"ê", "Ⲓ"=>"I", "ⲓ"=>"i", "Ⲕ"=>"K", "ⲕ"=>"k", 
"Ⲗ"=>"L", "ⲗ"=>"l", "Ⲙ"=>"M", "ⲙ"=>"m", "Ⲛ"=>"N","ⲛ"=>"n", "Ⲝ"=>"ks", "ⲝ"=>"ks", "Ⲟ	"=>"O", "ⲟ"=>"o", 
"Ⲡ"=>"B", "ⲡ"=>"b", "Ⲣ"=>"R","ⲣ"=>"r", "Ⲧ"=>"T", "ⲧ"=>"t", "Ⲩ"=>"U", "ⲩ"=>"u", "Ⲫ"=>"F","ⲫ"=>"f","Ⲭ"=>"Kh", "ⲭ"=>"kh",
"Ⲯ"=>"Ps", "ⲯ"=>"ps", "Ⲱ"=>"ô", "ⲱ"=>"ô", "Ͷ"=>"W", "ͷ"=>"w"); // 

//"de" Akzente richtig, oder falsch????
$GLOBALS["listofelusion"] = array( "δ᾽"=>"δὲ","δ'"=>"δὲ", "ἀλλ’"=> "ἀλλά", "ἀνθ’"=> "ἀντί", "ἀπ’"=> "ἀπό", "ἀφ’"=> "ἀπό","γ’"=> "γε","γένοιτ’"=> "γένοιτο","δ’"=> "δέ","δι’"=> "διά","δύναιτ’"=> "δύναιτο","εἶτ’"=> "εἶτα","ἐπ’"=> "ἐπί","ἔτ’"=> "ἔτι","ἐφ’"=> "ἐπί","ἡγοῖντ’"=> "ἡγοῖντο","ἵν’"=> "ἵνα","καθ’"=> "κατά","κατ’"=> "κατά","μ’"=> "με","μεθ’"=> "μετά","μετ’"=> "μετά","μηδ’"=> "μηδέ","μήδ’"=> "μηδέ","ὅτ’"=> "ὅτε","οὐδ’"=> "οὐδέ","πάνθ’"=> "πάντα","πάντ’"=> "πάντα","παρ’"=> "παρά","ποτ’"=> "ποτε","σ’"=> "σε","ταῦθ’"=> "ταῦτα","ταῦτ’"=> "ταῦτα","τοῦτ’"=> "τοῦτο","ὑπ’"=> "ὑπό","ὑφ’"=> "ὑπό");
$cleanhtmltags =  '/\<[\w\/]*\>/';
$cleanhtmlformat1 =  '/&nbsp;/';
$regEbr1 =  '/<br\/>/'; 
$GLOBALS["regEbr2"] =  '/<br>/';
$GLOBALS["cleanNEWL"] =  '/\n/';
$GLOBALS["cleanRETL"] =  '/\r/';
$GLOBALS["cleanstrangehochpunkt"] =  '/‧/';
$GLOBALS["cleanthisbinde"] =  '/—/';
$GLOBALS["cleanthisleer"] =  '/\xa0/u';
$GLOBALS["cleanleerpunkt"] =  '/ \\./';
$GLOBALS["cleanleerdoppelpunkt"] =  '/ :/';
$GLOBALS["cleanleerkoma"] =  '/ ,/';
$GLOBALS["cleanleersemik"] =  '/ ;/';
$GLOBALS["cleanleerausrufe"] =  '/ !/';
$GLOBALS["cleanleerfrege"] =  '/ \\?/';

//breakdown typographic letiances "Bindestriche und Geviertstriche"
$GLOBALS["cleanklbindstrichvollbreit"] =  '/－/';
$GLOBALS["cleanklbindstrichkurz"] =  '/﹣/';
$GLOBALS["cleanklgeviert"] =  '/﹘/';
$GLOBALS["cleanviertelgeviert"] =  '/‐/';
$GLOBALS["cleanziffbreitergeviert"] =  '/‒/';
$GLOBALS["cleanhalbgeviert"] =  '/–/';
$GLOBALS["cleangeviert"] =  '/—/';

$GLOBALS["escspitzeL"] =  '/\</';
$GLOBALS["escspitzeR"] =  '/\>/';

$GLOBALS["notprivalpha"] = [];//["ἀΐω"];

// array of unicode diacritics (relevant for polytonic greek)
$GLOBALS["diacriticsunicodeRegExp"] = array( 
	 '/\x{0313}/u', 
	 "/\x{0314}/u", 
	 "/\x{0300}/u", 
	 "/\x{0301}/u", 
	 "/\x{00B4}/u", 
	 "/\x{02CA}/u", 
	 "/\x{02B9}/u", 
	 "/\x{0342}/u", 
	 "/\x{0308}/u", 
	 "/\x{0304}/u", 
	 "/\x{0306}/u",
     '/’/u',
     '/\'/u',
     '/᾽/u',
     '/´/u',
     "/‘/u"
);
$GLOBALS["regJotaSub"] =  '/\x{0345}/u';
/*$strClean1 =  '’';
$strClean2 =  '\'';
$strClean3 =  '᾽';
$strClean4 =  '´';
$strClean5 =  "‘";*/
$GLOBALS["numeringReg1"] =  '/\[[0-9]+\]/';
$GLOBALS["numeringReg2"] =  '/\[[M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})]+\]/';

//regular expressions of the relevant ligatures 
$GLOBALS["regEstigma"] =  '/Ϛ/'; 
$GLOBALS["regEstigmakl"] =  '/ϛ/';
$GLOBALS["regEomikonyplsi"] =  '/ȣ/';
$GLOBALS["regEomikonyplsiK"] =  '/Ȣ/';
$GLOBALS["regEUk"] =  '/Ꙋ/';
$GLOBALS["regEuk"] =  '/ꙋ/';
$GLOBALS["regEkai"] =  '/ϗ/';
$GLOBALS["regEKai"] =  '/Ϗ/';

$GLOBALS["regEdoppelP"] =  '/\:/';
$GLOBALS["regEeinfahP"] =  '/\./';
$GLOBALS["regEkomma"] =  '/\,/';
$GLOBALS["regEsemiK"] =  '/\;/';
$GLOBALS["regEhochP"] =  '/\·/';
$GLOBALS["regEausr"] =  '/\!/';
$GLOBALS["regEfarge"] =  '/\?/';
$GLOBALS["regEan1"] =  '/\“/';
$GLOBALS["regEan5"] =  '/\„/';
$GLOBALS["regEan2"] =  '/\”/';
$GLOBALS["regEan3"] =  '/\"/';
$GLOBALS["regEan4"] =  "/\'/";
$GLOBALS["regEan6"] =  '/\∶|\⋮|\·|\⁙|;/';
$GLOBALS["satzzeichen"] = [".", ";", ",", ":", "!", "?", "·"];

$GLOBALS["regU1"] =  "/†/";
$GLOBALS["regU2"] =  "/\*/";
$GLOBALS["regU3"] =  "/⋖/";
$GLOBALS["regU4"] =  "/#/"; 

$GLOBALS["regEtailingsig"] =  "/ς/";

$GLOBALS["regEkla1"] =  "/\(/";
$GLOBALS["regEkla2"] =  "/\)/";
$GLOBALS["regEkla3"] =  "/\{/";
$GLOBALS["regEkla4"] =  "/\}/";
$GLOBALS["regEkla5"] =  "/\[/";
$GLOBALS["regEkla6"] =  "/\]/";
$GLOBALS["regEkla7"] =  "/\</";
$GLOBALS["regEkla8"] =  "/\>/";
$GLOBALS["regEkla9"] =  "/⌈/";
$GLOBALS["regEkla10"] =  "/⌉/";
$GLOBALS["regEkla11"] =  "/‹/";
$GLOBALS["regEkla12"] =  "/›/";
$GLOBALS["regEkla13"] =  "/«/";
$GLOBALS["regEkla14"] =  "/»/";
$GLOBALS["regEkla15"] =  "/⟦/";
$GLOBALS["regEkla16"] =  "/⟧/";

$GLOBALS["regEuv"] =  "/u/";

//original abschrift, Klammerbehandlungfließtext
//Inschriften Klammersystem
//https=>//apps.timwhitlock.info/js/regex#
$GLOBALS["lueckeBestimmt"] =  "/\[[Ͱ-Ͼἀ-῾|◌̣ ]+\]/"; //l0
$GLOBALS["lueckeinZeile"] =  "/\[\-\-\-\]/"; //klasse l1
$GLOBALS["lueckeinZeile2"] = "/\[3\]/"; //lueckeinZeile, klasse l1
$GLOBALS["lueckeausZeile"] =  "/\[\-\-\-\-\-\-\]/"; //klasse l2
$GLOBALS["lueckeausZeile2"] =  "/\[6\]/"; //Luecke im Umfang einer Zeile, Klasse l2
$GLOBALS["lueckeunbest"] =  "/\]\[/"; // Klasse l3

$GLOBALS["zeilenende"] =  "/ \/ /"; // Klasse l4
$GLOBALS["zeilenendeDigit"] =  "/ \/ \d+ /"; // Klasse l4
$GLOBALS["zeilenanfang"] =  "/ \| /"; // Zeilenanfang, Klasse l5
$GLOBALS["zeilenanfangDigit"] =  "/ \| \d+ /"; // Zeilenanfang, Klasse l5
$GLOBALS["aufabk"] =  "/\(\)/";  //Auflösung von Abkürzungen, Klasse l6
$GLOBALS["beschaedigt"] =  "/\[nurbuchstabenoderleer\]/"; //beschädigt oder undeutlich, klasse l7
$GLOBALS["getilgt"] =  "/\{\}/"; // Tilgung, Klasse l8
$GLOBALS["rasiert"] =  "/\[\[\]\]/"; //Rasur, Klasse l9
$GLOBALS["ueberschr"] =  "/\<\<\>\>/"; // Überschrieben, Klasse l10
$GLOBALS["tilgrewrite"] =  "/\<\<\[\[\]\]\>\>/"; //Tilgung Wiedereinfügung, Klasse l11
$GLOBALS["punktunter"] = "/◌̣ /"; //Punkt unter Buchstaben - Buchstabe nur Teilweise erhalten -- später, Klasse l12
$GLOBALS["anzgriechbuch"] =  "/ \.+ /"; //Anzahl unbestimmabrer griechischen Bustaben, Klasse l13
$GLOBALS["anzlatbuchs"] =  "/ \++ /";  //Anzahl unbestimmbarer römsicher Buchstaben, Klasse l14
$GLOBALS["korrdeseditors"] =  "/\<\>/"; //Korrektur des Editors, Klasse l15

//******************************************************************************
// Section 000
// basic UNICODE NORMAL FORM / TRANSLITERATION
//******************************************************************************
function hasKEY( $alist, $thekey ){
    return array_key_exists( $thekey, $alist );
}

function len( $athing ){
    if( is_array( $athing ) ){
        return sizeof( $athing );
    } elseif( is_string( $athing ) ){
        return strlen( $athing );
    } else {
        return NULL; //hm will this do
    }

}

function setAnaFormTO( $fnew ){
    $GLOBALS["analysisNormalform"] = $fnew;
}

function setDisplFormTO( $fnew ){
    $GLOBALS["dispnormalform"] = $fnew;
}

function normarrayk( $aarray ){
	$replacearray = array( );
	foreach( $aarray as $p => $v ){ //FOREACH as key value
		$replacearray[ disambiguDIAkritika( normalizer_normalize( $p, $GLOBALS["analysisNormalform"] ) ) ] = $v;
	}
	return $replacearray;
}

function normarrayval( $aarray ){ // by reference ????
    foreach( $aarray as $p => $v ){
        $aarray[ $p ] = normalizer_normalize( $v, $GLOBALS["analysisNormalform"] );
    }
}

function normalizearraykeys(){
    $GLOBALS["listofelusion"] = normarrayk( $GLOBALS["listofelusion"] );
    normarrayval( $GLOBALS["listofelusion"] );
}

//function takes sting and normalform string (for example "NFD")
function normatextwordbyword( $text, $wichnorm ){
    $spt = explode(" ", $text );
    
    $lele = len( $spt );
    for( $w = 0; $w < $lele; $w++ ){
        $nw = normatext( $spt[ $w ], $wichnorm );
        $spt[ $w ] = $nw;
    }
    return implode(" ", $spt );
}

function normatext( $text, $wichnorm ){
    return normalizer_normalize( $text, $wichnorm );
}



function disambiguDIAkritika( $astr ){
    //\u2019
    $astr = implode( "’", explode( "\u{0027}", $astr ) ); //typogra korrektes postroph;
    $astr = implode( "\u{2019}", explode( "'"     , $astr ) );
    $astr = implode( "’", explode( "\u{1FBD}", $astr ) );
    return $astr;
}

function own_mb_str_split( $string ) {
    return preg_split('/(?<!^)(?!$)/u', $string ); //nicht am ende und nicht am Anfang und ansonsten nach jedem Zeichen (auch combining, wenn Normalform so gesetzt)
}

function ExtractDiafromBuchst( $buchst ){ //input as string
    
    $toitter = own_mb_str_split(  $buchst );//
    
    $b = array();
    $d = array();
    foreach( $toitter as $t => $v ){
        $co =  strtolower( $v );
        //$co =  mb_strtolower($v, "UTF-8");
        //echo $co."<br>";
        if( array_key_exists( $co, $GLOBALS["buchstGRI"] ) || array_key_exists( $co,$GLOBALS["buchsCoptic"] ) || array_key_exists( $co, $GLOBALS["buchstLAT"] )  ){
            $b[] = $v;
        } else {
            $d[] = $v;
        }
    }
    return [ implode( "", $d ), implode( "", $b ) ];
}

function ExtractDiafromBuchstText( $atext ){
    //echo ".........".normalizer_is_normalized( $atext, Normalizer::FORM_KD)."...........";
    if( !normalizer_is_normalized( $atext, Normalizer::FORM_KD) ){
       //this is errnous if you put in a  single word (explode of text) the shit does not work for some words
       $atext = normalizer_normalize( $atext, Normalizer::FORM_KD );
    }
    $t = "";
    $spli = explode(" " , $atext );
    foreach( $spli as $i => $v ){
        $resu = ExtractDiafromBuchst( $v );
        $t = $t. "[".$resu[0].",".$resu[1]."]";
    }
    return $t;
}

function replaceBehauchung( $adiakstring ){
    if( mb_strpos( $adiakstring, "῾" ) !== False ){
        return "h".preg_replace( "\῾\u", "", $adiakstring );
    } else {
        return $adiakstring;
    }
}

//replace a elision
function Expandelision( $aword ){
    //if word in listofelusion
    if( array_key_exists( $aword, $GLOBALS["listofelusion"] ) ){
        return $GLOBALS["listofelusion"][ $aword ];
    } else {
        return $aword;
    }
}

function ExpandelisionText( $atext ){
    $t = "";
    $wds = explode( " ", $atext );
    
    foreach( $wds as $w => $v ){
        $t = $t." ".Expandelision(  $v );
    }
    return $t;
}

function TraslitAncientGreekLatin( $astring ){
    //if( notgreek ){
    //    return astring;
    //}
    //console.log(astring);
    $wordlevel = explode( " ", normalizer_normalize( delligaturen( iotasubiotoad(  trim( $astring, " ") ) ) ,Normalizer::FORM_D ) ); //care for iotasubscriptum, Ligature
    //console.log(wordlevel);
    //de !!!
    $romanized = [];
    foreach( $wordlevel as $w => $v ){
        
        $buchstlevel = own_mb_str_split( Expandelision( $v ) );
        //console.log(buchstlevel);
        $grouped = [];
        $notlastdone = true;
        $extractedida2 = "";
        $extracteBUCHST2 = "";
        $lele = len( $buchstlevel );
        for( $b = 1; $b < $lele; $b+=1 ){
            if( $buchstlevel[ $b-1 ] === "" ){
                continue;
            }
            //$zwischenerg1 = ExtractDiafromBuchst( normalizer_normalize($buchstlevel[ $b-1 ],Normalizer::FORM_D ) );
            //$zwischenerg2 = ExtractDiafromBuchst( normalizer_normalize($buchstlevel[ $b ],Normalizer::FORM_D ) );
            $zwischenerg1 = ExtractDiafromBuchst( $buchstlevel[ $b-1 ]  );
            $zwischenerg2 = ExtractDiafromBuchst( $buchstlevel[ $b ]  );
            $extractedida1 = $zwischenerg1[0];
            $extractedida2 = $zwischenerg2[0];
            $extracteBUCHST1 = $zwischenerg1[1];
            $extracteBUCHST2 = $zwischenerg2[1];
            
            if( array_key_exists( $extracteBUCHST1.$extracteBUCHST2, $GLOBALS["groups"]) && mb_strpos( $extractedida2, "¨" ) === False ){ //wenn kein trema über dem zweiten buchstaben - diaresis keine Zusammenziehung (synresis)
                $gou = $GLOBALS["groups"][ $extracteBUCHST1.$extracteBUCHST2 ];
                $grouped[] = normalizer_normalize( $gou[0].replaceBehauchung( $extractedida1 ).$gou[1].replaceBehauchung( $extractedida2 ), Normalizer::FORM_C );
                $buchstlevel[ $b ] = "";//de$alread in groupand revistible
                $notlastdone = false;
            } else {
                if( array_key_exists( $extracteBUCHST1, $GLOBALS["buchstGRI"]) ){
                    $grouped[] = normalizer_normalize( $GLOBALS["buchstGRI"][$extracteBUCHST1].replaceBehauchung($extractedida1), Normalizer::FORM_C );
                } else {
                    if( array_key_exists( $extracteBUCHST1, $GLOBALS["buchsCoptic"]) ){
                        $grouped[] = normalizer_normalize( $GLOBALS["buchsCoptic"][$extracteBUCHST1].replaceBehauchung($extractedida1), Normalizer::FORM_C );
                    } else {
                        //realy not - leave IT
                        $grouped[] = $buchstlevel[ $b-1 ];
                    }
                }
                $notlastdone = true;
            }
        }
        if( $notlastdone ){
            if( array_key_exists( $extracteBUCHST2, $GLOBALS["buchstGRI"]) ){
                    $grouped[] = normalizer_normalize( $GLOBALS["buchstGRI"][$extracteBUCHST2].replaceBehauchung($extractedida2), Normalizer::FORM_C );
                } else {
                    if( array_key_exists( $extracteBUCHST2, $GLOBALS["buchsCoptic"] ) ){
                        $grouped[] =  normalizer_normalize($GLOBALS["buchsCoptic"][$extracteBUCHST2].replaceBehauchung($extractedida2), Normalizer::FORM_C );
                    } else {
                        //realy not - leave IT
                        $grouped[] = $buchstlevel[ len($buchstlevel)-1 ];
                    }
                }
        }
        $romanized[] = implode( "", $grouped );
    }
    return implode( " ", $romanized );  
}

//******************************************************************************
// Section 00 
// basic cleaning and string conversion via regexp 
//******************************************************************************
function spitzeklammernHTML( $astr ){
    $astr = preg_replace( $GLOBALS["escspitzeL"], '&lt;', $astr );
    $astr = preg_replace( $GLOBALS["escspitzeR"], '&gt;', $astr );
    return $astr;
}

//basic equalisation and hypenation reversion
function basClean( $astring ){
    $astring = preg_replace( $GLOBALS["cleanNEWL"], " <br/>", $astring );
    $astring = preg_replace( $GLOBALS["cleanRETL"], " <br/>", $astring );
    $astring = preg_replace( $GLOBALS["cleanstrangehochpunkt"], "·", $astring );
    $astring = preg_replace( $GLOBALS["cleanthisbinde"], " — ", $astring );
    $astring = preg_replace( $GLOBALS["cleanthisleer"], ' ', $astring );
    $astring = preg_replace( $GLOBALS["cleanleerpunkt"], '.', $astring );
    $astring = preg_replace( $GLOBALS["cleanleerdoppelpunkt"], ':', $astring );
    $astring = preg_replace( $GLOBALS["cleanleerkoma"], ',', $astring );
    $astring = preg_replace( $GLOBALS["cleanleersemik"], ';', $astring );
    $astring = preg_replace( $GLOBALS["cleanleerausrufe"], '!', $astring );
    $astring = preg_replace( $GLOBALS["cleanleerfrege"], '?', $astring );
    $astring = preg_replace( $GLOBALS["cleangeviert"], '-', $astring );
    $astring = preg_replace( $GLOBALS["cleanhalbgeviert"], '-', $astring );
    $astring = preg_replace( $GLOBALS["cleanziffbreitergeviert"], '-', $astring );
    $astring = preg_replace( $GLOBALS["cleanviertelgeviert"], '-', $astring );
    $astring = preg_replace( $GLOBALS["cleanklgeviert"], '-', $astring );
    $astring = preg_replace( $GLOBALS["cleanklbindstrichkurz"], '-', $astring );
    $astring = preg_replace( $GLOBALS["cleanklbindstrichvollbreit"], '-', $astring );

    // remove hyphens
    $ws = explode( " ", $astring );
    $ca = Trennstricheraus( $ws );
    return implode(" ", $ca );
}

function ohnesatzzeichen( $wliste ){
	foreach( $GLOBALS["satzzeichen"] as $sa  ){
		foreach( $wliste as $w => $v ){
			$wliste[ $w ] = implode( "", explode( $sa, $v ) );
		}
	}
	return $wliste;
}

//******************************************************************************
// Section 0
// word leve conversions=> 
// alpha privativum
// alpha copulativum
// Klammersysteme
//******************************************************************************

function AlphaPrivativumCopulativum( $aword ){ //just works on NFC and NFKC
    if( in_array( $aword, $GLOBALS["notprivalpha"] ) === false ){
        $buchs = own_mb_str_split( delall( $aword ) );
        if( $buchs[0] === "α" ){ //erste Buchstabe alpha
            if( hasKEY( $GLOBALS["vokaleGRI"] , $buchs[1] ) ){ // zweiter ein Vokal
                $b2dia = ExtractDiafromBuchst( $aword[1] )[0];
                //$b1dia = ExtractDiafromBuchst(aword[0])[0]; 
                //console.log(  "zweiter vokal", ""b2dia, b2dia.indexOf(  "\u{0308}" )) 
                //insert the https=>//de.wikipedia.org/wiki/Unicodeblock_Kombinierende_diakritische_Zeichen
                if( mb_strpos( $b2dia, "\u{0308}" ) !== False  ){ //zweiter Buchstabe mit Trema, erste Buchstabe mit spiritus lenis
                    return $aword[0]." ".substr( $aword, 1 );
                } else { //
                    return $aword;
                }
            } else {
                return $aword;
            }
        } else {
            return $aword;
        }
    } else {
        return $aword;
    }
        
}

function AlphaPrivativumCopulativumText( $atext ){
    $t = "";
    $spli = explode( " ", $atext );
    foreach( $spli as $l => $v ){
        $t = $t." ".AlphaPrivativumCopulativum( $v );
    }
    return $t;
}


//KLAMMERSYSTEME HIER BEHANDELN

//******************************************************************************
// Section 1 
// unicode related comparing and norming, handling of diacritics
//******************************************************************************

// function takes string, splits it with jota subscriptum and joins the string again using jota adscriptum
function iotasubiotoad( $aword ){
 	return implode( "ι", explode( "\u{0345}", $aword ) );
}

// function takes "one word"
function ohnediakritW( $aword ){
    foreach( $GLOBALS["diacriticsunicodeRegExp"] as $dia   ){ //use replace array and put both array into preg_replace
		$aword = preg_replace( $dia, "", $aword );
	}
	return $aword;
}

function capitali( $astring ) {
    //return ucfirst( strtolower( $astring ));
    return ucfirst( mb_strtolower( $astring, "UTF-8" ));
}

// function takes a string replaces some signs with regexp and oth
function nodiakinword( $aword ){
    //$spt = ((aword.replace(strClean1, "").replace(strClean2, "").replace(strClean3, "").replace(strClean4, "")).normalize( analysisNormalform ));
    //return iotasubiotoad( ohnediakritW( spt ) );
    return iotasubiotoad( ohnediakritW( normalizer_normalize( $aword, $GLOBALS["analysisNormalform"] ) ) );
}

//******************************************************************************
// Section 2 deleting things that could be not same in two texts
//******************************************************************************

// function take a string and deletes diacritical signes, ligatures, remaining interpunction, line breaks, capital letters to small ones, equalizes sigma at the end of greek words, and removes brakets
function delall( $text ){
    if( $GLOBALS["doUVlatin"] ){ // convert u to v in classical latin text
        $text=deluv(delklammern(sigmaistgleich(delgrkl(delumbrbine(delligaturen(delinterp(delmakup(delnumbering(delunknown(deldiak($text)))))))))));
    } else {
        $text=delklammern(sigmaistgleich(delgrkl(delumbrbine(delligaturen(delinterp(delmakup(delnumbering(delunknown(deldiak($text))))))))));
    }
    return $text;
}

//run this before the klammern deletion
function delnumbering( $text ){ //untested
    $text = preg_replace( $GLOBALS["numeringReg1"], "", $text );
    $text = preg_replace( $GLOBALS["numeringReg2"], "", $text );
    return $text;
}

// function take a string and replaces all occorences of a regular expression
function delligaturen( $text ){
    
    $text = preg_replace( $GLOBALS["regEstigma"], "στ", $text );
    $text = preg_replace( $GLOBALS["regEstigmakl"], "στ", $text );
    $text = preg_replace( $GLOBALS["regEUk"], "Υκ", $text );
    $text = preg_replace( $GLOBALS["regEuk"], "υκ", $text );
    $text = preg_replace( $GLOBALS["regEomikonyplsi"], "ου", $text );
    $text = preg_replace( $GLOBALS["regEomikonyplsiK"], "ου", $text );
    $text = preg_replace( $GLOBALS["regEkai"], "καὶ", $text );
    $text = preg_replace( $GLOBALS["regEKai"], "Καὶ", $text );
    /*$text = preg_replace( $GLOBALS["regEl1"], "\u{039F}\u{03C5}", $text );
    $text = preg_replace( $GLOBALS["regEl2"], "\u{03BF}\u{03C5}", $text );*/

    

    return $text;
}

// function takes string and splits it into words, than normalizes each word, joins the string again
function deldiak( $text ){
    $spt = explode( " ", $text ); //seperate words
    $lele = len( $spt );
    for( $wi = 0; $wi < $lele; $wi+=1 ){
        $spt[ $wi ] = nodiakinword( $spt[ $wi ] );
    }
    return implode(" ", $spt );
}    

// function takes a string and replaces interpunction
function delinterp( $text ){
    $text = preg_replace( $GLOBALS["regEdoppelP"], " ", $text );
    $text = preg_replace( $GLOBALS["regEeinfahP"], " ", $text );
    $text = preg_replace( $GLOBALS["regEkomma"], " ", $text );
    $text = preg_replace( $GLOBALS["regEsemiK"], " ", $text );
    $text = preg_replace( $GLOBALS["regEhochP"], " ", $text );
    $text = preg_replace( $GLOBALS["regEausr"], " ", $text );
    $text = preg_replace( $GLOBALS["regEfarge"], " ", $text );
    $text = preg_replace( $GLOBALS["regEan1"], " ", $text );
    $text = preg_replace( $GLOBALS["regEan2"], " ", $text );
    $text = preg_replace( $GLOBALS["regEan3"], " ", $text );
    $text = preg_replace( $GLOBALS["regEan4"], " ", $text );
    $text = preg_replace( $GLOBALS["regEan5"], " ", $text );
    $text = preg_replace( $GLOBALS["regEan6"], " ", $text );
    return $text;
}

// function takes a string and replaces some unknown signs
function delunknown( $text ){
    $text = preg_replace( $GLOBALS["regU1"], "", $text );
    $text = preg_replace( $GLOBALS["regU2"], "", $text );
    $text = preg_replace( $GLOBALS["regU3"], "", $text );
    $text = preg_replace( $GLOBALS["regU4"], "", $text );
    return $text;
}


// function takes string and replace html line breakes
function delumbrbine( $text ){
    $text = preg_replace( $GLOBALS["regEbr1"], "", $text );
    $text = preg_replace( $GLOBALS["regEbr2"], "", $text );
    return $text;
}

//more to come
function delmakup( $text ){
    $text = preg_replace( $GLOBALS["cleanhtmltags"], "", $text );
    $text = preg_replace( $GLOBALS["cleanhtmlformat1"], "", $text );
    return $text;
}

// ...
function delgrkl( $text ){
    /*$a = own_mb_str_split($text);
    foreach( $a as $k => $v ){
        echo $k." ".$v." ".strtolower( $v )."<br>";
        $a[$k] = strtolower( $v );
    }
    return implode( "", $a );*/
    return mb_strtolower( $text );
}

// function takes string and converts tailing sigma to inline sigma (greek lang)
function sigmaistgleich( $text ){
    return preg_replace( $GLOBALS["regEtailingsig"], "σ", $text );
}


// function take sstring and replaces the brakets -- do not run this before the Klammersystem fkt
function delklammern( $text ){
    $text = preg_replace( $GLOBALS["regEkla1"], "", $text );
    $text = preg_replace( $GLOBALS["regEkla2"], "", $text );
    $text = preg_replace( $GLOBALS["regEkla3"], "", $text );
    $text = preg_replace( $GLOBALS["regEkla4"],"", $text );
    $text = preg_replace( $GLOBALS["regEkla5"],"", $text );
    $text = preg_replace( $GLOBALS["regEkla6"],"", $text );
    $text = preg_replace( $GLOBALS["regEkla7"],"", $text );
    $text = preg_replace( $GLOBALS["regEkla8"],"", $text );
    $text = preg_replace( $GLOBALS["regEkla9"],"", $text );
    $text = preg_replace( $GLOBALS["regEkla10"],"", $text );
    $text = preg_replace( $GLOBALS["regEkla11"],"", $text );
    $text = preg_replace( $GLOBALS["regEkla12"],"", $text );
    $text = preg_replace( $GLOBALS["regEkla13"],"", $text );
    $text = preg_replace( $GLOBALS["regEkla14"],"", $text );
    $text = preg_replace( $GLOBALS["regEkla15"],"", $text );
    $text = preg_replace( $GLOBALS["regEkla16"],"", $text );
    return $text;
}

// function takes string and replaces u by v, used in classical latin texts
function deluv( $text ){
    return preg_replace( $GLOBALS["regEuv"], "v" , $text );
}

//some bundels
function Trennstricheraus( $wliste ){
	$ersterteil = "";
	$zweiterteil = "";
	$neueWLISTE = [];
    $lele = len( $wliste );
	for( $w = 0; $w < $lele; $w+=1 ){
		if( len($ersterteil) === 0 ){
			if( mb_strpos( $wliste[ $w ], "-" ) !== False ){
				$eUNDz = explode( "-", $wliste[ $w ] );
				if( len( $eUNDz[1] ) > 0 ){
					$zweiohnenewline = explode( "\n", $eUNDz[1] );
			 		$neueWLISTE[] = $eUNDz[0].$zweiohnenewline[ len($zweiohnenewline)-1 ];
				} else {
					$ersterteil = $eUNDz[0];
				}
			} else { //nix - normales wort
				$neueWLISTE[] = $wliste[ $w ];
			}
		} else { // es gab eine Trennung und die ging über zwei Listenzellen
			if( mb_strpos( $wliste[ $w ], "[" ) === False && mb_strpos( $wliste[ $w ], "]" ) === False ){
				$zweiteralsliste = explode( "\n", $wliste[ $w ] );
				$neueWLISTE[] = $ersterteil.$zweiteralsliste[ len($zweiteralsliste)-1 ];
				$ersterteil = "";
			} else { //klammern behandeln
					 //wenn ich hier kein push auf der neune Wortliste mache, dann lösche ich damit die geklammerten sachen

				if( mb_strpos( $wliste[ $w ], "[" ) !== False && mb_strpos($wliste[ $w ], "]" ) !== False ){ //klammern in einem Wort
					$zweiteralsliste = explode( "]", $wliste[ $w ] );
				                                    
					$neueWLISTE[] = $ersterteil.substr( $zweiteralsliste[1], 1 );
					//console.log("NO SPLIT", ersterteil+zweiteralsliste[1].substring(1, zweiteralsliste[1].length-1));
				} else if( mb_strpos( $wliste[ $w ], "[" ) !== False ){
					$zweiteralsliste = explode( "[", $wliste[ $w ] );
					$neueWLISTE[] = $ersterteil.implode( "", $zweiteralsliste);
				} else { //nur schließende Klammer
					$zweiteralsliste = explode( "]", $wliste[ $w ] );
					$neueWLISTE[] = $ersterteil.$zweiteralsliste[1];
					//console.log("NO SPLIT", ersterteil+zweiteralsliste[1].substring(1, zweiteralsliste[1].length-1));
				}
			}
		}
	}
	return $neueWLISTE;
}

function UmbruchzuLeerzeichen( $atext ){
	$atext = implode( " ", explode( "\n", $atext) );
	return $atext;
}

function Interpunktiongetrennt( $wliste ){
    $neuewliste = [];
    foreach( $GLOBALS["satzzeichen"] as $sa => $v ){
        foreach( $wliste as $w => $wv ){ //besser &$wv
            if( mb_strpos( $wv, $v ) !== False ){
                $neuewliste[] = implode( "", explode( $v, $wv) );
                $neuewliste[] = $v;
            } else {
                $neuewliste[] = $wv;
            }
        }
        $wliste = $neuewliste;
        $neuewliste = [];
    }
	return $wliste;
}

function iotasubiotoadL( $wliste ){
	foreach( $wliste as $w => $v  ){
		$wliste[ $w ] = iotasubiotoad( $v );
	}
	return $wliste;
}

//function to use with greek text maybe
function GRvorbereitungT( $dtext ){
	$diewo =  explode( " ", disambiguDIAkritika( delgrkl( normalizer_normalize( delnumbering( $dtext), $GLOBALS["analysisNormalform"] ) ) ) );
    //$diewo = iotasubiotoadL( $diewo );
	$diewo = explode( " ", UmbruchzuLeerzeichen( implode( " ", Trennstricheraus( $diewo ) ) ) );
	$diewo = Interpunktiongetrennt( $diewo );
	//$diewo = Klammernbehandeln( $diewo );
	return $diewo;
} 

//******************************************************************************
// Section 3 Edition Klammerung
//******************************************************************************
function hervKLAMMSYS( $stringtomani ){ //RUN ON NFC/NFKC
    $matches = [];
    preg_match( $GLOBALS["lueckeBestimmt"], $stringtomani, $matches, PREG_OFFSET_CAPTURE );
    $out = "";
    $startindex = 0;
    foreach( $matches as $ma ){
        //console.log( lueckeBestimmt.lastIndex-matches[i].length, lueckeBestimmt.lastIndex, matches[i] );
        $out = $out.substr( $stringtomani, $startindex, $ma[1] )."<b>".$ma[0]."</b><sup>l0</sup>";
        $startindex = $ma[1]+len( $ma[0] );
    }
    $out = $out.substr( $stringtomani, $startindex );
    return $out;
}

function delKLAMMSYS( $stringtomani ){ //RUN ON NFC/NFKC
    $matches = [];
    preg_match( $GLOBALS["lueckeBestimmt"], $stringtomani, $matches, PREG_OFFSET_CAPTURE );
    $out = "";
    $startindex = 0;
    foreach( $matches as $ma ){
        //console.log( lueckeBestimmt.lastIndex-matches[i].length, lueckeBestimmt.lastIndex, matches[i] );
        $out = $out.substr( $stringtomani, $startindex, len( $ma[0] ) );
        $startindex = $ma[1]+len( $ma[0] );
    }
    $out = $out.substr( $stringtomani, $startindex );
    return $out;
}

//******************************************************************************
// USAGE
//******************************************************************************
function readfilein( $file ){
    $s = "";
    if( file_exists( $file ) ){
        if( ($h = fopen($file, "r")) !== FALSE ){
            $s = fread($h,filesize($file));
            fclose($h);       
      }//end if
    }//end if 
 
  return $s;     
}

function writefileout( $tn, $txt ){
    $myfile = fopen( $tn, "w") or die("Unable to open file!");
    fwrite($myfile, $txt);
    fclose($myfile);
}


//demsplitmb( );
function demsplitmb(){
    $testfile = 'test_strnorm.txt';  
    $atesttext = readfilein( $testfile );
    //$atesttext = 

    echo "<b>Not normalized multbyte string str_split:</b><br>";
    echo print_r(str_split($atesttext) );

    $testnorm = normatext( $atesttext, $GLOBALS["analysisNormalform"] );
    echo "<br><b>Normalized (NFKD) multbyte string str_split:</b><br>";
    echo print_r(str_split($testnorm) );

    echo "<br><b>Normalized (NFKD) multbyte string own_mb_str_split:</b><br>";
    echo implode( " /// ", own_mb_str_split($testnorm) );
    writefileout( "outofteststrnorm.txt", implode( " /// ", own_mb_str_split($testnorm) ) );
}

demUsagePHP( );

function demUsagePHP( ){
    //small greek/latin example
    normalizearraykeys(); //!
    //$atesttext = "„[IX]” ⁙ ἀλλ’ ἑτέραν τινὰ φύσιν ἄπειρον', ἐξ ἧς ἅπαντας γίνεσθαι τοὺς οὐρανοὺς καὶ τοὺς ἐν αὐτοῖς κόσμους· ἐξ ὧν δὲ ἡ γένεσίς ἐστι τοῖς οὖσι, καὶ τὴν φθορὰν εἰς ταῦτα γίνεσθαι κατὰ τὸ χρεών. διδόναι γὰρ αὐτὰ δίκην καὶ τίσιν ἀλλήλοις τῆς ἀδικίας κατὰ τὴν τοῦ χρόνου τάξιν, ποιητικωτέροις οὕτως ὀνόμασιν αὐτὰ λέγων· δῆλον δὲ ὅτι τὴν εἰς ἄλληλα μεταβολὴν τῶν τεττάρων στοιχείων οὗτος θεασάμενος οὐκ ἠξίωσεν ἕν τι τούτων ὑποκείμενον ποιῆσαι, ἀλλά τι ἄλλο παρὰ ταῦτα. οὗτος δὲ οὐκ ἀλλοιουμένου τοῦ στοιχείου τὴν γένεσιν ποιεῖ, ἀλλ’ ἀποκρινομένων τῶν ἐναντίων διὰ τῆς ἀιδίου κινή- σεως· 1 Summá pecúniae, quam dedit in [bla bla bla] aerarium vel plebei Romanae vel dimissis militibus=> denarium sexiens milliens. 2 Opera fecit nova § aedem Martis, Iovis Tonantis et Feretri, Apollinis, díví Iúli, § Quirini, § Minervae, Iunonis Reginae, Iovis Libertatis, Larum, deum Penátium, § Iuventatis, Matris deum, Lupercal, pulvinar ad [11] circum, § cúriam cum chalcidico, forum Augustum, basilicam 35 Iuliam, theatrum Marcelli, § porticus . . . . . . . . . . , nemus trans Tiberím Caesarum. § 3 Refécit Capitolium sacrasque aedes numero octoginta duas, theatrum Pompeí, aquarum rivos, viam Flaminiam.  Ϗ ϗ ϚϛȢȣꙊꙋἀἁἂἃἄἅἆἇἈἉἊἋἌἍἎἏἐἑἒἓἔἕἘἙἚἛἜἝἠἡἢἣἤἥἦἧἨἩἪἫἬἭἮἯἰἱἲἳἴἵἶἷἸἹἺἻἼἽἾἿὀὁὂὃὄὅὈὉὊὋὌὍὐὑὒὓὔὕὖὗὙὛὝὟὠὡὢὣὤὥὦὧὨὩὪὫὬὭὮὯὰάὲέὴήὶίὸόὺύὼώ	ᾀᾁᾂᾃᾄᾅᾆᾇᾈᾉᾊᾋᾌᾍᾎᾏᾐᾑᾒᾓᾔᾕᾖᾗᾘᾙᾚᾛᾜᾝᾞᾟᾠᾡᾢᾣᾤᾥᾦᾧᾨᾩᾪᾫᾬᾭᾮᾯᾰᾱᾲᾳᾴᾶᾷᾸᾹᾺΆᾼ᾽ι᾿῀῁ῂῃῄῆῇῈΈῊΉῌ῍῎῏ῐῑῒΐῖῗῘῙῚΊ῝῞῟ῠῡῢΰῤῥῦῧῨῩῪΎῬ῭΅`ῲῳῴῶῷῸΌῺΏῼ´῾ͰͱͲͳʹ͵Ͷͷͺͻͼͽ;Ϳ΄΅Ά·ΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϏϐϑϒϓϔϕϖϗϘϙϚϛϜϝϞϟϠϡϢϣϤϥϦϧϨϩϪϫϬϭϮϯϰϱϲϳϴϵ϶ϷϸϹϺϻϼϽϾϿ Αι αι γγ γκ γξ γχ ου Υι υι ἄϋλος αὐλός  τί φῄς; γραφὴν σέ τις, ὡς ἔοικε, γέγραπται οὐ γὰρ ἐκεῖνό γε καταγνώσομαι, ὡς σὺ ἕτερον. δ̣[ὲ κ]αὶ";
    $testfile = 'test_strnorm.txt';  
    $atesttext = readfilein( $testfile );
    
    //print_r($GLOBALS);
    $atttext = "";

    //latin
    $GLOBALS["doUVlatin"] = true; 
    $str1 = "<b>Textinput 1:</b>";
    $atttext = $atttext."\n<br/>".$str1."<br/>\n".$atesttext;
    //normed in analysis form
    $testnorm = normatext( $atesttext, $GLOBALS["analysisNormalform"] );
    
    

    $disa = disambiguDIAkritika( $testnorm ); 
    $disades = "<b>a) Disambuguation of diacritics (takes a string, replaces diakritica to have them equaly encoded, return string):</b>\n";
    $atttext = $atttext."\n\n<br/><br/>".$disades."<br/>\n".$disa;

    $ex = ExtractDiafromBuchstText( $testnorm ); //input normalized
    $exdes = "<b>b) Separation of diakritics  (takes array of letters and returns array of array of diakritica and array of letters):</b>";
    $atttext = $atttext."\n\n<br/><br/>".$exdes."<br/>\n".$ex;

    $basicres =  basClean( $testnorm );   
    $str2 = "<b>c) Text output basic norm (basic equalization and hypenation reversal):</b>";
    $atttext = $atttext."\n\n<br/><br/>".$str2."<br/>\n".$basicres;

    $translitbsp = TraslitAncientGreekLatin( $basicres );
    $str12 = "<b>d) Text transliteration (takes greek utf8 string and returns transliterated latin utf8 string):</b>";  
    $atttext = $atttext."\n\n<br/><br/>".$str12."<br/>\n".$translitbsp; 

    $expeli = ExpandelisionText( $testnorm );
    $desexpeli = "<b>e) Elusion expansion (given a text, if this is an elusion it will be expanded):</b>";
    $atttext = $atttext."\n\n<br/><br/>".$desexpeli."<br/>\n".$expeli; 

    $spiekla = spitzeklammernHTML( $testnorm );
    $desspiekla = "<b>f) Spitze Klammern zu html (escapes spitze klammern to html encoding):</b>";  
    $atttext = $atttext."\n\n<br/><br/>".$desspiekla."<br/>\n".$spiekla;

    $al = AlphaPrivativumCopulativumText( $atesttext ); //Normal form composed!!!
    $desal = "<b>g) Alpha privativum  / copulativum (takes utf8 greek and splits the alpha privativum and copulativum from wordforms):</b>";  
    $atttext = $atttext."\n\n<br/><br/>".$desal."<br/>\n".$al;

    $jo = iotasubiotoad( $testnorm ); //Normal form composed!!!
    $desjo = "<b>h) JOTA (takes greek utf8 string and repleces jota subscriptum with jota ad scriptum):</b>";  
    $atttext = $atttext."\n\n<br/><br/>".$desjo."<br/>\n".$jo;

    $diakdelled = deldiak( $basicres );
    $str3 = "<b>i) Text output without diacritics (replaces diacritics):</b>" ;
    $atttext = $atttext."\n\n<br/><br/>".$str3."<br/>\n".$diakdelled;

    $numb = delnumbering( $testnorm );
    $desnumb = "<b>j) Text output without numbering (takes string return string without the edition numbering i.e. [2]):</b>" ;
    $atttext = $atttext."\n\n<br/><br/>".$desnumb."<br/>\n".$numb;
    
    $unk = delunknown( $testnorm );
    $desunk = "<b>k) Text output without some signs (delete some to the programmer unknown signs=> †, *,⋖,#):</b>" ;
    $atttext = $atttext."\n\n<br/><br/>".$desunk."<br/>\n".$unk;

    $mark = delmakup( $testnorm );
    $desmark = "<b>l) Text output without markup (input a string and get it pack with markup removed):</b>" ;
    $atttext = $atttext."\n\n<br/><br/>".$desmark."<br/>\n".$mark;

    $interpdelled = delinterp( $basicres );
    $str4 = "<b>m) Text output without punctuation (takes string and returns the string without):</b>";
    $atttext = $atttext."\n\n<br/><br/>".$str4."<br/>\n".$interpdelled;

    $ligdelled = delligaturen( $basicres );
    $str5 = "<b>n) Text output without ligature (takes a string return string with ligatures turned to single letters):</b>";
    $atttext = $atttext."\n\n<br/><br/>".$str5."<br/>\n".$ligdelled;

    $umbrdelled = delumbrbine( $basicres );
    $str6 = "<b>o) Text output without newline (input string and get it back with linebreaks removed):</b>";
    $atttext = $atttext. "\n\n<br/><br/>". $str6."<br/>\n". $umbrdelled;

    $grkldelled = delgrkl( $basicres );
    $str7 = "<b>p) Text output equal case (input a string and get it bach with all small case letters):</b>";
    $atttext = $atttext."\n\n<br/><br/>".$str7."<br/>\n".$grkldelled;

    $sidelled = sigmaistgleich( $basicres );
    $str8 = "<b>q) Text output tailing sigma uniform (equalize tailing sigma):</b>";
    $atttext = $atttext."\n\n<br/><br/>".$str8."<br/>\n".$sidelled;

    $kladelled = delklammern( $basicres );
    $str9 = "<b>r) Text output no brackets (input stringa nd get it back with no brackets):</b>";
    $atttext = $atttext."\n\n<br/><br/>".$str9."<br/>\n".$kladelled;

    $uvdelled = deluv( $basicres );
    $str10 = "<b>s) Text output latin u-v (repaces all u with v):</b>";
    $atttext = $atttext."\n\n<br/><br/>".$str10."<br/>\n".$uvdelled;

    $alldelled = delall( $basicres );
    $str11 = "<b>t) Text output all deleted (deletes UV, klammern, sigma, grkl, umbrüche, ligaturen, interpunktion, edition numbering, unknown signs, diakritika):</b>";
    $atttext = $atttext."\n\n<br/><br/>".$str11."<br/>\n".$alldelled;

    $tre = Trennstricheraus( explode(" ", $testnorm ) );
    $destre = "<b>u) Text output no hypens (input array of words removes hyphenation):</b>";
    $atttext = $atttext."\n\n<br/><br/>".$destre."<br/>\n".implode( " ", $tre);

    $comb = GRvorbereitungT( $atesttext );
    $descomb = "<b>v) Text output a combination of steps (diacritics disambiguation, normalization, hyphenation removal, linebreak to space, punctuation separation and bracket removal):</b>";       
    $atttext = $atttext."\n\n<br/><br/>".$descomb."<br/>\n".implode( " ", $comb);
   
    //$klammsys = delKLAMMSYS( $testnorm );
    $klammsys = hervKLAMMSYS( $atesttext );
    $desklammsys = "<b>w) Editions Klammerung (leidener Klammersystem):</b>";  
    $atttext = $atttext."\n\n<br/><br/>".$desklammsys."<br/>\n".$klammsys;

    echo $atttext;
    //writefileout( "test_out_strnorm.txt", $atttext );
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

hervKLAMMSYS( text ) // input a string, mark all editorial signs
*/
//eof

?>
