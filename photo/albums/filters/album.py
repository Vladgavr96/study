from django.db.models import Q


class AlbumFilter:

    def __init__(self, **kwargs):
        self.ordering = kwargs.get("ordering")
        self.ordering = self.ordering if self.ordering else []

    def __str__(self):
        return f"""
        orders       {self.ordering}
        get_q_filter {self.get_q_filter()}
        get_ordering {self.get_ordering()}
        """

    def get_q_filter(self) -> Q:
        q = Q()

        return q

    def get_ordering(self, valid_fields=["count", "created_at"]) -> [str]:
        valid_fields += [f'-{i}' for i in valid_fields] + [f'+{i}' for i in valid_fields]
        ret_ordering = []
        for item in self.ordering:
            if item in valid_fields:
                if item[0] == "+":
                    item = item[1:]
                ret_ordering.append(item)
        return ret_ordering
