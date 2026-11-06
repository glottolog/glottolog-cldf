def test_valid(cldf_dataset, cldf_sqlite_database, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)
    res = cldf_sqlite_database.query("select cldf_latitude from languagetable where cldf_id = 'aust1307'")
    assert res[0][0] > 0
    res = cldf_sqlite_database.query("select count(cldf_id) from languagetable where cldf_macroarea = ''")
    assert res[0][0] < 250
    res = cldf_sqlite_database.query("select count(vs.sourcetable_id) as nrefs from valuetable_sourcetable as vs join valuetable as v on v.cldf_id = vs.valuetable_cldf_id where v.cldf_parameterreference = 'bib' group by v.cldf_languagereference order by nrefs desc limit 5")
    assert res[0][0] > 4000

    for val in cldf_dataset.objects('ValueTable'):
        if val.parameter.id == 'medovertime':
            assert isinstance(val.typed_value, list)
        else:
            _ = val.typed_value
