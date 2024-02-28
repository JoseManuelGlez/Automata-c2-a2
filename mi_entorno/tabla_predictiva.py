tabla_predictiva = {
    ('start', 'FUNCTION'): ['S'],

    ('S', 'FUNCTION'): ['F', 'N', 'PM'],
    ('F', 'FUNCTION'): ['function'],
    ('PM', 'OPEN_PAREN'): ['PA', 'PL', 'PC'],
    ('PA', 'OPEN_PAREN'): ['('],
    ('PC', 'CLOSE_PAREN'): [')'],
    ('PL', 'VAR'): ['V', 'X', 'LT'],
    ('V', 'VAR'): ['var'],
    ('X', 'LETTER'): ['N', ':', 'T'],
    ('N', 'LETTER'): ['L', 'RN'],

    ('RN', 'LETTER'): ['L', 'RN'],
    ('RN', 'TWO_DOT'): ['EPSILON'],
    ('RN', 'OPEN_PAREN'): ['EPSILON'],

    ('L', 'LETTER'): ['letra'],

    ('T', 'BOOLEAN'): ['boolean'],
    ('T', 'STRING'): ['string'],

    ('LT', 'CLOSE_PAREN'): ['EPSILON'],
    ('LT', 'DOT_COMA'): ['P', 'X', 'LT'],

    ('P', 'DOT_COMA'): [';'],

    ('function', 'FUNCTION'): ['FUNCTION'],
    ('(', 'OPEN_PAREN'): ['OPEN_PAREN'],
    (')', 'CLOSE_PAREN'): ['CLOSE_PAREN'],
    ("var", 'VAR'): ['VAR'],
    ("string", 'STRING'): ['STRING'],
    ("boolean", 'BOOLEAN'): ['BOOLEAN'],
    (";", 'DOT_COMA'): ['DOT_COMA'],
    (":", 'TWO_DOT'): ['TWO_DOT'],

    ('letra', 'LETTER'): ['LETTER'],
    ('numero', 'NUMBER'): ['NUMBER'],

    ('RE', 'EOF'): ['EPSILON'],
}
