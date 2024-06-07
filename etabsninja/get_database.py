import pandas as pd
pd.options.mode.chained_assignment = None
from typing import Optional, Tuple, List, Any

class DatabaseTables:
    def __init__(self,SapModel=None,etabs=None):
        if not SapModel:
            self.etabs = etabs
            self.SapModel = etabs.SapModel
        else:
            self.SapModel = SapModel
    
    @staticmethod
    def reshape_data_to_df(table: Tuple[Any, Any, List[str], Any, List[Any]], cols: Optional[List[str]] = None) -> pd.DataFrame:
        FieldsKeysIncluded = table[2]
        table_data = table[4]
        n = len(FieldsKeysIncluded)
        data = [list(table_data[i:i + n]) for i in range(0, len(table_data), n)]
        df = pd.DataFrame(data, columns=FieldsKeysIncluded)
        if cols is not None:
            df = df[cols]
        return df
    
    def table_exist(self, table_key: str) -> bool:
        all_table = self.SapModel.DatabaseTables.GetAvailableTables()[1]
        return table_key in all_table

    def read(self, table_key: str, to_dataframe: bool = False) -> Optional[pd.DataFrame]:
        data = self.read_table(table_key)
        if data is None:
            return None
        if to_dataframe:
            df = self.reshape_data_to_df(data)
            return df
        return None  # Explicitly return None if not converting to DataFrame

    def read_table(self, table_key: str) -> Optional[Tuple[str, List[Any], List[str], int, List[Any]]]:
        GroupName = table_key
        FieldKeyList = []
        TableVersion = 0
        FieldsKeysIncluded = []
        NumberRecords = 0
        TableData = []
        if not self.table_exist(table_key):
            return None
        return self.SapModel.DatabaseTables.GetTableForDisplayArray(table_key, FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
