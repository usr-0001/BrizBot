from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from source.persistance.models import ViewKindVariant

__all__ = ["resolve_view_kind"]


def resolve_view_kind(id: int) -> ViewKindVariant | None:
    """
    Identify the kind by the specific id.

    :param id: The id of the view kind.
    :type id: int

    :return: The corresponding ViewKindVariant enum member if found, None otherwise.
    :rtype: ViewKindVariant | None
    """
    try: return ViewKindVariant(id)
    except ValueError: return None
