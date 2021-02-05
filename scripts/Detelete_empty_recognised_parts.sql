SELECT * FROM LegoSorterDB.Recognisedparts WHERE ID < 166 AND no IS NULL

UPDATE LegoSorterDB.Recognisedparts SET DELETED = now() WHERE id < 984 AND score IS NULL
