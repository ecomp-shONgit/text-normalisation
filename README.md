# Goal of the software

This is a set of JavaScript/Python3/PHP functions (unified over the three implementations) that represent a minimum of text normalization (aka cleaning) for the work with Latin and polytonic Greek digital texts (UTF8). You can realize different levels of text normalization. There is a documented set of functions to be called on text or tokens (a set of tokens is created by a  *.split( " " )* on a string considered to be a space separated text).

# Usage

Include it to your website: *<script type="text/javascript" src="textnorm.js"></script>*

Or use the example: Download the github repository, unzip it and open textnorm.html, see JavaScript file for the
*demUsage( )* function.

Demo JS: http://www.ecomparatio.net/~khk/textnorm/textnorm.html (input own text)

Demo PHP: http://www.ecomparatio.net/~khk/textnorm/textnorm.php (output as txt: http://www.ecomparatio.net/~khk/textnorm/test_out_strnorm.txt)

# Ligatures and abbreviations

Note: we cover very view ligatures and no abbreviations. The list of ligatures and abbreviations will be very long. Often ligatures and abbreviations broken down through the transcription process. If work on this is needed let us know.

# UTF8

For the purpose of text analysis it is suitable to use the NFD and for the purpose display the NFC is better (typography).

# Functions

## setAnaFormTO( formstring )

Setter for global variable of analysis-normalform.

## setDisplFormTO( formstring )

Setter for the global variable of display-normalform.

## disambiguDIAkritika( string )

Return *string* with replaced diacritics.

## normarrayk( array )

Normalizes the key strings of a dictionary.

## normatextwordbyword( text, wichnorm )

Splits the text into words and calls norm fkt on it.

## normatext( text, wichnorm )

Calles norm fkt on whole string.

## disambiguDIAkritika( astr )

Takes a string, replaces diacritics to have them equal encoded, return new string.

## ExtractDiafromBuchst( buchst )

Takes array of letters and returns array of array of diacritics and array of letters.

## replaceBehauchung( adiakstring )

Replaces *Behauchung* in the transliteration of Greek to Latin.

## Expandelision( aword )

Given a word, if this is an *Elusion* it will be expanded.

## TraslitAncientGreekLatin( astring )

Takes Greek UTF8 string and returns transliterated Latin UTF8 string.

## spitzeklammernHTML

Escapes arrow brackets to HTML encoding.

## basClean( astring )

Basic equalization and hyphenation reversal.

## AlphaPrivativumCopulativum( aword )

Takes a word UTF8 Greek and splits the *alpha privativum* and *copulativum* from wordform.

## iotasubiotoad( aword )

Takes Greek UTF8 string and replaces *jota subscriptum* with *jota ad scriptum*.

## ohnediakritW( aword )

Replaces diacritics.

## capitali( astring )

First letter capitalized, rest lowercase.

## nodiakinword( astring )

Combination of diacrics removal and *jota subscriptum* conversion.

## delall( text )

Deletes latin-UV, brackets, sigma, same case, hyphenation, ligatures, punctuation, edition numbering, unknown signs, diacritics.

## delnumbering( text )

Takes string and return string without the edition numbering i.e. [2].

## delligaturen( text )

Takes a string and return string with ligatures turned to single letters.

## deldiak( text )

Like *nodiakinword()*.

## delinterp( text )

Takes string and returns the string without punctuation.

## delunknown( text )

Delete some to the programmer unknown signs.

## delumbrbine( text )

Input a string and get it back with line breaks removed.

## delmakup( text )

Input a string and get it back with markup removed.

## delgrkl( text )

Input a string and get it back with all small case letters.

## sigmaistgleich( text )

Equalize tailing sigma with sigma.

## delklammern( text )

Input string and get it back with no brackets.

## deluv( text )

Repaces all u with v.

## Trennstricheraus( array of words )

Input a array of words, removes hyphenation.

## UmbruchzuLeerzeichen( text )

Input a string and get back a string with newlines replaces by spaces.

## Interpunktiongetrennt( wordlist )

Input array of words and have the punctuation separated from each word.

## Klammernbehandeln( wordlist )

Same as delklammern but on array of words.

## iotasubiotoadL( wordlist )

Same as iotasubiotoad but on array of words.

## GRvorbereitungT( text )

Input a string and get a combination of diacritic disambiguation, normalization, hyphenation removal, line break to space, punctuation separation and bracket removal

## hervKLAMMSYS( text )

Input a string, mark all *signis criticis*.

