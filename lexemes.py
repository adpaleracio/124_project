# lexemes.py
# Description: contains regular expressions for lexemes

identifier = '^[a-zA-Z][a-zA-Z0-9\\_]*$'

lexemes_dict = {
    '^HAI$': 'Code Delimiter',
    '^KTHXBYE$': 'Code Delimiter',
    '^WAZZUP$': 'Code Delimiter',
    '^BUHBYE$': 'Code Delimiter',

    '^BTW$': 'Comment',
    '^OBTW$': 'Comment',
    '^TLDR$': 'Comment',

    '^I HAS A$': 'Variable Declaration',
    '^ITZ$': 'Variable Assignment',

    '^R$': 'Assignment Operator',

    '^0$|^\\-?[1-9][0-9]*$': 'Literal',
    '^".*"$': 'Literal',
    '^(WIN|FAIL)$': 'Literal',
    '^(NOOB|NUMBR|NUMBAR|YARN|TROOF)$': 'Literal',

    '^SUM OF$': 'Arithmetic Operator',
    '^DIFF OF$': 'Arithmetic Operator',
    '^PRODUKT OF$': 'Arithmetic Operator',
    '^QUOSHUNT OF$': 'Arithmetic Operator',
    '^MOD OF$': 'Arithmetic Operator',
    '^BIGGR OF$': 'Arithmetic Operator',
    '^SMALLR OF$': 'Arithmetic Operator',

    '^BOTH OF$': 'Boolean Operator',
    '^EITHER OF$': 'Boolean Operator',
    '^WON OF$': 'Boolean Operator',
    '^NOT$': 'Boolean Operator',
    '^ANY OF$': 'Boolean Operator',
    '^ALL OF$': 'Boolean Operator',

    '^BOTH SAEM$': 'Comparison Operator',
    '^DIFFRINT$': 'Comparison Operator',

    '^SMOOSH$': 'Concatenation Operator',
    '^\\+$': 'Concatenation Operator',
    
    '^MAEK$': 'Typecast Operator',
    '^A$': 'Typecast Keyword',
    '^IS NOW A$': 'Typecast Assignment',

    '^VISIBLE$': 'Output Keyword',
    '^GIMMEH$': 'Input Keyword',

    '^O RLY\\?$': 'If Statement Start',
    '^YA RLY$': 'If True Branch',
    '^MEBBE$': 'Else If Branch',
    '^NO WAI$': 'If False Branch',
    '^OIC$': 'If Statement End',

    '^WTF\\?$': 'Switch Statement Start',
    '^OMG$': 'Case Statement',
    '^OMGWTF$': 'Default Case',

    '^IM IN YR$': 'Loop Start',
    '^UPPIN$': 'Loop Increment',
    '^NERFIN$': 'Loop Decrement',
    '^YR$': 'Loop Variable',
    '^TIL$': 'Loop Until',
    '^WILE$': 'Loop While',
    '^IM OUTTA YR$': 'Loop End',

    '^HOW IZ I$': 'Function Declaration',
    '^IF U SAY SO$': 'Function End',
    '^GTFO$': 'Break Statement',
    '^FOUND YR$': 'Return Statement',
    '^I IZ$': 'Function Call',
    '^MKAY$': 'Expression End',
    
    '^AN$': 'And Operator'
}
