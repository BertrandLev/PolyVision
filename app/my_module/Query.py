

class Query():
    """
    A class to manage the creation of SQL queries.
    
    Attributes:
        search_type (str): The search type for the query builder. It can take either "Quick" or "Advance" as values.
            Default is "Quick"

        conditions (list): contain the field, operator and values to create the where part of the query
    """
    def __init__(self) -> None:
        self.search_type = "Quick"
        self.conditions = []

    def add_conditions(self, condition) -> None:
        if not len(condition) == 3 :
            raise ValueError("Condition should be a list of 3 elements : Field/Operator/Values")
        self.conditions.append(condition)

    def preview_query(self) -> str:
        join_condition = ["/ ".join(condition) for condition in self.conditions]
        return "\n".join(join_condition)