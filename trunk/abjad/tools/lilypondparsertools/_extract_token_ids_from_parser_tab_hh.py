def _extract_token_ids_from_parser_tab_hh(filepath):

    f = open(filepath, 'r')
    lines = f.read( ).split('\n')
    f.close( )

    token_ids = { }
    in_enum = False
    for line in lines:
        text = line.strip( )

        if in_enum and text == '};':
            break;

        if in_enum:
            parts = text.split(' ')
            name = parts[0]
            if parts[2].endswith(','):
                number = int(parts[2][:-1])
            else:
                number = int(parts[2])
            token_ids[number] = name

        if text == 'enum yytokentype {':
            in_enum = True

    return token_ids
