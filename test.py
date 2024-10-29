def test_valid(cldf_dataset, cldf_sqlite_database, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)
    res = cldf_sqlite_database.query("select cldf_latitude from languagetable where cldf_id = 'aust1307'")
    assert res[0][0] > 0
