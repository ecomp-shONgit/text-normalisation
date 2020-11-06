# Goal of the software

This is a set of JavaScript/Python3/PHP functions (unified over the three implementations, a Rust Version could be foubnd in this repository: https://github.com/ecomp-shONgit/string-thing) that represent a minimum of text normalization (cleaning) for the work with Latin and polytonic Greek digital texts (UTF8). You can realize different levels of text normalization. There is a documented set of functions to be called on text or tokens (a set of tokens is created by a  *.split( " " )* on a string considered to be a space separated text).

Definition: A text normalization is everything done to equalize encoding, appearance 
and composition of a sequence of signs called a text. There are two goals of 
normalization. The first is a common ground of signs  and the second is a 
reduction of differences between two sequences of signs.  Not every 
normalization step is useful for every comparison task! Remember: 
Sometimes it is important to not equalize word forms and 
sometimes it is important.


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

## 1. Fkt: setAnaFormTO( string ) 

Setter for global variable of analysis UTF8-normalform string.

## 2. Fkt: setDisplFormTO( string ) 

Setter for the global variable of display UTF8-normalform.

## 3. Fkt: disambiguDIAkritika( string ) 

Return String with replaced diacritics.

## 4. Fkt: normarrayk( arrayofstrings ) 

Normalizes the key strings of a dictionary.

## 5. Fkt: normatextwordbyword( string, string ) 

Splits the fist string into words and calls norm fkt with second stroing as normalization parameter ("NFD").

## 6. Fkt: normatext( string, string ) 

Calles norm fkt on whole frist string with second string as normalization parameter.

## 7. Fkt: disambiguDIAkritika( string )

takes a string, replaces diakritica to have them equaly encoded, return string

## 8. Fkt: ExtractDiafromBuchst( arrayofletters ) 

Takes array of letters and returns array of array of diacritics and array of letters.

## 9. Fkt: replaceBehauchung( string ) 

Replaces aspiration in the transliteration of greek to roman letters.

## 10. Fkt: Expandelision( string ) 

Input a word (string), if it is an elusion it will be expanded.

## 11. Fkt: TraslitAncientGreekLatin( astring ) 

Takes greek utf8 string and returns transliterated in roman letters utf8 string.

## 12. Fkt: spitzeklammernHTML( string ) 

Escapes angle brackets to html encoding.

## 13. Fkt: basClean( string ) 

Basic equalisation and hypenation reversal.

## 14. Fkt: AlphaPrivativumCopulativum( string ) 

Takes a word utf8 greek and splits the alpha privativum and copulativum from wordform.

## 15. Fkt:  iotasubiotoad( string )  

Takes greek utf8 string and repleces jota subscriptum with jota adscriptum.

## 16. Fkt: ohnediakritW( string ) 

Replaces diacritics.

## 17. Fkt:  capitali( string )  

First letter of string capitalized rest lowercase.

## 18. Fkt: nodiakinword( string )  

Combination of diacritics removal and jota subscriptum conversion.

## 19. Fkt: delall( string ) 

Deletes UV, brackets, sigma, grkl, linebreaks, ligatures, punctuation, edition numbering, unknown signs, diacritics.

## 20. Fkt: delnumbering( string ) 

Takes a string and returns string without the edition numbering i.e. [2].

## 21. Fkt: delligaturen( string ) 

Takes a string and returns string with ligatures turned to single letters.

## 22. Fkt: deldiak( string ) 

Like nodiakinword().

## 23. Fkt: delinterp( string ) 

Takes a string and returns the string without punctuation.

## 24. Fkt: delunknown( string )  

Delete some, to the programmer unknown, signs from string.

## 25. Fkt: delumbrbine( string )  

Input a string and get it back with linebreaks removed.

## 26. Fkt: delmakup( string ) 

Input a string and get it back with markup removed.

## 27. Fkt: delgrkl( string ) 

Input a string and get it back with all small case letters.

## 28. Fkt: sigmaistgleich( string ) 

Equalize tailing sigma in string.

## 29. Fkt: delklammern( string )  

Input string and get it back with no brackets.

## 30. Fkt: deluv( string )  

Repaces all u with v.

## 31. Fkt: Trennstricheraus( arrayofwords ) 

Input array of words and get it back as array of words with removed hyphenation.

## 32. Fkt: UmbruchzuLeerzeichen( string )  

Input a string and get back a string with newlines replaces by spaces.

## 33. Fkt: Interpunktiongetrennt( wordlist ) 

Input array of words and have the punctuation separated from each word.

## 34. Fkt: Klammernbehandeln( wordlist ) 

Same as delklammern() but on array of words.

## 35. Fkt: iotasubiotoadL( wordlist ) 

Same as iotasubiotoad() but on array of words.

## 36. Fkt: GRvorbereitungT( string )

Input a string and get a combination of diacritics disambiguation, normalization, hyphenation removal, linebreak to space, punctuation separation and bracket removal.

