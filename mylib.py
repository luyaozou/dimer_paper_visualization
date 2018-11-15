#! encoding = utf-8

def gen_search_sql_str(search_opts):
    ''' Generate sqlite3 inqury strings.

    Arguments
    search_opts -- (mol1, mol2, yr_start, yr_end, checked_lit_types)

    Returns
    sql_str -- str, sqlite3 query string
    sql_arg -- single value / list, sqlite3 query arguments

    '''

    (mol1, mol2, yr_start, yr_end, checked_lit_types) = search_opts

    sql_arg = []
    sql_frag = []
    sql_str = ""

    if mol1 and mol2:   # if both molecules are specified
        sql_frag.append("(mol1 = ? AND mol2 = ?) OR (mol1 = ? AND mol2 = ?)")
        sql_arg.append(mol1)
        sql_arg.append(mol2)
        sql_arg.append(mol2)
        sql_arg.append(mol1)
    elif mol1:
        sql_frag.append("(mol1 = ? OR mol2 = ?)")
        sql_arg.append(mol1)
        sql_arg.append(mol1)
    elif mol2:
        sql_frag.append("(mol1 = ? OR mol2 = ?)")
        sql_arg.append(mol2)
        sql_arg.append(mol2)
    else:
        pass

    if yr_start:
        sql_frag.append("year >= ?")
        sql_arg.append(yr_start)
    else:
        pass

    if yr_end:
        sql_frag.append("year <= ?")
        sql_arg.append(yr_end)
    else:
        pass

    if checked_lit_types:
        n = len(checked_lit_types)
        _this_str = "?, " * (n-1) + "?"
        sql_frag.append("lit_type in ({:s})".format(_this_str))
        for item in checked_lit_types:
            sql_arg.append(item)
    else:
        pass

    if sql_frag:  # if there are arguments
        while sql_frag:   # stitch all sql fragments together
            sql_str = " AND " + sql_frag.pop() + sql_str
        # chop off the first " AND " and replace it with " WHERE "
        return "SELECT * FROM lit WHERE" + sql_str[4:], sql_arg
    else:   # no arguments, return a pure search sentence
        return "SELECT * FROM lit", []
